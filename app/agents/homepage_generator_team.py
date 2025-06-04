"""
Homepage Content Generator Agent Team System

This module implements a team-based system for automatically generating website homepage content
using a coordinated team of specialized AI agents based on JSON mapping configuration.

The system follows these steps:
1. Crawl a target website to extract content and analyze its structure
2. Develop content strategy based on the website's purpose and audience
3. Generate specialized content for each homepage section using dedicated agents
4. Optimize content for SEO and conversions
5. Assemble the final document with proper structure and formatting
6. Export the document in the requested format (markdown or HTML)
"""

from typing import Dict, List, Optional, Any, Iterator, Tuple
import json
import os
import asyncio
import requests
from pathlib import Path
from bs4 import BeautifulSoup

from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.utils.pprint import pprint_run_response
from agno.storage.sqlite import SqliteStorage
from app.core import settings


class HomepageGeneratorAgentTeam:
    """
    Team-based agent system for generating comprehensive website homepage content
    using specialized agents for different aspects of content creation.
    """
    
    def __init__(self):
        """Initialize the homepage generator agent team system."""
        self.AGENT_STORAGE = settings.AGENT_STORAGE
        self._load_mapping()
        self._setup_agent_team()
        
    def _load_mapping(self):
        """Load the homepage mapping JSON file."""
        mapping_path = Path(__file__).parent / "home_page_mapping.json"
        
        with open(mapping_path, 'r') as f:
            self.mapping = json.load(f)
        
        print(f"Loaded homepage mapping with {len(self.mapping['homepage_sections'])} sections.")
    
    def _setup_agent_team(self):
        """Set up the homepage generator agent team."""
        print("Setting up homepage generator agent team...")
        self.homepage_generator_team = self._create_homepage_generator_team()
    
    # Individual Agent Creation Methods
    
    def create_website_crawler_agent(self):
        """Create an agent specialized in crawling and analyzing websites."""
        return Agent(
            name="Website Crawler Agent",
            role="You are an expert at crawling websites and extracting relevant content for analysis",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Crawl website URLs to extract text content",
                "Focus on extracting primary content, not navigation or footer elements",
                "Identify and categorize content by page sections",
                "Extract headings, paragraphs, lists, and other structured content",
                "Identify key messaging, value propositions, and unique selling points",
                "Analyze the website's overall structure and content organization",
                "Extract company information, product/service details, and customer testimonials",
                "Identify target audience segments and their needs",
                "Assess current content quality, messaging clarity, and value communication",
                "Format analysis as structured data with categories for each content type",
                "Provide content relevance scores to help with prompt generation"
            ],
            show_tool_calls=True,
            tools=[],  # We'll manually fetch the website content to avoid asyncio issues
            stream=True,
            markdown=True,
        )
    
    def create_content_strategy_agent(self):
        """Create an agent specialized in developing content strategy for homepages."""
        return Agent(
            name="Content Strategy Agent",
            role="You are an expert at developing strategic content plans for marketing websites",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Analyze website content to create a cohesive homepage content strategy",
                "Identify key messages that should be emphasized throughout the homepage",
                "Develop a logical content hierarchy that guides visitors through the value proposition",
                "Create a cohesive narrative structure for the homepage content",
                "Plan the strategic placement of CTAs and conversion points",
                "Ensure content addresses different stages of the buyer journey",
                "Develop a consistent tone and voice strategy based on brand and audience",
                "Identify content gaps in the current website messaging",
                "Plan content structure that accommodates both skimmers and detailed readers",
                "Create a consistent messaging framework that guides all section creation"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_seo_optimization_agent(self):
        """Create an agent specialized in SEO optimization for homepages."""
        return Agent(
            name="SEO Optimization Agent",
            role="You are an expert at optimizing website content for search engines",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Identify primary keywords and search terms relevant to the website's industry and offerings",
                "Determine optimal keyword placement for homepage sections",
                "Suggest semantic HTML structure for SEO optimization",
                "Develop meta descriptions and title tag recommendations",
                "Create header hierarchy recommendations for improved SEO",
                "Ensure natural keyword integration without keyword stuffing",
                "Optimize content for featured snippets and rich results",
                "Create schema.org markup recommendations for the homepage",
                "Develop SEO-friendly heading strategies for each section",
                "Align all recommendations with current search engine best practices"
            ],
            show_tool_calls=True,
            tools=[GoogleSearchTools()],
            stream=True,
            markdown=True,
        )
    
    def create_above_fold_agent(self):
        """Create an agent specialized in above-the-fold content."""
        return Agent(
            name="Above the Fold Agent",
            role="You are an expert at creating compelling above-the-fold website content",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Create concise, powerful headlines that communicate the core value proposition",
                "Develop compelling subheadlines that clarify and support the main headline",
                "Craft primary CTAs that drive immediate engagement and conversion",
                "Design hero section content that captures attention within seconds",
                "Incorporate social proof elements to build immediate credibility",
                "Ensure content communicates what the company does with perfect clarity",
                "Focus on immediate value communication that resonates with target audience",
                "Create visual content direction that supports the messaging",
                "Develop microcopy that guides users to take desired actions",
                "Ensure all content fits within standard above-fold constraints"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_value_proposition_agent(self):
        """Create an agent specialized in crafting value propositions."""
        return Agent(
            name="Value Proposition Agent",
            role="You are an expert at creating compelling value propositions and benefits content",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Develop clear, compelling value propositions that communicate unique benefits",
                "Transform features into customer-focused benefits statements",
                "Create concise benefit bullets that emphasize outcomes over processes",
                "Develop ROI-focused content that quantifies value wherever possible",
                "Ensure all value statements address specific customer pain points",
                "Create comparison content that highlights competitive advantages",
                "Focus on transformational outcomes rather than just service descriptions",
                "Use benefit-driven headings that emphasize customer results",
                "Create consistent value messaging across all content sections",
                "Incorporate proof points and evidence to support value claims"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_use_cases_agent(self):
        """Create an agent specialized in developing use cases and solutions content."""
        return Agent(
            name="Use Cases & Solutions Agent",
            role="You are an expert at creating compelling use cases and solution descriptions",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Create industry-specific or role-based use case content",
                "Develop mini case studies that demonstrate real-world application",
                "Format use cases with clear problem → solution → result structure",
                "Create use case content tailored to different audience segments",
                "Develop solution descriptions that highlight specific capabilities",
                "Create industry-specific language for different target markets",
                "Develop metrics-focused outcome descriptions for each use case",
                "Create versatile use case content that can support dynamic personalization",
                "Ensure use cases address specific pain points for each audience segment",
                "Develop concise storytelling elements that highlight customer transformation"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_social_proof_agent(self):
        """Create an agent specialized in social proof and trust elements."""
        return Agent(
            name="Social Proof & Trust Agent",
            role="You are an expert at creating compelling social proof and trust content",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Transform raw testimonials into compelling story-driven quotes",
                "Create concise case study summaries with quantifiable results",
                "Develop trust-building content around certifications and security",
                "Create client logo showcase descriptions and ordering strategy",
                "Format social proof content for maximum impact and readability",
                "Develop award and recognition presentation content",
                "Create content that reinforces specific value propositions with proof",
                "Optimize testimonial selection to address common objections",
                "Develop content that builds credibility through specificity",
                "Create effective calls-to-action that leverage social proof elements"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_cta_optimization_agent(self):
        """Create an agent specialized in call-to-action optimization."""
        return Agent(
            name="CTA Optimization Agent",
            role="You are an expert at creating effective calls-to-action for website conversions",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Create primary and secondary CTA messaging for all homepage sections",
                "Develop button copy that drives clicks through clarity and value",
                "Create lead generation CTAs for different funnel stages",
                "Develop early-stage CTAs for visitors not yet ready to convert",
                "Create content for forms and signup elements",
                "Develop microcopy that reduces friction and answers objections",
                "Create strategic CTA placement recommendations for each section",
                "Develop newsletter and subscription CTAs that drive engagement",
                "Create urgency and scarcity elements that boost conversion rates",
                "Ensure all CTAs have clear next steps and value communication"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def create_document_composer_agent(self):
        """Create an agent specialized in assembling the final document."""
        return Agent(
            name="Document Composer Agent",
            role="You are an expert at organizing and assembling content into cohesive documents",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=12000),
            instructions=[
                "Compile generated content from multiple agents into a cohesive homepage document",
                "Organize content according to the provided structure and flow",
                "Ensure consistency in tone, style, and formatting across all sections",
                "Add transitional elements between sections for smooth content flow",
                "Format the document according to the requested output format (Markdown or HTML)",
                "Ensure proper heading hierarchy and document structure for SEO",
                "Remove any duplicative content or inconsistencies between sections",
                "Maintain consistent formatting and style throughout the document",
                "Create a clear visual hierarchy through proper structural elements",
                "Ensure the document follows accessibility best practices and semantic structure"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
    
    def _create_homepage_generator_team(self):
        """Create the coordinated homepage generator team."""
        return Agent(
            name="Homepage Generator Team",
            team=[
                self.create_website_crawler_agent(),
                self.create_content_strategy_agent(),
                self.create_seo_optimization_agent(),
                self.create_above_fold_agent(),
                self.create_value_proposition_agent(),
                self.create_use_cases_agent(),
                self.create_social_proof_agent(),
                self.create_cta_optimization_agent(),
                self.create_document_composer_agent()
            ],
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=12000),
            instructions=[
                "You are a team of homepage content creation experts working together to generate comprehensive website homepages.",
                "Given a website URL, analyze the site and generate optimized homepage content that effectively communicates value.",
                "Each team member has specific expertise aligned with essential homepage elements:",
                "1. Website Crawler analyzes the existing website to gather key information and understand current messaging",
                "2. Content Strategy develops the overall narrative and messaging approach",
                "3. SEO Optimization ensures all content follows search engine best practices",
                "4. Above the Fold creates impactful hero section content that hooks visitors immediately",
                "5. Value Proposition crafts compelling benefit statements and unique value messaging",
                "6. Use Cases & Solutions creates targeted content for different audience segments and needs",
                "7. Social Proof & Trust develops credibility-building elements with testimonials and trust signals",
                "8. CTA Optimization creates effective calls-to-action to drive conversions throughout",
                "9. Document Composer assembles all content into a cohesive, well-structured final document",
                "Analyze the website thoroughly to understand its purpose, audience, and current messaging.",
                "Generate a complete homepage document with all necessary sections following the homepage mapping.",
                "Format output according to the requested format (markdown/HTML).",
                "Ensure all content is cohesive, compelling, and optimized for both users and search engines.",
                "Focus on creating a homepage that drives visitors toward specific conversion goals."
            ],
            show_tool_calls=True,
            markdown=True,
            storage=SqliteStorage(table_name="homepage_generator_team", db_file=self.AGENT_STORAGE),
            stream=True,
        )
    
    async def crawl_website(self, url: str) -> Dict[str, Any]:
        """
        Crawl the target website to extract content.
        
        Args:
            url: The URL of the website to crawl
            
        Returns:
            Dict containing extracted website content
        """
        print(f"Starting website crawl for URL: {url}")
        
        try:
            # Get the website content
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content and clean it up
            # Remove script and style elements
            for script_or_style in soup(['script', 'style']):
                script_or_style.extract()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Get a truncated version of the HTML content
            extracted_html = str(soup)[:100000]  # Limit to avoid huge strings
            
            # Return the raw content for now - it will be analyzed by the team
            return {
                "url": url,
                "raw_content": text,
                "html_content": extracted_html,
                "title": soup.title.string if soup.title else url,
            }
            
        except Exception as e:
            print(f"Error crawling website: {e}")
            return {
                "url": url,
                "raw_content": f"Error crawling website: {e}",
                "html_content": "",
                "title": url
            }
    
    async def generate_homepage(self, url: str, output_format: str = "markdown") -> str:
        """
        Generate a complete homepage using the agent team.
        
        Args:
            url: The URL of the website to analyze
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            String containing the complete homepage content
        """
        print(f"Starting homepage generation for URL: {url}")
        
        try:
            # Step 1: Crawl the website
            website_data = await self.crawl_website(url)
            
            # Step 2: Generate the homepage content using the team
            prompt = self._create_team_prompt(url, website_data, output_format)
            
            print("Running homepage generator team...")
            response_stream = self.homepage_generator_team.run(prompt)
            content = ""
            
            # Handle streaming response
            if hasattr(response_stream, '__iter__') and not hasattr(response_stream, 'content'):
                for response_chunk in response_stream:
                    if hasattr(response_chunk, 'content'):
                        content += response_chunk.content
                    print(".", end="", flush=True)
            else:
                # If it's already a RunResponse object with content
                content = response_stream.content if hasattr(response_stream, 'content') else str(response_stream)
            
            print("\nHomepage generation completed successfully.")
            return content
            
        except Exception as e:
            print(f"Error generating homepage: {e}")
            return f"# Error during homepage generation\n\n{str(e)}"
    
    def _create_team_prompt(self, url: str, website_data: Dict[str, Any], output_format: str) -> str:
        """Create the main prompt for the homepage generator team."""
        # Format the JSON mapping structure in a readable way
        sections_summary = "\n".join([
            f"- {section['section_name']}: {section['section_description']}"
            for section in self.mapping["homepage_sections"]
        ])
        
        # Build the team prompt
        prompt = f"""
        # Homepage Generation Task
        
        Please create a complete, professional homepage for the website: {url}
        
        ## Website Information
        Website Title: {website_data.get('title', url)}
        
        ## Homepage Content Sample
        ```
        {website_data.get('raw_content', '')[:2000]}
        ```
        
        ## Required Homepage Sections
        The homepage should include the following sections:
        {sections_summary}
        
        ## Task Instructions
        1. Website Crawler Agent should analyze the provided website content to understand:
           - The company's value proposition and core messaging
           - Product/service offerings and key features
           - Target audience and their needs
           - Brand voice and tone
           
        2. Content Strategy Agent should develop an overall content strategy including:
           - Key messaging priorities
           - Content hierarchy and flow
           - Narrative structure and tone guidance
           
        3. SEO Optimization Agent should provide:
           - Key search terms to target
           - SEO structure recommendations
           - Metadata suggestions
           
        4. Above the Fold Agent should create:
           - Primary headline (clear, compelling value statement)
           - Supporting subheadline
           - Hero section description
           - Primary CTA
           
        5. Value Proposition Agent should develop:
           - Main value proposition statement
           - 3-4 key benefits with supporting copy
           - Feature overview content
           
        6. Use Cases & Solutions Agent should create:
           - Industry or role-specific use cases
           - Solution descriptions
           - Relevant example scenarios
           
        7. Social Proof & Trust Agent should create:
           - Testimonial content and presentation
           - Trust indicators and certification elements
           - Case study/success story snippets
           
        8. CTA Optimization Agent should develop:
           - Primary and secondary CTAs throughout the homepage
           - Form and lead capture content
           - Newsletter/subscription elements
           
        9. Document Composer Agent should:
           - Assemble all content into a cohesive document
           - Ensure proper formatting and structure
           - Format according to the requested output ({output_format})
           
        ## Final Output Requirements
        - The final homepage should be complete and ready to implement
        - All content should be cohesive and follow a consistent tone and messaging strategy
        - Output should be formatted as {output_format}
        - Include all necessary homepage sections with appropriate hierarchy
        - Optimize for both user engagement and search visibility
        """
        
        return prompt
        
    def run_homepage_generator(self, url: str, output_format: str = "markdown") -> str:
        """
        Run the homepage generator for the given URL.
        
        Args:
            url: The URL of the website to analyze
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            String containing the complete homepage content
        """
        try:
            # Check if we're already in an event loop
            try:
                loop = asyncio.get_running_loop()
                # We're inside an event loop, use a different approach
                print("Already inside an event loop, using create_task")
                
                async def run_generator():
                    try:
                        return await self.generate_homepage(url, output_format)
                    except Exception as e:
                        print(f"Error in run_generator: {e}")
                        return f"# Error during homepage generation: {e}"
                
                # Create and run the task
                task = loop.create_task(run_generator())
                
                # Wait for the task to complete
                while not task.done():
                    loop.run_until_complete(asyncio.sleep(0.1))
                    
                return task.result()
                
            except RuntimeError:
                # No running event loop, use asyncio.run
                print("No running event loop, using asyncio.run")
                return asyncio.run(self.generate_homepage(url, output_format))
                
        except Exception as e:
            print(f"Error generating homepage: {e}")
            return f"# Error: {e}"
