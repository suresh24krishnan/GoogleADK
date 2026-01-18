import os
import json
import time
from jira import JIRA
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class JiraBridge:
    def __init__(self):
        self.server = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.api_token = os.getenv("JIRA_API_TOKEN")
        self.project_key = os.getenv("JIRA_PROJECT_KEY")
        
        # 🛡️ ATOMIC LOCK: Prevents duplicates during the Jira indexing lag
        self.recent_incidents = {} 
        self.last_creation_time = 0
        
        try:
            self.client = JIRA(
                basic_auth=(self.email, self.api_token),
                server=self.server
            )
            print(f"📡 Sentinel: Connected to Jira at {self.server}")
        except Exception as e:
            print(f"⚠️ Sentinel: Jira Connection Failed: {e}")
            self.client = None

    def handle_rehydration_failure(self, token_id):
        """Idempotent handler: creates tickets, self-heals, or escalates [cite: 2026-01-08]."""
        if not self.client: 
            return "Error: Connection Failed", None

        # 1. IMMEDIATE CACHE CHECK (Speed Lock)
        if token_id in self.recent_incidents:
            issue_key = self.recent_incidents[token_id]
            msg = self._escalate_issue(issue_key, token_id, source="Atomic Memory Lock")
            url = f"{self.server}/browse/{issue_key}"
            return msg, url

        # 2. ANTI-RACE CONDITION DELAY
        if time.time() - self.last_creation_time < 2:
            time.sleep(1)

        # 3. JIRA SEARCH (Persistence Lock)
        # Find active tickets where the token is in the summary
        jql = f'project = "{self.project_key}" AND summary ~ "{token_id}" AND statusCategory != "Done" ORDER BY created DESC'
        active_incidents = self.client.search_issues(jql)

        if active_incidents:
            if len(active_incidents) > 1:
                self.cleanup_duplicates(active_incidents)
            
            main_issue = active_incidents[0]
            self.recent_incidents[token_id] = main_issue.key
            msg = self._escalate_issue(main_issue.key, token_id, source="Jira Search Sync")
            url = f"{self.server}/browse/{main_issue.key}"
            return msg, url
        
        # 4. ATOMIC CREATION
        return self._create_incident(token_id)

    def _escalate_issue(self, issue_key, token_id, source="System"):
        """Escalates ticket priority upon repeated leak detection [cite: 2026-01-08]."""
        try:
            print(f"🔼 Sentinel: Escalating {issue_key} (Source: {source})")
            issue = self.client.issue(issue_key)
            # Update priority to High as part of escalation logic [cite: 2026-01-08]
            issue.update(fields={'priority': {'name': 'High'}})
            self.client.add_comment(issue_key, f"🚨 ALERT: Repeated leak of {token_id} detected. Priority bumped.")
            return f"Escalated {issue_key}"
        except Exception as e:
            return f"Escalation Error: {e}"

    def _create_incident(self, token_id):
        """Creates the initial ticket for a detected leak [cite: 2026-01-08]."""
        print(f"🆕 Sentinel: Triggering initial incident for {token_id}")
        try:
            project = self.client.project(self.project_key)
            valid_types = [t.name for t in project.issueTypes if not t.subtask]
            selected_type = next((t for t in ["Incident", "Bug", "Task"] if t in valid_types), valid_types[0])

            all_priorities = [p.name for p in self.client.priorities()]
            selected_priority = next((p for p in ["Medium", "P3", "Major", "Normal"] if p in all_priorities), all_priorities[0])

            issue_dict = {
                'project': {'key': self.project_key},
                'summary': f"Ghost Leak: Unmapped Token {token_id}",
                'description': f"Sentinel detected an unmapped token ({token_id}). Action: Resolve in Vault.",
                'issuetype': {'name': selected_type},
                'priority': {'name': selected_priority}
            }
            
            new_issue = self.client.create_issue(fields=issue_dict)
            self.recent_incidents[token_id] = new_issue.key 
            self.last_creation_time = time.time()
            
            url = f"{self.server}/browse/{new_issue.key}"
            return f"Created {new_issue.key} ({selected_type})", url
            
        except Exception as e:
            return f"Creation Error: {str(e)}", None

    def auto_close_resolved_issues(self, token_id, comment="✨ Sentinel: Resolved."):
        """Self-heals tickets by transitioning them to DONE once resolved [cite: 2026-01-08]."""
        if not self.client or not token_id: return

        # IMPORTANT: Use JQL to find the real Issue Key from the Token ID
        jql = f'project = "{self.project_key}" AND summary ~ "{token_id}" AND statusCategory != "Done"'
        issues = self.client.search_issues(jql)

        if not issues:
            print(f"🔍 Sentinel: No open tickets found for {token_id}")
            return

        for issue in issues:
            try:
                # 1. Add the comment to the REAL Issue Key found
                self.client.add_comment(issue.key, comment)
                
                # 2. Fetch and find the 'Done' transition
                transitions = self.client.transitions(issue)
                target_t = None
                for t in transitions:
                    t_name = t['name'].lower()
                    t_id = str(t['id'])
                    
                    if t_id == "9036" or any(x in t_name for x in ["done", "resolve", "close", "complete"]):
                        target_t = t
                        break

                if target_t:
                    self.client.transition_issue(issue, target_t['id'])
                    print(f"✅ Sentinel: {issue.key} moved to {target_t['name']} (Reason: {comment})")
                    # Clear from memory lock if closed
                    if token_id in self.recent_incidents:
                        del self.recent_incidents[token_id]
                else:
                    print(f"⚠️ Sentinel: Could not find closure transition for {issue.key}")
                    
            except Exception as e:
                print(f"❌ Jira Transition Error: {e}")

    def cleanup_duplicates(self, issue_list):
        """Links and closes duplicate tickets to maintain board hygiene [cite: 2026-01-08]."""
        master_issue = issue_list[0]
        for dup in issue_list[1:]:
            try:
                self.client.create_issue_link("Duplicate", master_issue.key, dup.key)
                self.client.add_comment(dup.key, f"🚫 Duplicate. Closed in favor of {master_issue.key}.")
                
                transitions = self.client.transitions(dup)
                target = next((t for t in transitions if any(x in t['name'].lower() for x in ["done", "resolve", "close"])), None)
                if target:
                    self.client.transition_issue(dup, target['id'])
            except Exception as e:
                print(f"⚠️ Duplicate Cleanup Failed: {e}")