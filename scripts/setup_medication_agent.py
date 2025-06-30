#!/usr/bin/env python3
"""
Setup script for Medication Interaction Agent
Adds the agent to the database and verifies installation
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

try:
    from sqlmodel import Session, select
    from app.db.engine import engine
    from app.db.models import Agent
    from app.agents.enum.agent_enum import AgentType
    from app.agents.agent_factory import AgentFactory
    from datetime import datetime
    import logging

    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    def setup_medication_agent():
        """Add the Medication Interaction Agent to the database"""
        
        logger.info("Setting up Medication Interaction Agent...")
        
        try:
            # Test database connection first
            with Session(engine) as session:
                # Check if agent already exists
                existing_agent = session.exec(
                    select(Agent).where(Agent.slug == "medication-interaction")
                ).first()
                
                if existing_agent:
                    logger.info(f"Medication Interaction Agent already exists with ID: {existing_agent.id}")
                    return existing_agent
                
                # Create new agent entry
                new_agent = Agent(
                    name="Medication Interaction Agent",
                    slug="medication-interaction",
                    description="Advanced AI agent for comprehensive medication interaction analysis, safety assessment, and clinical decision support with real-time drug database integration using free search tools.",
                    image=None,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                
                session.add(new_agent)
                session.commit()
                session.refresh(new_agent)
                
                logger.info(f"✅ Created Medication Interaction Agent with ID: {new_agent.id}")
                return new_agent
                
        except Exception as e:
            logger.error(f"❌ Database setup error: {e}")
            logger.error("Make sure your database is accessible and the schema is up to date.")
            return None

    def verify_agent_setup():
        """Verify the agent is properly set up"""
        
        logger.info("Verifying Medication Interaction Agent setup...")
        
        try:
            # Test database connection and agent existence
            with Session(engine) as session:
                agents = session.exec(
                    select(Agent).where(Agent.slug == "medication-interaction")
                ).all()
                
                if not agents:
                    logger.error("❌ No medication agents found in database")
                    return False
                
                logger.info(f"✅ Found {len(agents)} medication agent(s) in database")
            
            # Test agent factory integration
            try:
                from app.agents.medication_interaction_agent import MedicationInteractionAgent
                agent_instance = AgentFactory.get_agent(AgentType.MEDICATION_INTERACTION_AGENT)
                logger.info("✅ Agent factory integration successful")
            except Exception as e:
                logger.error(f"❌ Agent factory integration failed: {e}")
                return False
            
            # Test agent initialization
            try:
                med_agent = MedicationInteractionAgent()
                logger.info("✅ Agent initialization successful")
            except Exception as e:
                logger.error(f"❌ Agent initialization failed: {e}")
                return False
            
            logger.info("✅ Medication Interaction Agent verification completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Verification failed: {e}")
            return False

    def main():
        """Main setup function"""
        print("🔧 Medication Interaction Agent Setup")
        print("=" * 50)
        
        # Check environment variables
        required_vars = ['ANTHROPIC_API_KEY', 'DATABASE_URL', 'AGENT_STORAGE']
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.warning(f"⚠️  Missing environment variables: {', '.join(missing_vars)}")
            logger.info("Please ensure these are set in your .env file")
        else:
            logger.info("✅ Environment variables verified")
        
        # Setup agent in database
        agent = setup_medication_agent()
        if not agent:
            logger.error("❌ Failed to setup agent in database")
            return False
        
        # Verify setup
        if verify_agent_setup():
            print("\n🎉 Setup completed successfully!")
            print("\nNext steps:")
            print("1. Start the server: uvicorn app.main:app --reload")
            print("2. Test the agent via API at http://localhost:8000/docs")
            print("3. Look for 'Medication Interaction Agent' in the agents list")
            return True
        else:
            logger.error("❌ Setup verification failed")
            return False

    if __name__ == "__main__":
        import argparse
        
        parser = argparse.ArgumentParser(description='Setup Medication Interaction Agent')
        parser.add_argument('--verify-only', action='store_true', help='Only verify existing setup')
        args = parser.parse_args()
        
        if args.verify_only:
            success = verify_agent_setup()
        else:
            success = main()
        
        sys.exit(0 if success else 1)

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please make sure you're running this from the project root and all dependencies are installed.")
    print("Run: uv sync")
    sys.exit(1)
