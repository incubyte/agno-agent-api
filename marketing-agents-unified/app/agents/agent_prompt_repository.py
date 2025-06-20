"""
Agent Prompt Repository
Centralized repository for agent prompts and instructions.
"""

from app.agents.enum.agent_enum import AgentType

agent_prompt_repository = {
    AgentType.MARKETING_AGENT: {
        "role": "You are an expert marketing analyst and strategist specializing in comprehensive website optimization and conversion analysis.",
        "description": "You are a marketing agent that conducts complete marketing reviews and optimizations of websites. Your task is to analyze websites as marketing machines that generate leads and convert them into customers.",
        "instructions": [
            "Conduct comprehensive marketing reviews focused on lead generation and conversion",
            "Analyze technical aspects, SEO strategy, offers, audience understanding, and conversion pathways",
            "Create complete new website copy variations for different audience segments",
            "Provide actionable recommendations with clear implementation steps",
            "Focus on transforming websites into effective marketing machines",
            "Target audience: CxOs, Product Managers, and Founders of startups",
            "Emphasize quality software development and craftsmanship positioning",
            "Challenge offshore development stereotypes through exceptional quality delivery",
            "Create detailed TODO lists for developers with priority levels",
            "Format all output in markdown with clear sections and actionable steps"
        ]
    },
    
    AgentType.TECH_BLOG_WRITER: {
        "role": "You are an expert technical blog writer specializing in software development, AI, and technology content.",
        "description": "You are a technical blog writer that creates comprehensive, well-structured technical blog posts that educate and engage developers.",
        "instructions": [
            "Create comprehensive, well-structured technical blog posts that educate and engage developers",
            "Include clear explanations of technical concepts with appropriate depth for the target audience",
            "Provide practical code examples, best practices, and real-world applications",
            "Structure content with proper headings, subheadings, and logical flow",
            "Include common pitfalls, troubleshooting tips, and performance considerations",
            "Use markdown formatting for code blocks, links, and emphasis",
            "Ensure content is accurate, up-to-date, and follows industry standards",
            "Create engaging introductions that hook readers and clear conclusions that summarize key points",
            "Include relevant technical keywords for SEO without keyword stuffing",
            "Provide actionable takeaways that readers can implement immediately",
            "Adapt writing style and complexity based on target audience level",
            "Include references to documentation, tools, and additional resources when helpful",
            "Focus on practical value and real-world problem solving",
            "Ensure code examples are syntactically correct and follow best practices"
        ]
    },
    
    AgentType.LINKEDIN_WRITER: {
        "role": "You are an expert LinkedIn content creator specializing in professional, engaging, and viral-worthy posts.",
        "description": "You are a LinkedIn content writer that creates compelling LinkedIn posts that drive engagement and professional value.",
        "instructions": [
            "Create compelling LinkedIn posts that drive engagement and professional value",
            "Use proven LinkedIn content frameworks and best practices",
            "Incorporate storytelling, insights, and actionable takeaways",
            "Optimize for LinkedIn algorithm preferences (engagement, comments, shares)",
            "Include appropriate hashtags and call-to-action elements",
            "Match the tone to professional yet approachable style",
            "Create content that positions the author as a thought leader",
            "Use formatting that works well on LinkedIn (line breaks, emojis when appropriate)",
            "Ensure content is valuable, authentic, and shareable",
            "Format all output in markdown for easy copying",
            "Always include 3-5 relevant hashtags at the end",
            "Create content that encourages meaningful professional discussions",
            "Target audience: Software development professionals, startup founders, tech leaders",
            "Focus on high-quality software development, AI-enhanced solutions, and craftsmanship"
        ]
    },
    
    AgentType.LIFESTYLE_BLOG_WRITER: {
        "role": "You are an expert lifestyle blog writer specializing in wellness, personal development, and lifestyle content.",
        "description": "You are a lifestyle blog writer that creates engaging, relatable lifestyle blog posts that inspire and provide practical value.",
        "instructions": [
            "Create engaging, relatable lifestyle blog posts that inspire and provide practical value",
            "Use storytelling techniques to connect emotionally with readers",
            "Include personal insights, practical tips, and actionable advice",
            "Write in a conversational, authentic tone that feels like talking to a friend",
            "Focus on topics like wellness, personal growth, relationships, productivity, and life balance",
            "Include relatable examples and real-life scenarios",
            "Use positive, uplifting language that motivates readers",
            "Structure content with engaging introductions, valuable body content, and inspiring conclusions",
            "Include practical takeaways that readers can implement immediately",
            "Use markdown formatting for better readability",
            "Create content that feels authentic and avoids being preachy",
            "Include relevant lifestyle trends and current topics when appropriate",
            "Focus on holistic well-being including mental, physical, and emotional health",
            "Make complex lifestyle concepts accessible and easy to understand",
            "Target audience: Modern professionals seeking work-life balance and personal growth"
        ]
    }
}

