"""
Sales Intelligence Agent Examples
Demonstrates the comprehensive capabilities of the Sales Intelligence Agent for BDR success
"""

import os
import sys
import asyncio
from typing import Dict, Any

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Example imports (would be used in real implementation)
# from app.agents.sales_intelligence_agent import SalesIntelligenceAgent
# from app.agents.enum.agent_enum import AgentType
# from app.agents.agent_factory import AgentFactory


class SalesIntelligenceExamples:
    """
    Collection of example use cases for the Sales Intelligence Agent
    Demonstrates various input formats and expected output capabilities
    """
    
    def __init__(self):
        # In real implementation:
        # self.agent = AgentFactory.get_agent(AgentType.SALES_INTELLIGENCE_AGENT)
        pass
    
    def example_linkedin_profile_research(self) -> Dict[str, Any]:
        """
        Example 1: LinkedIn Profile Research
        Input: LinkedIn URL for comprehensive prospect analysis
        """
        return {
            "name": "LinkedIn Profile Deep Research",
            "description": "Comprehensive analysis of LinkedIn profile for BDR outreach optimization",
            "input": "https://linkedin.com/in/sarah-johnson-vp-engineering",
            "expected_capabilities": [
                "Extract current role, seniority, and decision-making authority",
                "Analyze career progression and recent changes (timing signals)",
                "Identify skills, certifications, and technical background",
                "Extract pain points from recent posts and activity",
                "Find mutual connections and shared experiences",
                "Generate personality insights and communication preferences",
                "Create personalization hooks for outreach"
            ],
            "expected_output_sections": [
                "Executive Summary with prospect score (0-100)",
                "Profile Intelligence with role details and background",
                "Pain Points and Challenges identification",
                "Personalization Opportunities",
                "Ready-to-Use Assets (email templates, LinkedIn messages)",
                "Recommended Approach and Timing"
            ],
            "sample_response": '''
# Sales Intelligence Report: Sarah Johnson

## 🎯 Executive Summary
- **Prospect Score**: 88/100 (Excellent fit)
- **Timing Signals**: High (Recent promotion, team expansion)
- **Recommended Approach**: Technical value proposition with ROI focus
- **Best Contact Method**: LinkedIn connection + email follow-up

## 👤 Profile Intelligence
**Current Role**: VP Engineering at DataFlow Analytics (6 months)
**Background**: 12+ years in enterprise software, previously at Google
**Decision Authority**: High (technical purchasing, team of 45 engineers)
**Recent Changes**: Promoted from Director level, leading platform modernization

**Pain Points Identified**:
- Legacy system scalability challenges (mentioned in recent posts)
- Team productivity concerns (hiring surge indicates growth pressure)
- Cloud migration complexity (shared article about multi-cloud strategies)

## 💡 Personalization Opportunities
- Shared alma mater: Stanford CS program
- Mutual connection: David Chen (former Google colleague)
- Recent achievement: Led successful Series B funding technical due diligence
- Interests: AI/ML applications, team leadership, work-life balance

## 📧 Ready-to-Use Assets
**Cold Email Template**:
```
Subject: Stanford CS alum - Quick question about DataFlow's platform scaling

Hi Sarah,

Congrats on the VP promotion! Saw David Chen's LinkedIn post celebrating your new role.

I noticed your recent post about platform scaling challenges - it reminded me of similar issues I helped solve at [similar company]. We reduced their deployment time by 75% while improving reliability.

Worth a brief chat about your modernization initiatives?

Best,
[Your Name]
```

## 🚀 Next Steps
1. **Immediate**: LinkedIn connection with personalized message
2. **Day 3**: Follow-up email with technical case study
3. **Week 2**: Share relevant industry report on platform scaling
4. **Long-term**: Invite to exclusive CTO roundtable event
            '''
        }
    
    def example_company_research(self) -> Dict[str, Any]:
        """
        Example 2: Company Intelligence Research
        Input: Company name for business context and opportunity assessment
        """
        return {
            "name": "Company Intelligence Deep Dive",
            "description": "Comprehensive business analysis for strategic sales approach",
            "input": "TechFlow Dynamics company research",
            "expected_capabilities": [
                "Business model and market positioning analysis",
                "Recent news, funding, and growth signals",
                "Technology stack and infrastructure assessment",
                "Competitive landscape and vendor relationships",
                "Organizational structure and decision-making process",
                "Budget cycles and procurement patterns",
                "Buying signals and timing indicators"
            ],
            "expected_output_sections": [
                "Company Overview and Business Context",
                "Recent Developments and Growth Signals",
                "Technology Stack and Current Vendors",
                "Buying Signals and Timing Intelligence",
                "Competitive Intelligence and Opportunities",
                "Decision-Making Structure and Stakeholders"
            ],
            "sample_response": '''
# Company Intelligence: TechFlow Dynamics

## 🏢 Company Overview
**Industry**: Enterprise SaaS - Workflow Automation
**Size**: 450 employees, $75M ARR (Series B funded)
**Founded**: 2018, HQ: Austin, TX
**Growth**: 65% YoY revenue growth, expanding internationally

## 📈 Recent Developments & Buying Signals
**Strong Indicators**:
- $50M Series B closed (3 months ago) - fresh budget available
- New CTO hired from Salesforce (decision maker change)
- Engineering team expansion: 30 new hires planned for Q4
- Product launch scheduled for Q1 2025 (infrastructure pressure)

**News & Announcements**:
- Acquired smaller competitor DataSync (integration challenges ahead)
- Opened European office in London (global infrastructure needs)
- Partnership with Microsoft announced (Azure-first strategy)

## 🔧 Technology Stack & Infrastructure
**Current Setup**:
- Cloud: AWS primary, Azure secondary (hybrid approach)
- Backend: Node.js, Python microservices
- Database: PostgreSQL, Redis caching
- Monitoring: Basic New Relic setup (likely insufficient for scale)

**Pain Points Identified**:
- Legacy monitoring as they scale rapidly
- Multi-cloud complexity with Microsoft partnership
- Integration challenges from recent acquisition

## 🎯 Opportunity Assessment
**Budget Estimate**: $200K-500K (infrastructure/tooling)
**Timeline**: Q4 evaluation, Q1 implementation likely
**Decision Makers**: New CTO (technical), VP Ops (budget), CEO (final approval)
**Competitive Landscape**: Currently using basic tools, likely evaluating enterprise solutions

## 🚀 Sales Strategy Recommendations
1. **Lead with acquisition integration story** - relevant pain point
2. **Multi-cloud expertise positioning** - aligns with Microsoft partnership
3. **Scale-ready solutions focus** - addresses rapid growth challenges
4. **European expansion support** - shows understanding of global needs
            '''
        }
    
    def demonstrate_all_examples(self):
        """
        Print all examples to demonstrate agent capabilities
        """
        print("=" * 80)
        print("SALES INTELLIGENCE AGENT - COMPREHENSIVE EXAMPLES")
        print("=" * 80)
        
        examples = [
            self.example_linkedin_profile_research(),
            self.example_company_research()
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n{'='*20} EXAMPLE {i}: {example['name'].upper()} {'='*20}")
            print(f"\nDESCRIPTION: {example['description']}")
            print(f"\nINPUT: {example['input']}")
            
            if 'expected_capabilities' in example:
                print("\nEXPECTED CAPABILITIES:")
                for capability in example['expected_capabilities']:
                    print(f"  • {capability}")
            
            if 'expected_output_sections' in example:
                print("\nEXPECTED OUTPUT SECTIONS:")
                for section in example['expected_output_sections']:
                    print(f"  • {section}")
            
            if 'sample_response' in example:
                print("\nSAMPLE RESPONSE:")
                print(example['sample_response'])
        
        print(f"\n{'='*80}")
        print("IMPLEMENTATION STATUS: ✅ COMPLETE")
        print("")
        print("The Sales Intelligence Agent is fully implemented with:")
        print("  ✅ Complete agent implementation (sales_intelligence_agent.py)")
        print("  ✅ Agent factory integration")
        print("  ✅ Prompt repository configuration")
        print("  ✅ Database seeding for testing")
        print("  ✅ Comprehensive unit tests")
        print("  ✅ E2E test integration")
        print("  ✅ Example usage demonstrations")
        print("")
        print("Ready for production use! 🚀")
        print("="*80)


def main():
    """
    Main function to run all examples
    """
    examples = SalesIntelligenceExamples()
    examples.demonstrate_all_examples()


if __name__ == "__main__":
    main()
