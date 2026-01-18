# Project GHOST — Demo Implementation

A minimal, runnable demo of **Project GHOST**: a control-plane pattern for **tokenizing PII before inference** and **rehydrating only under governance**, with a **Sentinel (Jira) loop** for unmapped/hallucinated tokens.

> This repo contains the working Streamlit UI + Vault + Sentinel. It also includes an **upgrade** to deterministic HMAC tokenization with **epoch-based key rotation** (to match the architectural spec).

---

## Figure 1 — Trust-Boundary Workflow (Conceptual)

```mermaid
flowchart LR
    subgraph ZoneA[Zone A — Application/UI]
        UI[Streamlit Control Center\n(app.py)]
    end

    subgraph ZoneB[Zone B — GHOST Control Plane]
        GP[GhostProxy\n(core/ghost/proxy.py)]
        VAULT[GhostVault (Token Registry)\n(core/ghost/vault.py)]
        KEYMGR[EpochKeyManager\n(core/ghost/key_manager.py)]
    end

    subgraph ZoneC[Zone C — Inference Boundary]
        LLM[(LLM / Model Runtime)]
    end

    subgraph ZoneD[Zone D — Governance & Audit]
        JIRA[JiraBridge\n(sentinel/jira_bridge.py)]
        MON[SentinelMonitor\n(sentinel/monitor.py)]
        REG[(registry.json)]
    end

    UI -->|1. raw prompt| GP
    GP -->|2. detect PII & mint tokens| VAULT
    VAULT --> KEYMGR
    VAULT --> REG

    GP -->|3. tokenized prompt| LLM
    LLM -->|4. tokenized response| GP

    GP -->|5. rehydrate known tokens| VAULT
    VAULT --> REG

    GP -->|6a. success -> close| JIRA
    GP -->|6b. unknown token -> incident| JIRA

    MON -->|7. periodic audit + dedupe + close| JIRA
    MON -->|8. checks token validity| VAULT
```

---

## End-to-end workflow (one example)

**User input (contains PII):**

> Draft a notice for **Suresh Krishnan**. His SSN is **123-45-6789**. Email **suresh@example.com**.

### 1) Cloak (before inference)
- `app.py` calls: `GhostProxy.cloak(raw_prompt)`
- `proxy.py` detects PII via regex patterns and calls: `GhostVault.ghost_identity(value, entity_type)`
- `vault.py` mints deterministic tokens (HMAC) using the active epoch key:
  - `PERSON_<hash>`
  - `SSN_<hash>`
  - `EMAIL_ADDRESS_<hash>`

**Tokenized prompt sent to inference (Zone C):**

> Draft a notice for **PERSON_9F2A88F9D2E1**. His SSN is **SSN_A31C88F9D2E1**. Email **EMAIL_ADDRESS_55D2A10B9C2F**.

### 2) Reveal (after inference)
- `app.py` calls: `GhostProxy.reveal(llm_response)`
- `proxy.py` calls: `GhostVault.rehydrate(text)`
- `vault.py` replaces known tokens with the original values (or with a restricted placeholder if blocked)

### 3) Sentinel (governance loop)
- If a token is **still present** after `rehydrate()`, it is treated as **unmapped/hallucinated**.
- `proxy.py` calls: `JiraBridge.handle_rehydration_failure(token_id)`
  - creates or escalates a Jira incident
- Later, when an operator authorizes/restricts the token in the UI, the token becomes valid and:
  - `SentinelMonitor` (background) auto-closes the Jira incident via `auto_close_resolved_issues()`.

---

## Exact code path trace (function calls + sample I/O)

### A) Cloak path
1. `app.py` → `ghost.cloak(user_input)`
2. `core/ghost/proxy.py::GhostProxy.cloak(raw_prompt)`
3. For each PII match:
   - `core/ghost/vault.py::GhostVault.ghost_identity(real_value, entity_type)`
   - `core/ghost/key_manager.py::EpochKeyManager.get_active_epoch()`
   - `core/ghost/key_manager.py::EpochKeyManager.hmac_token(domain, value, epoch_id, tenant_id)`
4. `vault.py` writes mapping to `data/vault/registry.json`
5. `cloak()` returns the fully tokenized prompt

**Input:**
```
Draft a notice for Suresh Krishnan. His SSN is 123-45-6789. Email suresh@example.com.
```

**Output (example):**
```
Draft a notice for PERSON_9F2A88F9D2E1. His SSN is SSN_A31C88F9D2E1. Email EMAIL_ADDRESS_55D2A10B9C2F.
```

### B) Reveal path
1. `app.py` → `ghost.reveal(mock_reply_or_llm_response)`
2. `core/ghost/proxy.py::GhostProxy.reveal(llm_response)`
   - extracts tokens via regex
3. `core/ghost/vault.py::GhostVault.rehydrate(text)`
4. For each token:
   - If token still present after rehydrate → `sentinel/jira_bridge.py::JiraBridge.handle_rehydration_failure(token)`
   - Else → `sentinel/jira_bridge.py::JiraBridge.auto_close_resolved_issues(token)`

**Input:**
```
The Neuro-Mesh processed: Draft a notice for PERSON_9F2A88F9D2E1...
```

**Output:**
```
The Neuro-Mesh processed: Draft a notice for Suresh Krishnan...
```

### C) Hallucinated token example
**LLM returns** a token never minted:
```
... send it to PERSON_ABC999 ...
```
- `rehydrate()` cannot replace it → token remains
- `JiraBridge.handle_rehydration_failure("PERSON_ABC999")` creates/escalates a Jira incident

---

## Deterministic HMAC tokens + epoch rotation

This demo implements **epoch-based key rotation** for minting **new tokens**:
- Old tokens are **never rewritten**.
- When the epoch changes, only the **active minting key** changes.
- Rehydration uses the registry mapping (token → original value), so old tokens remain resolvable.

### Configure epoch duration
Set a short epoch for testing (e.g., 60 seconds):

```bash
export GHOST_EPOCH_SECONDS=60
export GHOST_TENANT_ID=TENANT_DEFAULT
```

**What changes across epochs?**
- If the same SSN appears again in a new epoch, it will mint a **different** token.
- If the value never appears again, **nothing changes** (no swapping).

---

## Run

### Streamlit UI
```bash
streamlit run app.py
```

### Sentinel background monitor (optional)
```bash
python -m sentinel.monitor
```

---

## Repo layout
```
app.py
core/ghost/
  proxy.py
  vault.py
  key_manager.py
  schemas.py
sentinel/
  jira_bridge.py
  monitor.py
data/
  vault/registry.json
  keys/epoch_keys.json
```