def get_agent_prompt(agent_type: AgentType) -> dict:
    """
    Get the prompt configuration for a specific agent type.
    
    Args:
        agent_type: The type of agent to get prompts for
        
    Returns:
        Dictionary containing role, description, and instructions for the agent
    """
    return agent_prompt_repository.get(agent_type, {
        "role": "You are a helpful AI assistant.",
        "description": "You are an AI assistant that helps users with various tasks.",
        "instructions": ["Provide helpful and accurate responses to user queries"]
    })

def get_agent_role(agent_type: AgentType) -> str:
    """
    Get the role prompt for a specific agent type.
    
    Args:
        agent_type: The type of agent to get the role for
        
    Returns:
        Role string for the agent
    """
    return get_agent_prompt(agent_type).get("role", "You are a helpful AI assistant.")

def get_agent_instructions(agent_type: AgentType) -> list:
    """
    Get the instructions list for a specific agent type.
    
    Args:
        agent_type: The type of agent to get instructions for
        
    Returns:
        List of instruction strings for the agent
    """
    return get_agent_prompt(agent_type).get("instructions", ["Provide helpful and accurate responses to user queries"])

def get_agent_description(agent_type: AgentType) -> str:
    """
    Get the description for a specific agent type.
    
    Args:
        agent_type: The type of agent to get the description for
        
    Returns:
        Description string for the agent
    """
    return get_agent_prompt(agent_type).get("description", "You are an AI assistant that helps users with various tasks.")

def list_available_agents() -> list:
    """
    Get a list of all available agent types.
    
    Returns:
        List of AgentType enums for all available agents
    """
    return list(agent_prompt_repository.keys())

def validate_agent_type(agent_type: AgentType) -> bool:
    """
    Validate if an agent type is supported.
    
    Args:
        agent_type: The agent type to validate
        
    Returns:
        True if the agent type is supported, False otherwise
    """
    return agent_type in agent_prompt_repository

# Agent-specific prompt templates for different use cases
agent_prompt_templates = {
    AgentType.TECH_BLOG_WRITER: {
        "blog_post": """
        Create a technical blog post about: "{topic}"
        
        Specifications:
        - Complexity Level: {complexity} 
        - Length: {length}
        - Post Type: {post_type}
        
        Content Structure Requirements:
        1. **Engaging Title**: Create a compelling, SEO-friendly title
        2. **Hook Introduction**: Start with a relatable problem or interesting insight
        3. **Clear Outline**: Brief overview of what the post will cover
        4. **Main Content**: Detailed technical content with proper sections
        5. **Code Examples**: Practical, runnable code snippets with explanations
        6. **Best Practices**: Industry-standard recommendations and tips
        7. **Common Pitfalls**: What to avoid and how to troubleshoot issues
        8. **Real-world Applications**: How this applies in actual development scenarios
        9. **Performance Considerations**: Optimization tips and considerations
        10. **Conclusion**: Summary of key takeaways and next steps
        11. **Additional Resources**: Links to documentation, tools, and further reading
        """,
        
        "series": """
        Create a comprehensive blog series about: "{topic}"
        
        Series Specifications:
        - Number of posts: {series_length}
        - Complexity level: {complexity}
        - Each post should be 1500-2500 words
        - Progressive difficulty and depth
        """,
        
        "comparison": """
        Create a comprehensive technical comparison between: {technologies}
        
        Comparison Structure:
        1. **Executive Summary**: Quick overview of recommendations
        2. **Technology Overviews**: Brief introduction to each technology
        3. **Feature Comparison Matrix**: Side-by-side comparison
        4. **Detailed Analysis**: In-depth comparison across criteria
        5. **Use Case Scenarios**: Which technology works best for specific scenarios
        """
    },
    
    AgentType.LINKEDIN_WRITER: {
        "general_post": """
        Create a LinkedIn post based on this prompt: "{prompt}"
        
        Post type: {post_type}
        
        LinkedIn Content Guidelines:
        1. Hook: Start with an attention-grabbing first line
        2. Value: Provide genuine insights or useful information
        3. Story: Use storytelling when appropriate to make it relatable
        4. Engagement: End with a question or call-to-action to encourage comments
        5. Format: Use line breaks, bullet points, and emojis strategically
        6. Length: Optimal for LinkedIn (typically 150-300 words)
        """,
        
        "series": """
        Create a series of {series_length} LinkedIn posts around the topic: "{topic}"
        
        Each post should:
        1. Stand alone as valuable content
        2. Connect to the overall theme
        3. Build anticipation for the next post
        4. Include series numbering
        5. Use different content formats
        """
    },
    
    AgentType.LIFESTYLE_BLOG_WRITER: {
        "blog_post": """
        Create a lifestyle blog post about: "{topic}"
        
        Specifications:
        - Style: {style}
        - Length: {length}
        - Focus Area: {focus_area}
        
        Content Structure Requirements:
        1. **Compelling Title**: Engaging, relatable headline
        2. **Hook Opening**: Start with a relatable scenario or personal story
        3. **Personal Connection**: Share relevant insights or experiences
        4. **Main Content**: Valuable lifestyle advice in digestible sections
        5. **Practical Tips**: Actionable advice readers can implement today
        6. **Real-life Examples**: Relatable scenarios and case studies
        7. **Common Challenges**: Address obstacles and how to overcome them
        8. **Mindful Reflection**: Encourage self-reflection and awareness
        9. **Inspiring Conclusion**: End with motivation and clear next steps
        """,
        
        "seasonal": """
        Create seasonal lifestyle content for: "{season}"
        
        Focus Area: {lifestyle_focus}
        
        Seasonal Content Requirements:
        1. **Seasonal Connection**: How this time affects lifestyle and well-being
        2. **Timely Challenges**: Common struggles during this season
        3. **Seasonal Opportunities**: Unique advantages this season offers
        4. **Practical Adaptations**: How to adjust routines seasonally
        """
    }
}

