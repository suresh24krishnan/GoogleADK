import json
import os
import re
from datetime import datetime
from typing import Dict

from .schemas import ShadowToken
from .key_manager import EpochKeyManager


def _normalize_value(value: str) -> str:
    # Trim and collapse internal whitespace so "Suresh  Krishnan" and "Suresh Krishnan " map consistently.
    return re.sub(r"\s+", " ", value).strip()


class GhostVault:
    def __init__(self, registry_path: str = "data/vault/registry.json"):
        self.registry_path = registry_path
        self.registry = self._load_registry()

        self.keys = EpochKeyManager()  # demo-safe key manager
        self.tenant_id = os.getenv("GHOST_TENANT_ID", "TENANT_DEFAULT")

    @property
    def mappings(self) -> Dict:
        """Exposes the internal shadow_to_real registry for the Streamlit UI."""
        return self.registry.get("shadow_to_real", {})

    def _load_registry(self) -> Dict:
        """Safely loads the vault. Initializes if file is missing or empty."""
        default_structure = {"real_to_shadow": {}, "shadow_to_real": {}}

        if os.path.exists(self.registry_path):
            try:
                if os.path.getsize(self.registry_path) > 0:
                    with open(self.registry_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        # Backward compatibility: ensure expected keys exist.
                        data.setdefault("real_to_shadow", {})
                        data.setdefault("shadow_to_real", {})
                        return data
            except (json.JSONDecodeError, IOError):
                print(f"⚠️ Vault at {self.registry_path} was corrupted. Using default.")

        return default_structure

    def refresh(self) -> None:
        """Reloads the registry from disk to pick up changes from UI (Authorize/Restrict)."""
        self.registry = self._load_registry()

    def ghost_identity(self, real_value: str, entity_type: str = "ID") -> str:
        """Creates a deterministic shadow token (HMAC-SHA256) scoped by epoch.

        - Tokens minted in different epochs will differ for the same value.
        - Existing tokens are never rewritten; old tokens remain resolvable via registry.
        """
        normalized = _normalize_value(real_value)

        # Determine active epoch
        epoch = self.keys.get_active_epoch()
        epoch_id = epoch.epoch_id

        # Use composite key for real_to_shadow so the same value can mint a new token in a new epoch.
        real_key = f"{self.tenant_id}|{entity_type}|E{epoch_id}|{normalized}"
        existing = self.registry.get("real_to_shadow", {}).get(real_key)
        if existing and existing in self.registry.get("shadow_to_real", {}):
            return existing

        # Deterministic suffix (12 hex chars by default)
        suffix, key_id = self.keys.hmac_token(domain=entity_type, value=normalized, epoch_id=epoch_id, tenant_id=self.tenant_id, length=12)
        token_id = f"{entity_type}_{suffix}"

        # Handle ultra-rare collisions: if token already exists for a different value, extend length.
        shadow = self.registry.get("shadow_to_real", {}).get(token_id)
        if shadow and isinstance(shadow, dict) and shadow.get("original_value") != normalized:
            suffix, key_id = self.keys.hmac_token(domain=entity_type, value=normalized, epoch_id=epoch_id, tenant_id=self.tenant_id, length=16)
            token_id = f"{entity_type}_{suffix}"

        token_data = ShadowToken(
            token_id=token_id,
            category=entity_type,
            original_value=normalized,
            tenant_id=self.tenant_id,
            epoch_id=epoch_id,
            key_id=key_id,
            is_authorized=True,
            is_restricted=False,
        )

        self.registry["shadow_to_real"][token_id] = token_data.model_dump()
        self.registry["real_to_shadow"][real_key] = token_id

        self._save_registry()
        return token_id

    def rehydrate(self, text: str) -> str:
        """Replaces tokens in LLM responses with original values from the vault.

        Governance behavior:
        - If a token is restricted, replace with its stored placeholder (e.g., "🚫 [RESTRICTED]").
        """
        self.refresh()

        # Sort by length descending to prevent partial matches
        sorted_tokens = sorted(self.registry["shadow_to_real"].items(), key=lambda x: len(x[0]), reverse=True)

        for token_id, data in sorted_tokens:
            if isinstance(data, dict):
                real_val = data.get("original_value", token_id)
                # If restricted, we still replace (but never reveal raw value).
                if data.get("is_restricted") is True:
                    real_val = data.get("original_value", "🚫 [RESTRICTED]")
            else:
                real_val = data

            text = text.replace(token_id, real_val)
        return text

    def is_token_valid(self, token_id: str) -> bool:
        """Used by Sentinel to check if a token has a known mapping."""
        self.refresh()
        return token_id in self.registry.get("shadow_to_real", {})

    def add_mapping(self, real_value: str, token_id: str) -> None:
        """Link a hallucinated token to a real value or a restriction marker.

        - If real_value contains "RESTRICTED", token will be marked restricted.
        - This does *not* mint new tokens; it authorizes/blocks an existing token.
        """
        normalized = _normalize_value(real_value)
        is_restricted = "RESTRICTED" in normalized

        # Keep existing metadata if present
        existing = self.registry.get("shadow_to_real", {}).get(token_id, {})
        category = existing.get("category") or (token_id.split("_")[0] if "_" in token_id else "UNKNOWN")

        self.registry["shadow_to_real"][token_id] = {
            "token_id": token_id,
            "category": category,
            "original_value": normalized,
            "tenant_id": existing.get("tenant_id", self.tenant_id),
            "epoch_id": existing.get("epoch_id", 0),
            "key_id": existing.get("key_id"),
            "is_authorized": not is_restricted,
            "is_restricted": is_restricted,
            "created_at": existing.get("created_at", datetime.now().isoformat()),
        }

        # Store a composite real_to_shadow key for future lookup (best-effort)
        real_key = f"{self.tenant_id}|{category}|E{existing.get('epoch_id', 0)}|{normalized}"
        self.registry["real_to_shadow"][real_key] = token_id
        self._save_registry()

    def clear(self) -> None:
        """Wipes all mappings (demo reset)."""
        self.registry = {"real_to_shadow": {}, "shadow_to_real": {}}
        self._save_registry()

    def _save_registry(self) -> None:
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self.registry, f, indent=4)
        except IOError as e:
            print(f"❌ Failed to save vault: {e}")
