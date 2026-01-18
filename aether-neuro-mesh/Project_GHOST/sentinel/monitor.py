import time
import os
import re
from sentinel.jira_bridge import JiraBridge
from core.ghost.vault import GhostVault

class SentinelMonitor:
    def __init__(self, check_interval=30):
        # The bridge and vault act as the source of truth for the audit loop
        self.bridge = JiraBridge()
        self.vault = GhostVault()
        self.check_interval = check_interval 
        self.project_key = os.getenv("JIRA_PROJECT_KEY", "SEN")
        
        # Updated Regex: Matches [TYPE]_[6 HEX CHARS] e.g., PERSON_F4D7AF
        # This now matches the dynamic tokens generated in vault.py
        self.token_pattern = r'[A-Z]+_[A-Z0-9]+'

    def run_audit_loop(self):
        """Main background loop that maintains system health [cite: 2026-01-08]."""
        print(f"🚀 Sentinel Monitor Active | Project: {self.project_key}")
        print(f"📡 Heartbeat: {self.check_interval}s | Logic: Self-Healing + Deduplication")
        print("-" * 60)

        while True:
            try:
                self.audit_and_remediate()
            except Exception as e:
                print(f"⚠️ Monitor Loop Error: {e}")
            
            time.sleep(self.check_interval)

    def audit_and_remediate(self):
        """Scans, Deduplicates, and Heals PII leak incidents autonomously."""
        if not self.bridge.client:
            print("❌ Monitor: No Jira Connection.")
            return

        # 1. FETCH ALL UNRESOLVED INCIDENTS
        # We look for anything NOT Done to see if it can be 'Healed'
        jql = f'project = "{self.project_key}" AND summary ~ "Ghost Leak" AND statusCategory != "Done" ORDER BY created ASC'
        open_issues = self.bridge.client.search_issues(jql)

        if not open_issues:
            print(f"[{time.strftime('%H:%M:%S')}] ✅ System Healthy: No active leaks.")
            return

        print(f"[{time.strftime('%H:%M:%S')}] 🔍 Auditing {len(open_issues)} incidents...")

        # 2. GROUP BY TOKEN
        token_groups = {}
        for issue in open_issues:
            # We search the summary for the token ID
            match = re.search(self.token_pattern, issue.fields.summary)
            if match:
                tid = match.group()
                if tid not in token_groups:
                    token_groups[tid] = []
                token_groups[tid].append(issue)

        # 3. ENFORCE GOVERNANCE POLICIES
        for tid, issues in token_groups.items():
            # POLICY A: Deduplication [cite: 2026-01-08]
            # If a human or a bug created multiple tickets for the same leak, kill the extras.
            if len(issues) > 1:
                print(f"🔗 Sentinel: Found {len(issues)} duplicates for {tid}. Merging...")
                self.bridge.cleanup_duplicates(issues)
            
            master_issue = issues[0]

            # POLICY B: Self-Healing [cite: 2026-01-08]
            # The heart of the system: If the Vault now knows this token, close the ticket.
            if self.vault.is_token_valid(tid):
                print(f"✨ Self-Healing: {tid} is now authorized. Closing {master_issue.key}...")
                self.bridge.auto_close_resolved_issues(
                    tid, 
                    comment="🛰️ Monitor: Background Sync detected resolution in Vault. Closing incident."
                )
            else:
                # POLICY C: Audit Heartbeat
                # If it's still unmapped, leave a 'still watching' comment.
                try:
                    self.bridge.client.add_comment(
                        master_issue.key, 
                        f"Sentinel Heartbeat [{time.strftime('%H:%M:%S')}]: Token still unmapped. Governance required."
                    )
                except:
                    pass

if __name__ == "__main__":
    monitor = SentinelMonitor(check_interval=30) 
    monitor.run_audit_loop()