def get_prompt_template(agent_type: AgentType, template_type: str) -> str:
    """
    Get a specific prompt template for an agent type.
    
    Args:
        agent_type: The type of agent
        template_type: The specific template type (e.g., 'blog_post', 'series')
        
    Returns:
        Prompt template string
    """
    agent_templates = agent_prompt_templates.get(agent_type, {})
    return agent_templates.get(template_type, "")

def format_prompt_template(agent_type: AgentType, template_type: str, **kwargs) -> str:
    """
    Get and format a prompt template with the provided parameters.
    
    Args:
        agent_type: The type of agent
        template_type: The specific template type
        **kwargs: Parameters to format into the template
        
    Returns:
        Formatted prompt string
    """
    template = get_prompt_template(agent_type, template_type)
    try:
        return template.format(**kwargs)
    except KeyError as e:
        print(f"Warning: Missing template parameter {e} for {agent_type.value} {template_type}")
        return template

def get_all_template_types(agent_type: AgentType) -> list:
    """
    Get all available template types for a specific agent.
    
    Args:
        agent_type: The type of agent
        
    Returns:
        List of available template types
    """
    agent_templates = agent_prompt_templates.get(agent_type, {})
    return list(agent_templates.keys())

def create_agent_from_repository(agent_type: AgentType):
    """
    Create an agent instance using the prompt repository configuration.
    This function demonstrates how to use the repository with actual agent creation.
    
    Args:
        agent_type: The type of agent to create
        
    Returns:
        Configured agent instance (placeholder - would need actual agent imports)
    """
    from agno.agent import Agent
    from agno.models.anthropic import Claude
    from agno.tools.reasoning import ReasoningTools
    from agno.tools.googlesearch import GoogleSearchTools
    from app.core import settings
    
    config = get_agent_prompt(agent_type)
    
    # Base configuration for all agents
    base_config = {
        "name": agent_type.value.replace('-', ' ').title(),
        "role": config.get("role", "You are a helpful AI assistant."),
        "model": Claude(id="claude-3-5-sonnet-20241022", max_tokens=8096),
        "instructions": config.get("instructions", ["Provide helpful responses."]),
        "show_tool_calls": True,
        "tools": [ReasoningTools(add_instructions=True)],
        "stream": True,
        "markdown": True,
    }
    
    # Agent-specific tool configurations
    if agent_type in [AgentType.TECH_BLOG_WRITER, AgentType.LIFESTYLE_BLOG_WRITER]:
        base_config["tools"].append(GoogleSearchTools())
    elif agent_type == AgentType.MARKETING_AGENT:
        from agno.tools.crawl4ai import Crawl4aiTools
        base_config["tools"].extend([GoogleSearchTools(), Crawl4aiTools(max_length=None)])
        base_config["max_tokens"] = 12000
    
    return Agent(**base_config)

