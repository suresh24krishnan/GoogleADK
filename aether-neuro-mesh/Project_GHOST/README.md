# Project GHOST — Demo Implementation

A high-fidelity reference implementation of Project GHOST: an enterprise-grade control-plane for deterministic PII tokenization and autonomous Sentinel governance.

> **Security Invariant:** No architectural path exists for raw identity data to enter the inference execution environment. Trust is enforced at the network mediation layer.

---

## Figure 1 — Control Plane Logical Zoning

![Project GHOST Architecture](./docs_Figure1.png)

*Figure 1: Visual representation of the GHOST Control Plane, illustrating the strict boundary between the Trusted App Domain (Zone A), the Governance Core (Zone B), and the Blind Inference Zone (Zone C).*

---

## The Ghosting Workflow: A Practical Example

**User Input (Raw PII):**
> "Draft a notice for **Suresh Krishnan**. His SSN is **123-45-6789**. Email **suresh@example.com**."

### 1. The Cloak (Pre-Inference)
The `GhostProxy` intercepts the prompt. The engine performs **precedence-aware regex detection**, ensuring high-risk patterns like SSNs are ghosted before general numbers.

- **Action:** `GhostVault.ghost_identity()` invokes the `EpochKeyManager`.
- **Logic:** Generates a deterministic **HMAC-SHA256** token.
- **Output (Sent to LLM):**
  > "Draft a notice for **PERSON_9F2A88F9D2E1**. His SSN is **SSN_A31C88F9D2E1**. Email **EMAIL_ADDRESS_55D2A10B9C2F**."

### 2. The Reveal (Post-Inference)
The LLM processes the request using the "Ghosted" personas. When the response returns:
- **Action:** `GhostProxy.reveal()` triggers `GhostVault.rehydrate()`.
- **Result:** Tokens are mapped back to original values using the secure, append-only registry.

### 3. Sentinel Governance (Self-Healing Loop)
If the LLM fabricates a token (hallucination) or if an unauthorized token is detected:
- **Escalation:** `JiraBridge` creates a high-priority incident.
- **Self-Healing:** Upon manual or programmatic authorization, the `SentinelMonitor` detects the resolution and **automatically closes the Jira ticket**, reducing SRE toil by >80%.

---

## Core Technical Features

### Epoch-Based Key Rotation
To meet Tier-0 security standards, this demo implements **Temporal Key Isolation**:
- New tokens are minted using the **Active Epoch Key**.
- Historical tokens remain resolvable via the registry, ensuring backward compatibility without re-exposing data.
- **Config:** Set `export GHOST_EPOCH_SECONDS=3600` to define rotation frequency.

### Deterministic Integrity
Because tokens are deterministic, the same identity results in the same "Ghost" across multiple distributed sessions, allowing AI agents to maintain referential context (e.g., knowing that `PERSON_A` in Session 1 is the same as `PERSON_A` in Session 5) without ever knowing the user's name.

---

## Quick Start

### 1. Launch the UI
```bash
streamlit run app.py
2. Start the Sentinel Monitor
Bash

python -m sentinel.monitor
Repository Structure
Plaintext

Project_GHOST/
├─ app.py                # Streamlit Entry Point
├─ core/ghost/
│  ├─ proxy.py           # Interception & Precedence Logic
│  ├─ vault.py           # HMAC Tokenization & Rehydration
│  └─ key_manager.py     # Epoch-based Key Rotation
├─ sentinel/
│  ├─ jira_bridge.py     # Ticket Lifecycle Management
│  └─ monitor.py         # Autonomous SRE Monitor
├─ data/
│  ├─ vault/             # Append-Only Registries
│  └─ keys/              # Secured Epoch Keys
└─ docs_Figure1.png      # Control Plane Diagram (Clean_v2)
---

**Architect of Record:** Suresh Krishnan  
**Classification:** Tier-0 Strategic Asset / Enterprise AI Infrastructure

