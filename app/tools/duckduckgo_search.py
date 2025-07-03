"""
Free DuckDuckGo Search Tool for Agno Framework
Alternative to paid Google Search APIs
"""

try:
    import requests
except ImportError:
    requests = None

import json
import time
from typing import List, Dict, Any, Optional
from urllib.parse import quote_plus
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DuckDuckGoSearchTool:
    """
    Free DuckDuckGo search tool for finding drug and medical information
    Uses DuckDuckGo's instant answers and HTML search
    """
    
    def __init__(self, max_results: int = 5, delay: float = 1.0):
        """
        Initialize DuckDuckGo search tool
        
        Args:
            max_results: Maximum number of search results to return
            delay: Delay between requests to be respectful to the service
        """
        if requests is None:
            raise ImportError("The 'requests' library is required for search functionality. Install it with: pip install requests")
            
        self.max_results = max_results
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search_instant_answers(self, query: str) -> Dict[str, Any]:
        """
        Search DuckDuckGo instant answers API for drug information
        Good for getting basic drug information and definitions
        """
        try:
            encoded_query = quote_plus(query)
            url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            result = {
                'query': query,
                'abstract': data.get('Abstract', ''),
                'abstract_source': data.get('AbstractSource', ''),
                'abstract_url': data.get('AbstractURL', ''),
                'definition': data.get('Definition', ''),
                'definition_source': data.get('DefinitionSource', ''),
                'definition_url': data.get('DefinitionURL', ''),
                'answer': data.get('Answer', ''),
                'answer_type': data.get('AnswerType', ''),
                'infobox': data.get('Infobox', {}),
                'related_topics': [topic.get('Text', '') for topic in data.get('RelatedTopics', [])[:3]]
            }
            
            logger.info(f"DuckDuckGo instant answers search successful for: {query}")
            return result
            
        except Exception as e:
            logger.error(f"Error in instant answers search for '{query}': {e}")
            return {'query': query, 'error': str(e)}
    
    def search_web_results(self, query: str) -> List[Dict[str, Any]]:
        """
        Search DuckDuckGo for web results
        Uses HTML scraping approach as fallback
        """
        try:
            # Add medical/drug specific terms to improve relevance
            if any(term in query.lower() for term in ['drug', 'medication', 'interaction', 'pharmacy']):
                enhanced_query = f"{query} drug interaction pharmaceutical FDA"
            else:
                enhanced_query = query
            
            encoded_query = quote_plus(enhanced_query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Simple HTML parsing for key information
            content = response.text
            results = []
            
            # Look for drug databases and medical sources
            medical_sources = [
                'drugs.com', 'rxlist.com', 'webmd.com', 'mayoclinic.org', 
                'medlineplus.gov', 'nih.gov', 'fda.gov', 'ncbi.nlm.nih.gov'
            ]
            
            # Extract basic information (simplified approach)
            import re
            
            # Find titles and URLs
            title_pattern = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>([^<]*)</a>'
            snippet_pattern = r'<a[^>]*class="result__snippet"[^>]*>([^<]*)</a>'
            
            titles = re.findall(title_pattern, content)
            snippets = re.findall(snippet_pattern, content)
            
            for i, (url, title) in enumerate(titles[:self.max_results]):
                snippet = snippets[i] if i < len(snippets) else ""
                
                # Prioritize medical sources
                is_medical_source = any(source in url.lower() for source in medical_sources)
                
                results.append({
                    'title': title.strip(),
                    'url': url,
                    'snippet': snippet.strip(),
                    'is_medical_source': is_medical_source,
                    'relevance_score': 10 if is_medical_source else 5
                })
            
            # Sort by relevance (medical sources first)
            results.sort(key=lambda x: x['relevance_score'], reverse=True)
            
            logger.info(f"DuckDuckGo web search successful for: {query}, found {len(results)} results")
            return results[:self.max_results]
            
        except Exception as e:
            logger.error(f"Error in web search for '{query}': {e}")
            return [{'query': query, 'error': str(e)}]
    
    def search_drug_information(self, drug_name: str) -> Dict[str, Any]:
        """
        Comprehensive drug information search combining multiple approaches
        """
        time.sleep(self.delay)  # Rate limiting
        
        # Search for basic drug information
        basic_query = f"{drug_name} drug medication"
        instant_results = self.search_instant_answers(basic_query)
        
        time.sleep(self.delay)
        
        # Search for interaction information
        interaction_query = f"{drug_name} drug interactions side effects"
        web_results = self.search_web_results(interaction_query)
        
        time.sleep(self.delay)
        
        # Search for FDA information
        fda_query = f"{drug_name} FDA approved drug information"
        fda_results = self.search_web_results(fda_query)
        
        # Combine results
        combined_results = {
            'drug_name': drug_name,
            'instant_answers': instant_results,
            'interaction_sources': web_results,
            'fda_sources': fda_results,
            'search_timestamp': time.time()
        }
        
        return combined_results
    
    def search_drug_interactions(self, drug1: str, drug2: str) -> Dict[str, Any]:
        """
        Search for specific drug-drug interactions
        """
        time.sleep(self.delay)
        
        # Multiple search strategies
        queries = [
            f"{drug1} {drug2} drug interaction",
            f"{drug1} interact with {drug2}",
            f"interaction between {drug1} and {drug2}",
            f"{drug1} {drug2} contraindication"
        ]
        
        all_results = []
        
        for query in queries[:2]:  # Limit to 2 queries to avoid rate limiting
            web_results = self.search_web_results(query)
            all_results.extend(web_results)
            time.sleep(self.delay)
        
        # Remove duplicates and prioritize medical sources
        unique_results = []
        seen_urls = set()
        
        for result in all_results:
            if result.get('url') not in seen_urls:
                unique_results.append(result)
                seen_urls.add(result.get('url', ''))
        
        return {
            'drug_pair': f"{drug1} + {drug2}",
            'interaction_results': unique_results[:self.max_results],
            'search_timestamp': time.time()
        }


# Agno Tool Integration Class
class FreeDrugSearchTool:
    """
    Agno-compatible tool for drug information search using DuckDuckGo
    """
    
    def __init__(self, max_results: int = 5):
        try:
            self.search_engine = DuckDuckGoSearchTool(max_results=max_results)
            self.search_available = True
        except ImportError as e:
            logger.warning(f"Search functionality disabled: {e}")
            self.search_engine = None
            self.search_available = False
            
        self.name = "drug_search"
        self.description = "Search for drug information, interactions, and safety data using free sources"
    
    def search_drug_info(self, drug_name: str) -> str:
        """Search for comprehensive drug information"""
        if not self.search_available:
            return f"# Drug Information: {drug_name}\n\nSearch functionality unavailable. Please install the 'requests' library to enable search.\n"
            
        try:
            results = self.search_engine.search_drug_information(drug_name)
            
            # Format results for agent consumption
            formatted_results = f"# Drug Information: {drug_name}\n\n"
            
            # Add instant answers
            instant = results.get('instant_answers', {})
            if instant.get('abstract'):
                formatted_results += f"## Overview\n{instant['abstract']}\n\n"
            if instant.get('definition'):
                formatted_results += f"## Definition\n{instant['definition']}\n\n"
            
            # Add interaction sources
            interaction_sources = results.get('interaction_sources', [])
            if interaction_sources:
                formatted_results += "## Interaction Information Sources\n"
                for source in interaction_sources[:3]:
                    if 'error' not in source:
                        formatted_results += f"- **{source.get('title', 'N/A')}**\n"
                        formatted_results += f"  {source.get('snippet', 'No snippet available')}\n"
                        formatted_results += f"  Source: {source.get('url', 'N/A')}\n\n"
            
            # Add FDA sources
            fda_sources = results.get('fda_sources', [])
            if fda_sources:
                formatted_results += "## Official/FDA Sources\n"
                for source in fda_sources[:2]:
                    if 'error' not in source and source.get('is_medical_source'):
                        formatted_results += f"- **{source.get('title', 'N/A')}**\n"
                        formatted_results += f"  {source.get('snippet', 'No snippet available')}\n"
                        formatted_results += f"  Source: {source.get('url', 'N/A')}\n\n"
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in drug info search: {e}")
            return f"Error searching for drug information: {str(e)}"
    
    def search_drug_interactions(self, drug1: str, drug2: str) -> str:
        """Search for drug-drug interactions"""
        if not self.search_available:
            return f"# Drug Interaction Search: {drug1} + {drug2}\n\nSearch functionality unavailable. Please install the 'requests' library to enable search.\n"
            
        try:
            results = self.search_engine.search_drug_interactions(drug1, drug2)
            
            formatted_results = f"# Drug Interaction Search: {drug1} + {drug2}\n\n"
            
            interaction_results = results.get('interaction_results', [])
            if interaction_results:
                formatted_results += "## Interaction Information Found\n"
                for i, result in enumerate(interaction_results[:5], 1):
                    if 'error' not in result:
                        formatted_results += f"### Source {i}\n"
                        formatted_results += f"**Title:** {result.get('title', 'N/A')}\n"
                        formatted_results += f"**Summary:** {result.get('snippet', 'No summary available')}\n"
                        formatted_results += f"**URL:** {result.get('url', 'N/A')}\n"
                        formatted_results += f"**Medical Source:** {'Yes' if result.get('is_medical_source') else 'No'}\n\n"
            else:
                formatted_results += "No specific interaction information found in search results.\n"
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in drug interaction search: {e}")
            return f"Error searching for drug interactions: {str(e)}"
    
    def search_general(self, query: str) -> str:
        """General search functionality"""
        try:
            # Determine if this is a drug-related query
            if any(term in query.lower() for term in ['drug', 'medication', 'interact', 'side effect']):
                web_results = self.search_engine.search_web_results(query)
                
                formatted_results = f"# Search Results: {query}\n\n"
                for i, result in enumerate(web_results[:3], 1):
                    if 'error' not in result:
                        formatted_results += f"## Result {i}\n"
                        formatted_results += f"**Title:** {result.get('title', 'N/A')}\n"
                        formatted_results += f"**Summary:** {result.get('snippet', 'No summary available')}\n"
                        formatted_results += f"**URL:** {result.get('url', 'N/A')}\n\n"
                
                return formatted_results
            else:
                return "This search tool is optimized for drug and medical information. Please use drug-related search terms."
                
        except Exception as e:
            logger.error(f"Error in general search: {e}")
            return f"Error in search: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    # Test the tool
    tool = FreeDrugSearchTool()
    
    print("Testing drug information search...")
    result = tool.search_drug_info("aspirin")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    print("Testing drug interaction search...")
    result = tool.search_drug_interactions("warfarin", "aspirin")
    print(result)
