from .utils import get_llm_response
from ..db.db_manager import DBManager

class ResearchAgent:
    def __init__(self, db: DBManager):
        self.db = db

    def research_sponsor(self, sponsor_id: int, company_name: str, website: str):
        print(f"[ResearchAgent] Starting research on {company_name}...")
        
        # Scrape website
        scraped_text = ""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            # Ensure protocol
            if not website.startswith('http'):
                website = 'https://' + website
                
            print(f"Scraping {website}...")
            resp = requests.get(website, timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                # Get text from paragraphs
                paragraphs = soup.find_all('p')
                scraped_text = " ".join([p.get_text() for p in paragraphs])[:5000] # Limit context
                print(f"Scraped {len(scraped_text)} chars.")
            else:
                print(f"Failed to scrape: Status {resp.status_code}")
        except Exception as e:
            print(f"Scraping error: {e}")
        
        # Prompt with real data
        context = f"Website Content: {scraped_text}" if scraped_text else "Website could not be scraped."
        prompt = f"""
        Research the company {company_name} at {website}. 
        {context}
        
        Goal: Find a Point of Contact (POC) for sponsorship or partnership.
        Look for:
        1. Marketing/DevRel Lead Name
        2. Contact Email (prioritize specific people, fallback to generic)
        3. Recent News/Context
        
        Output format:
        POC Name: [Name]
        POC Email: [Email]
        Context: [Summary]
        """
        
        research_content = get_llm_response(prompt, system_prompt="You are a senior tech researcher. Your goal is to find contact info.")
        
        # Try to extract email from research content to update DB
        import re
        email_match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', research_content)
        if email_match:
            email = email_match.group(0)
            print(f"Found potential email: {email}")
            # Update sponsor email in DB
            conn = self.db._get_conn()
            conn.execute("UPDATE sponsors SET contact_email = ? WHERE id = ?", (email, sponsor_id))
            conn.commit()
            conn.close()
        
        # Save artifact
        self.db.add_research_artifact(sponsor_id, research_content)
        
        # Update status
        self.db.update_sponsor_status(sponsor_id, "Researching") # Actually it should be done, so maybe "Researched" or keep "Researching" until next step?
        # The pipeline says: Research complete -> hire Copywriter.
        # So maybe we update to a status that triggers Copywriter, or CampaignManager handles the transition.
        # Let's say we update to "Researched" or just keep it simple.
        # The columns are: Identified, Researching, Contacted...
        # So "Researching" is the active state. Once done, maybe it stays in Researching until Copywriter picks it up?
        # Or we move it to a ready state.
        # Let's assume the CampaignManager sees that an artifact exists and moves it to the next step.
        
        self.db.log_event(sponsor_id, "ResearchAgent", "Research Complete", f"Found: {research_content[:30]}...")
        return research_content
