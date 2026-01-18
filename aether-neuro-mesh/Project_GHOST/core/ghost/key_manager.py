import os
import json
import hmac
import hashlib
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple


@dataclass(frozen=True)
class EpochInfo:
    epoch_id: int
    starts_at_utc: str
    active: bool


class EpochKeyManager:
    """Epoch-based key rotation for deterministic tokenization.

    Demo behavior:
      - Stores epoch keys in a JSON file under data/keys/.
      - Uses a fixed epoch duration (seconds) and auto-creates the next epoch key when needed.

    Production guidance:
      - Store root keys in KMS/HSM.
      - Derive per-tenant/per-domain keys from a root key.
      - Never write raw keys to disk in plaintext.
    """

    def __init__(self, key_store_path: str = "data/keys/epoch_keys.json"):
        self.key_store_path = key_store_path
        self.epoch_seconds = int(os.getenv("GHOST_EPOCH_SECONDS", str(90 * 24 * 60 * 60)))  # default 90 days
        self.tenant_id = os.getenv("GHOST_TENANT_ID", "TENANT_DEFAULT")
        self._store = self._load_store()

    def _load_store(self) -> Dict:
        default = {
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "epoch_seconds": self.epoch_seconds,
            "tenants": {}
        }
        if os.path.exists(self.key_store_path) and os.path.getsize(self.key_store_path) > 0:
            try:
                with open(self.key_store_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data
            except Exception:
                return default
        return default

    def _save_store(self) -> None:
        os.makedirs(os.path.dirname(self.key_store_path), exist_ok=True)
        with open(self.key_store_path, "w", encoding="utf-8") as f:
            json.dump(self._store, f, indent=2)

    def _get_tenant_bucket(self, tenant_id: str) -> Dict:
        tenants = self._store.setdefault("tenants", {})
        return tenants.setdefault(tenant_id, {"epochs": {}})

    def _ensure_epoch(self, tenant_id: str, epoch_id: int) -> None:
        bucket = self._get_tenant_bucket(tenant_id)
        epochs = bucket.setdefault("epochs", {})
        if str(epoch_id) in epochs:
            return
        # Create a new random epoch secret
        # (Demo only - use KMS/HSM in prod)
        secret = os.urandom(32).hex()
        epochs[str(epoch_id)] = {
            "secret_hex": secret,
            "starts_at_utc": datetime.now(timezone.utc).isoformat()
        }
        self._save_store()

    def current_epoch_id(self, now_utc: Optional[datetime] = None) -> int:
        # We anchor epoch 1 at Unix epoch for simplicity.
        now = now_utc or datetime.now(timezone.utc)
        seconds_since = int(now.timestamp())
        return (seconds_since // self.epoch_seconds) + 1

    def get_active_epoch(self) -> EpochInfo:
        eid = self.current_epoch_id()
        self._ensure_epoch(self.tenant_id, eid)
        bucket = self._get_tenant_bucket(self.tenant_id)
        meta = bucket["epochs"][str(eid)]
        return EpochInfo(epoch_id=eid, starts_at_utc=meta["starts_at_utc"], active=True)

    def get_epoch_secret(self, epoch_id: int, tenant_id: Optional[str] = None) -> str:
        tid = tenant_id or self.tenant_id
        self._ensure_epoch(tid, epoch_id)
        bucket = self._get_tenant_bucket(tid)
        return bucket["epochs"][str(epoch_id)]["secret_hex"]

    def derive_domain_key(self, domain: str, epoch_id: int, tenant_id: Optional[str] = None) -> bytes:
        """Derive a per-tenant, per-domain key for the given epoch."""
        tid = tenant_id or self.tenant_id
        epoch_secret_hex = self.get_epoch_secret(epoch_id, tid)
        epoch_secret = bytes.fromhex(epoch_secret_hex)
        msg = f"{tid}|{domain}|epoch:{epoch_id}".encode("utf-8")
        # Use HMAC-SHA256 as a simple KDF for the demo.
        return hmac.new(epoch_secret, msg, hashlib.sha256).digest()

    def hmac_token(self, domain: str, value: str, epoch_id: int, tenant_id: Optional[str] = None, length: int = 12) -> Tuple[str, str]:
        """Create a deterministic token suffix and return (suffix, key_id)."""
        key = self.derive_domain_key(domain, epoch_id, tenant_id)
        digest = hmac.new(key, value.encode("utf-8"), hashlib.sha256).hexdigest().upper()
        suffix = digest[:length]
        tid = tenant_id or self.tenant_id
        key_id = f"{tid}:{domain}:E{epoch_id}"
        return suffix, key_id
