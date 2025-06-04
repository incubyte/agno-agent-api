# HomepageGeneratorAgentTeam

## Overview

The HomepageGeneratorAgentTeam is an advanced system for automatically generating comprehensive website homepage content using a team of specialized AI agents. This system follows the Agno team-based agent architecture to produce high-quality, conversion-focused homepage content.

## How It Works

The system follows these steps:

1. **Website Analysis**: Crawls and analyzes a target website to extract content, structure, and messaging
2. **Content Strategy**: Develops an overall content strategy based on the website's purpose and audience
3. **Section Generation**: Creates specialized content for each homepage section using dedicated agents
4. **SEO Optimization**: Optimizes content for search visibility and user engagement
5. **Document Assembly**: Assembles the final homepage with proper structure and formatting
6. **Output**: Exports the document in the requested format (markdown or HTML)

## Agent Team Structure

The team consists of specialized agents that work together:

1. **Website Crawler Agent**: Analyzes existing websites to extract information and understand messaging
2. **Content Strategy Agent**: Develops the overall narrative and messaging approach
3. **SEO Optimization Agent**: Ensures content follows search engine best practices
4. **Above the Fold Agent**: Creates hero section content that hooks visitors immediately
5. **Value Proposition Agent**: Crafts compelling benefit statements
6. **Use Cases & Solutions Agent**: Creates targeted content for different audience segments
7. **Social Proof & Trust Agent**: Develops credibility-building elements
8. **CTA Optimization Agent**: Creates effective calls-to-action to drive conversions
9. **Document Composer Agent**: Assembles all content into a cohesive final document

## Homepage Sections

The generator creates content for these standard homepage sections:

- **Above the Fold**: Hero section with headline, subheadline, and primary CTA
- **Market Insight**: Problem statements and industry context
- **Value Propositions & Benefits**: Core value proposition and supporting benefits
- **How It Works**: Process explanation and visualization
- **Use Cases & Solutions**: Industry or role-specific examples
- **Social Proof & Trust**: Testimonials, case studies, and trust indicators
- **Secondary CTAs & Resources**: Additional conversion opportunities
- **Navigation & UX**: Structure and user experience guidance
- **Footer**: Contact information and compliance elements

## Usage

You can use the HomepageGeneratorAgentTeam through various interfaces:

### Command Line

```bash
python scripts/generate_homepage_team.py --url https://yourwebsite.com --format markdown --output output/homepage.md
```

### Enhanced Script with Approach Selection

```bash
python scripts/enhanced_homepage_generator.py --url https://yourwebsite.com --format markdown --output output/homepage.md --approach team
```

### Programmatic Usage

```python
from app.agents.homepage_generator_team import HomepageGeneratorAgentTeam

# Create the team
generator = HomepageGeneratorAgentTeam()

# Generate the homepage
content = await generator.generate_homepage(
    url="https://yourwebsite.com",
    output_format="markdown"
)

# Use the generated content
print(content)
```

## Advantages Over Single-Agent Approach

The team-based approach offers several advantages:

1. **Specialized Expertise**: Each agent focuses on a specific aspect of content creation
2. **Higher Quality Output**: Specialized focus leads to better results in each area
3. **Comprehensive Coverage**: Ensures all homepage elements receive proper attention
4. **Consistent Strategy**: Content strategy coordination across all sections
5. **Balanced Perspective**: Multiple specialized viewpoints working together

## Implementation Details

- Based on the Agno agent framework using Claude AI models
- Configured with section-specific instructions and prompts
- Uses structured JSON mapping for homepage organization
- Supports both markdown and HTML output formats
- Includes extensive error handling and recovery mechanisms

## Dependencies

- Agno AI framework
- Claude 3.7 Sonnet API access
- BeautifulSoup for HTML parsing
- SQLite storage for agent memory
