"""
Seed file for E2E test database.
This file populates the test database with sample data for testing various scenarios,
including success and failure cases.

Uses the existing database engine from conftest.py setup.
"""
import os
import sys
from sqlmodel import Session, text

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, project_root)


def seed_test_database(engine):
    """
    Seed the test database with sample data for E2E testing.
    Includes both valid data and edge cases for testing failure scenarios.
    
    Args:
        engine: Database engine from conftest setup_test_db fixture
    """
    print("Seeding test database with sample data...")
    
    try:
        # Import models after environment is set up
        from app.db.models import Agent
        
        with Session(engine) as session:
            # Clear existing data first
            session.execute(text("DELETE FROM agents"))
            session.commit()
            
            # Sample agents for testing
            sample_agents = [
                # Valid agents for success scenarios that match AgentType enum
                Agent(
                    name="Marketing Agent",
                    slug="marketing-agent",  # Matches AgentType.MARKETING_AGENT
                    description="An AI agent specialized in creating marketing content",
                    image="marketing-agent.png"
                ),
                Agent(
                    name="Tech Blog Writer Agent",
                    slug="tech-blog-writer-agent",  # Matches AgentType.TECH_BLOG_WRITER_AGENT
                    description="Specialized in writing technical blog posts and documentation",
                    image="tech-writer.png"
                ),
                Agent(
                    name="LinkedIn Writer Agent",
                    slug="linkedin-writer-agent",  # Matches AgentType.LINKEDIN_WRITER_AGENT
                    description="Creates engaging LinkedIn posts and professional content",
                    image="linkedin-agent.png"
                ),
                Agent(
                    name="Lifestyle Blog Writer Agent",
                    slug="lifestyle-blog-writer-agent",  # Matches AgentType.LIFESTYLE_BLOG_WRITER_AGENT
                    description="Creates engaging lifestyle and wellness content",
                    image="lifestyle.png"
                ),
                Agent(
                    name="AI Agent",
                    slug="ai-agent",  # Matches AgentType.AI_AGENT
                    description="General purpose AI assistant for various tasks",
                    image="ai-agent.png"
                ),
                
                # New SEO and Marketing Agents
                Agent(
                    name="Website Performance Auditor",
                    slug="website-audit",  # Matches AgentType.WEBSITE_PERFORMANCE_AUDITOR
                    description="Comprehensive website effectiveness benchmark with SEO insights and optimization recommendations. Analyzes technical performance, SEO foundation, business messaging, and conversion metrics.",
                    image="website-audit.svg"
                ),
                Agent(
                    name="SEO Auditor Agent",
                    slug="seo-audit",  # Matches AgentType.SEO_AUDIT
                    description="Deep SEO analysis identifying keyword gaps and high-value optimization opportunities. Provides keyword research, content gap analysis, and technical SEO recommendations.",
                    image="seo-audit.svg"
                ),
                Agent(
                    name="Marketing Copywriter Agent",
                    slug="marketing-copy",  # Matches AgentType.MARKETING_COPYWRITER_AGENT
                    description="AI-powered copywriting team creating conversion-optimized content for different audience segments. Includes audience research, messaging strategy, and copy optimization.",
                    image="marketing-copy.svg"
                ),
                
                # Edge case agents for testing various scenarios (these will cause prompt errors but are useful for other tests)
                Agent(
                    name="Test Agent with Long Name for Boundary Testing",
                    slug="test-long-name-agent",
                    description="This is a test agent with a very long description to test how the system handles lengthy text inputs and ensure proper validation and display across different components of the application",
                    image="test-long.png"
                ),
                Agent(
                    name="Special-Chars-Agent!@#",
                    slug="special-chars-agent",
                    description="Agent with special characters for testing edge cases",
                    image="special.png"
                ),
                Agent(
                    name="Minimal Agent",
                    slug="minimal",
                    description="Min",
                    image="min.png"
                )
            ]
            
            # Add all agents to database
            for agent in sample_agents:
                session.add(agent)
            
            session.commit()
            
            # Verify seeding
            agent_count = session.execute(text("SELECT COUNT(*) FROM agents")).fetchone()[0]
            print(f"Successfully seeded {agent_count} agents to test database")
            
            return len(sample_agents)  # Returns 11 agents total
            
    except ImportError as e:
        print(f"Could not import models: {e}")
        print("   Make sure the project structure is correct")
        raise
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise


def clear_test_database(engine):
    """
    Clear all data from test database
    
    Args:
        engine: Database engine from conftest setup_test_db fixture
    """
    print("🧹 Clearing test database...")
    
    try:
        with Session(engine) as session:
            # Get all table names
            result = session.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
            tables = [row[0] for row in result if not row[0].startswith('sqlite_')]
            
            # Clear all tables
            for table in tables:
                session.execute(text(f"DELETE FROM {table}"))
            
            session.commit()
            print(f"Cleared {len(tables)} tables from test database")
            
    except Exception as e:
        print(f"Error clearing database: {e}")
        raise


def get_seeded_data_info():
    """Get information about seeded data for test reference"""
    return {
        "valid_agents": [
            {"slug": "marketing-agent", "name": "Marketing Agent"},
            {"slug": "tech-blog-writer-agent", "name": "Tech Blog Writer Agent"},
            {"slug": "linkedin-writer-agent", "name": "LinkedIn Writer Agent"},
            {"slug": "lifestyle-blog-writer-agent", "name": "Lifestyle Blog Writer Agent"},
            {"slug": "ai-agent", "name": "AI Agent"},
            {"slug": "website-audit", "name": "Website Performance Auditor"},
            {"slug": "seo-audit", "name": "SEO Auditor Agent"},
            {"slug": "marketing-copy", "name": "Marketing Copywriter Agent"},
        ],
        "edge_case_agents": [
            {"slug": "test-long-name-agent", "name": "Test Agent with Long Name for Boundary Testing"},
            {"slug": "special-chars-agent", "name": "Special-Chars-Agent!@#"},
            {"slug": "minimal", "name": "Minimal Agent"},
        ],
        "total_count": 11,
        "test_scenarios": {
            "success_cases": ["marketing-agent", "tech-blog-writer-agent", "linkedin-writer-agent"],
            "edge_cases": ["test-long-name-agent", "special-chars-agent", "minimal"],
            "duplicate_test": "marketing-agent",  # Use this to test duplicate creation
            "nonexistent_slug": "nonexistent-agent",  # Use this to test 404 scenarios
        }
    }
