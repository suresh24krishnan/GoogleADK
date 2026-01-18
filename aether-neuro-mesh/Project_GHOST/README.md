
````md
## Figure 1 — Trust-Boundary Workflow (Conceptual)

```mermaid
flowchart LR
  %% =========================
  %% Zones / Trust Boundaries
  %% =========================
  subgraph ZA["Zone A — Application / UI"]
    UI["Streamlit UI\n(app.py)"]
  end

  subgraph ZB["Zone B — GHOST Control Plane"]
    GP["GhostProxy\ncloak() / reveal()\n(core/ghost/proxy.py)"]
    VAULT["GhostVault\nToken Registry\n(core/ghost/vault.py)"]
    KEYMGR["EpochKeyManager\nKey Derivation + Rotation\n(core/ghost/key_manager.py)"]
  end

  subgraph ZC["Zone C — LLM Inference Boundary"]
    LLM["LLM Runtime\n(Tokens Only)"]
  end

  subgraph ZD["Zone D — Sentinel & Governance"]
    JIRA["JiraBridge\n(sentinel/jira_bridge.py)"]
    MON["SentinelMonitor\n(sentinel/monitor.py)"]
    REG["registry.json\n(token → value, policy, status)"]
  end

  %% =========================
  %% Primary Data Flow
  %% =========================
  UI -->|1) Raw prompt (may contain PII)| GP
  GP -->|2) Detect PII + mint tokens| VAULT
  VAULT -->|Derive active epoch key| KEYMGR
  VAULT -->|Write mappings / policy state| REG

  GP -->|3) Tokenized prompt| LLM
  LLM -->|4) Tokenized response| GP

  %% =========================
  %% Rehydration + Governance
  %% =========================
  GP -->|5) Rehydrate known tokens| VAULT
  VAULT -->|Lookup tokens + policy| REG

  GP -->|6a) All tokens resolved → close| JIRA
  GP -->|6b) Unknown/hallucinated token → incident| JIRA

  MON -->|7) Periodic audit / dedupe / auto-close| JIRA
  MON -->|8) Verify token state| VAULT

  %% =========================
  %% Visual styling (optional)
  %% =========================
  classDef zoneA fill:#E8F1FF,stroke:#3B82F6,color:#111827;
  classDef zoneB fill:#E9FCEB,stroke:#22C55E,color:#111827;
  classDef zoneC fill:#FFF7E6,stroke:#F59E0B,color:#111827;
  classDef zoneD fill:#FFECEC,stroke:#EF4444,color:#111827;

  class UI zoneA;
  class GP,VAULT,KEYMGR zoneB;
  class LLM zoneC;
  class JIRA,MON,REG zoneD;
````

````

---

## Notes (so you don’t get tripped again)
- Mermaid rendering depends on GitHub’s markdown renderer. It will **not** render in some contexts (like raw view), but it **will** render on the normal file view.
- Make sure the code fence is **exactly** ` ```mermaid ` (no extra spaces).

---

## Next steps
1) Paste the section above into `Project_GHOST/README.md`
2) Commit + push:

```powershell
git add README.md
git commit -m "Replace Figure 1 PNG with Mermaid diagram"
git push
````