# Prompt enhancement utilities
def enhance_prompt_with_context(base_prompt: str, agent_type: AgentType, **context) -> str:
    """
    Enhance a basic prompt with agent-specific context and instructions.
    
    Args:
        base_prompt: The base prompt to enhance
        agent_type: The type of agent
        **context: Additional context parameters
        
    Returns:
        Enhanced prompt string
    """
    config = get_agent_prompt(agent_type)
    instructions = "\\n".join([f"- {inst}" for inst in config.get("instructions", [])])
    
    enhanced = f"""
{config.get('role', '')}

{config.get('description', '')}

Instructions:
{instructions}

User Request: {base_prompt}

"""
    
    # Add context if provided
    if context:
        context_str = "\\n".join([f"- {k}: {v}" for k, v in context.items()])
        enhanced += f"\\nAdditional Context:\\n{context_str}\\n"
    
    return enhanced.strip()

# Agent capability matrix
agent_capabilities = {
    AgentType.MARKETING_AGENT: {
        "primary_functions": ["website_analysis", "seo_optimization", "conversion_optimization", "copy_creation"],
        "output_formats": ["comprehensive_reports", "todo_lists", "copy_variations", "analysis_summaries"],
        "target_audience": ["cxos", "product_managers", "founders", "marketing_teams"],
        "complexity_levels": ["executive_summary", "detailed_analysis", "implementation_guide"],
        "use_cases": ["website_audit", "competitor_analysis", "conversion_optimization", "copy_rewriting"]
    },
    
    AgentType.TECH_BLOG_WRITER: {
        "primary_functions": ["blog_posts", "tutorials", "technology_reviews", "comparisons", "series_creation"],
        "output_formats": ["blog_posts", "tutorial_series", "comparison_matrices", "technical_guides"],
        "target_audience": ["developers", "technical_leads", "engineers", "students"],
        "complexity_levels": ["beginner", "intermediate", "advanced"],
        "use_cases": ["education", "thought_leadership", "documentation", "technology_evaluation"]
    },
    
    AgentType.LINKEDIN_WRITER: {
        "primary_functions": ["professional_posts", "thought_leadership", "engagement_content", "series_creation"],
        "output_formats": ["linkedin_posts", "post_series", "engagement_content", "professional_updates"],
        "target_audience": ["professionals", "executives", "entrepreneurs", "tech_community"],
        "complexity_levels": ["quick_insights", "detailed_analysis", "comprehensive_series"],
        "use_cases": ["brand_building", "thought_leadership", "network_engagement", "professional_updates"]
    },
    
    AgentType.LIFESTYLE_BLOG_WRITER: {
        "primary_functions": ["lifestyle_posts", "wellness_content", "personal_development", "seasonal_content"],
        "output_formats": ["blog_posts", "guides", "series", "advice_content"],
        "target_audience": ["general_public", "wellness_seekers", "professionals", "personal_growth_enthusiasts"],
        "complexity_levels": ["casual", "formal", "inspirational", "conversational"],
        "use_cases": ["education", "inspiration", "guidance", "community_building"]
    }
}

def get_agent_capabilities(agent_type: AgentType) -> dict:
    """
    Get the capabilities matrix for a specific agent type.
    
    Args:
        agent_type: The type of agent
        
    Returns:
        Dictionary containing agent capabilities
    """
    return agent_capabilities.get(agent_type, {})

def suggest_agent_for_task(task_description: str) -> list:
    """
    Suggest the most suitable agent(s) for a given task.
    
    Args:
        task_description: Description of the task
        
    Returns:
        List of suggested AgentType enums, ordered by suitability
    """
    task_lower = task_description.lower()
    suggestions = []
    
    # Simple keyword-based matching - could be enhanced with ML
    if any(word in task_lower for word in ['website', 'marketing', 'seo', 'conversion', 'copy']):
        suggestions.append(AgentType.MARKETING_AGENT)
    
    if any(word in task_lower for word in ['technical', 'programming', 'code', 'tutorial', 'development']):
        suggestions.append(AgentType.TECH_BLOG_WRITER)
    
    if any(word in task_lower for word in ['linkedin', 'professional', 'networking', 'career']):
        suggestions.append(AgentType.LINKEDIN_WRITER)
    
    if any(word in task_lower for word in ['lifestyle', 'wellness', 'personal', 'health', 'growth']):
        suggestions.append(AgentType.LIFESTYLE_BLOG_WRITER)
    
    # If no specific matches, return all agents
    if not suggestions:
        suggestions = list(AgentType)
    
    return suggestions

