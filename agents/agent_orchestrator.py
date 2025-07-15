from agents.audio_agent import generate_audio_from_text, generate_text_from_audio
from agents.web_scraping_agent import generate_scrape_from_url
from agents.search_agent import search_internet

class AgentOrchestrator:
    def __init__(self):
        self.audio_to_text = generate_text_from_audio
        self.text_to_audio = generate_audio_from_text
        self.web_scrape = generate_scrape_from_url
        self.search = search_internet

    def process_audio_query(self, audio_file: str):
        """
        Main entry: User asks a question via audio.
        1. Transcribe audio to text.
        2. Search internet for top 3 results.
        3. Scrape each result, return first successful scrape.
        """
        query = self.audio_to_text(audio_file)
        search_results = self.search(query)
        for result in search_results:
            url = result['url'] if isinstance(result, dict) and 'url' in result else result
            scraped = self.web_scrape(url)
            if scraped and 'Failed to scrape' not in scraped:
                return {
                    'query': query,
                    'search_url': url,
                    'scraped_content': scraped
                }
        return {
            'query': query,
            'search_url': None,
            'scraped_content': 'No successful scrape from top 3 results.'
        }

    def followup_audio(self, audio_file: str, context: dict):
        """
        User asks a follow-up via audio. Uses previous context.
        """
        followup = self.audio_to_text(audio_file)
        # Optionally, you can re-search or just answer from context
        return {
            'followup': followup,
            'context': context
        }
