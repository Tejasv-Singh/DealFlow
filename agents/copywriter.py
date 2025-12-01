from .utils import get_llm_response
from ..db.db_manager import DBManager

class CopywriterAgent:
    def __init__(self, db: DBManager):
        self.db = db

    def generate_outreach(self, sponsor_id: int, company_name: str, research_content: str):
        print(f"[CopywriterAgent] Generating email for {company_name}...")
        
        prompt = f"Write a sponsorship outreach email for {company_name} based on this research: {research_content}"
        email_content = get_llm_response(prompt, system_prompt="You are a professional copywriter.")
        
        # In a real app, we might save this as a draft.
        # For now, we'll just log it and maybe simulate sending or saving to a 'drafts' table.
        # We'll save it to email_threads as a draft.
        
        # self.db.save_draft(sponsor_id, email_content) # We don't have this method yet.
        
        self.db.log_event(sponsor_id, "CopywriterAgent", "Draft Created", "Email draft generated.")
        return email_content