# Export commonly used functions for easy imports
__all__ = [
    'agent_prompt_repository',
    'get_agent_prompt',
    'get_agent_role', 
    'get_agent_instructions',
    'get_agent_description',
    'list_available_agents',
    'validate_agent_type',
    'get_prompt_template',
    'format_prompt_template',
    'get_all_template_types',
    'create_agent_from_repository',
    'enhance_prompt_with_context',
    'get_agent_capabilities',
    'suggest_agent_for_task'
]audience": ["cxos", "product_managers", "founders", "marketing_teams"],
        "complexity_levels": ["executive_summary", "detailed_analysis", "implementation_guide"],
        "use_cases": ["website_audit", "competitor_analysis", "conversion_optimization", "copy_rewriting"]
    },
    
    AgentType.TECH_BLOG_WRITER: {
        "primary_functions": ["blog_posts", "tutorials", "technology_reviews", "comparisons", "series_creation"],
        "output_formats": ["blog_posts", "tutorial_series", "comparison_matrices", "technical_guides"],
        "target_audience": ["developers", "technical_leads", "engineers", "students"],
        "complexity_levels": ["beginner", "intermediate", "advanced"],
        "use_cases": ["education", "thought_leadership", "documentation", "technology_evaluation"]
    },
    
    AgentType.LINKEDIN_WRITER: {
        "primary_functions": ["professional_posts", "thought_leadership", "engagement_content", "series_creation"],
        "output_formats": ["linkedin_posts", "post_series", "engagement_content", "professional_updates"],
        "target_audience": ["professionals", "executives", "entrepreneurs", "tech_community"],
        "complexity_levels": ["quick_insights", "detailed_analysis", "comprehensive_series"],
        "use_cases": ["brand_building", "thought_leadership", "network_engagement", "professional_updates"]
    },
    
    AgentType.LIFESTYLE_BLOG_WRITER: {
        "primary_functions": ["lifestyle_posts", "wellness_content", "personal_development", "seasonal_content"],
        "output_formats": ["blog_posts", "guides", "series", "advice_content"],
        "target_audience": ["general_public", "wellness_seekers", "professionals", "personal_growth_enthusiasts"],
        "complexity_levels": ["casual", "formal", "inspirational", "conversational"],
        "use_cases": ["education", "inspiration", "guidance", "community_building"]
    }
}

def get_agent_capabilities(agent_type: AgentType) -> dict:
    """
    Get the capabilities matrix for a specific agent type.
    
    Args:
        agent_type: The type of agent
        
    Returns:
        Dictionary containing agent capabilities
    """
    return agent_capabilities.get(agent_type, {})

def suggest_agent_for_task(task_description: str) -> list:
    """
    Suggest the most suitable agent(s) for a given task.
    
    Args:
        task_description: Description of the task
        
    Returns:
        List of suggested AgentType enums, ordered by suitability
    """
    task_lower = task_description.lower()
    suggestions = []
    
    # Simple keyword-based matching - could be enhanced with ML
    if any(word in task_lower for word in ['website', 'marketing', 'seo', 'conversion', 'copy']):
        suggestions.append(AgentType.MARKETING_AGENT)
    
    if any(word in task_lower for word in ['technical', 'programming', 'code', 'tutorial', 'development']):
        suggestions.append(AgentType.TECH_BLOG_WRITER)
    
    if any(word in task_lower for word in ['linkedin', 'professional', 'networking', 'career']):
        suggestions.append(AgentType.LINKEDIN_WRITER)
    
    if any(word in task_lower for word in ['lifestyle', 'wellness', 'personal', 'health', 'growth']):
        suggestions.append(AgentType.LIFESTYLE_BLOG_WRITER)
    
    # If no specific matches, return all agents
    if not suggestions:
        suggestions = list(AgentType)
    
    return suggestions

# Export commonly used functions for easy imports
__all__ = [
    'agent_prompt_repository',
    'get_agent_prompt',
    'get_agent_role', 
    'get_agent_instructions',
    'get_agent_description',
    'list_available_agents',
    'validate_agent_type',
    'get_prompt_template',
    'format_prompt_template',
    'get_all_template_types',
    'create_agent_from_repository',
    'enhance_prompt_with_context',
    'get_agent_capabilities',
    'suggest_agent_for_task'
]
