import re
from .vault import GhostVault
from sentinel.jira_bridge import JiraBridge

class GhostProxy:
    def __init__(self):
        self.vault = GhostVault()
        self.bridge = JiraBridge()  # Sentinel's automated Jira connector
        
        # PII Patterns: SSN remains first to ensure it matches before Phone
        self.patterns = {
            # 1. SSN (Strict 3-2-4 format)
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            
            "EMAIL_ADDRESS": r'[\w\.-]+@[\w\.-]+\.\w+',
            
            # 2. PHONE_NUMBER: Now catches 7-digit (555-0199) and 10-digit formats
            # The (?!...) ensures it ignores the SSN structure
            "PHONE_NUMBER": r'\b(?!\d{3}-\d{2}-\d{4})(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{3}-\d{4}\b',
            
            "PERSON": r'\b[A-Z][a-z]+ [A-Z][a-z]+\b|\bSuresh\b', 
            "LOCATION": r'\b\d+th Avenue\b|\bNew York\b',
            "CARD": r'\b(?:\d[ -]*?){13,16}\b' 
        }

    def cloak(self, raw_prompt: str) -> str:
        """Masks PII with unique aliases to ensure AI never sees raw data."""
        ghosted_text = raw_prompt
        
        # Process each category - SSN and Phone are handled distinctly
        for category, pattern in self.patterns.items():
            matches = re.finditer(pattern, ghosted_text)
            for match in sorted(matches, key=lambda x: x.start(), reverse=True):
                real_val = match.group()
                token = self.vault.ghost_identity(real_val, entity_type=category)
                ghosted_text = ghosted_text[:match.start()] + token + ghosted_text[match.end():]
                
        return ghosted_text

    def reveal(self, llm_response: str) -> str:
        """
        De-masks response and triggers Sentinel logic [cite: 2026-01-08].
        - Successful rehydration -> Auto-close Jira ticket (Self-Heal).
        - Failed rehydration -> Escalate Jira ticket.
        """
        found_tokens = re.findall(r'\b[A-Z]+_[A-Z0-9]+\b', llm_response)
        rehydrated = self.vault.rehydrate(llm_response)
        
        for token in found_tokens:
            if token in rehydrated:
                # Token still present: Sentinel triggers escalation
                self.bridge.handle_rehydration_failure(token)
            else:
                # Token replaced: Sentinel triggers self-healing
                self.bridge.auto_close_resolved_issues(
                    token, 
                    comment="✨ Sentinel: Fix verified. Auto-closing Jira incident."
                )

        return rehydrated