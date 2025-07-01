"""
End-to-End tests for the Agent Router
Tests all endpoints in app/routers/agent.py with real database and service interactions
"""
import pytest
import os
import sys

# Import the app - path setup is handled in conftest.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.db.models import Agent


@pytest.mark.e2e
class TestAgentRouterE2E:
    """E2E test class for Agent Router endpoints"""
    
    def _get_serializable_agent_data(self, agent: Agent) -> dict:
        """
        Convert Agent model to serializable dict for JSON requests.
        Excludes datetime fields that cause serialization issues.
        """
        data = {
            "name": agent.name,
            "slug": agent.slug,
        }
        
        # Add optional fields only if they're not None
        if agent.description is not None:
            data["description"] = agent.description
        if agent.image is not None:
            data["image"] = agent.image
            
        return data


    # =============================================================================
    # GET /agents - Get all agents
    # =============================================================================

    def test_get_agents_success(self, e2e_test_client):
        """Test GET /agents - Success scenario with seeded data"""
      
        response = e2e_test_client.get("/agents")
        print("Response:", response.json())
        
        assert response.status_code == 200 
        agents = response.json()
        assert isinstance(agents, list)
   
        
    # =============================================================================
    # POST /create-agent - Create new agent
    # =============================================================================
    
    def test_create_agent_success(self, e2e_test_client, sample_agent_data):
        """Test POST /create-agent - Success scenario"""
        agent = Agent(**sample_agent_data)
        response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        
        assert response.status_code == 200
        created_agent = response.json()
        assert created_agent["name"] == sample_agent_data["name"]
        assert created_agent["slug"] == sample_agent_data["slug"]
        assert created_agent["description"] == sample_agent_data["description"]
        assert created_agent["id"] is not None

    # =============================================================================
    # GET /agents/{agent_id} - Get agent by ID
    # =============================================================================

    def test_get_agent_by_id_success(self, e2e_test_client, sample_agent_data):
        """Test GET /agents/{agent_id} - Success scenario"""
        agent_id = 1  # Assuming this ID exists in the seeded data
        # refer the seed.py file for the seeded data

        # Get agent by ID which already exists in the database
        response = e2e_test_client.get(f"/agents/{agent_id}")
        print("Get agent response:", response.json())
        
        assert response.status_code == 200
        agent_data = response.json()
        assert agent_data["agent"]["id"] == agent_id
        assert agent_data["agent"]["name"] == "Marketing Agent"

    def test_get_agent_by_id_not_found(self, e2e_test_client):
        """Test GET /agents/{agent_id} - Error scenario: agent not found"""
        non_existent_id = 99999
        response = e2e_test_client.get(f"/agents/{non_existent_id}")
        
        assert response.status_code == 404
        assert f"Agent with ID {non_existent_id} not found" in response.json()["detail"]

    # =============================================================================
    # PUT /agents/{agent_id} - Update agent
    # =============================================================================
    
    def test_update_agent_success(self, e2e_test_client, sample_agent_data):
        """Test PUT /agents/{agent_id} - Success scenario"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "test-update"  # Unique slug
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        agent_id = create_response.json()["id"]
        
        # Update agent
        update_data = {
            "name": "Updated Test Agent",
            "description": "Updated description for testing"
        }
        response = e2e_test_client.put(f"/agents/{agent_id}", json=update_data)
        
        assert response.status_code == 200
        updated_agent = response.json()
        assert updated_agent["name"] == update_data["name"]
        assert updated_agent["description"] == update_data["description"]
        assert updated_agent["id"] == agent_id

    def test_update_agent_not_found(self, e2e_test_client):
        """Test PUT /agents/{agent_id} - Error scenario: agent not found"""
        non_existent_id = 99999
        update_data = {"name": "Updated Name"}
        
        response = e2e_test_client.put(f"/agents/{non_existent_id}", json=update_data)
        print("Update agent response:", response.json())
        assert response.status_code == 404
        assert f"Agent with ID {non_existent_id} not found" in response.json()["detail"]

    # =============================================================================
    # DELETE /agents/{agent_id} - Delete agent
    # =============================================================================
    
    def test_delete_agent_success(self, e2e_test_client, sample_agent_data):
        """Test DELETE /agents/{agent_id} - Success scenario"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "test-delete"  # Unique slug
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        agent_id = create_response.json()["id"]
        
        # Delete agent
        response = e2e_test_client.delete(f"/agents/{agent_id}")
        
        assert response.status_code == 200
        assert f"Agent with ID {agent_id} deleted successfully" in response.json()["message"]
        
        # Verify agent is deleted
        get_response = e2e_test_client.get(f"/agents/{agent_id}")
        assert get_response.status_code == 404

    def test_delete_agent_not_found(self, e2e_test_client):
        """Test DELETE /agents/{agent_id} - Error scenario: agent not found"""
        non_existent_id = 99999
        
        response = e2e_test_client.delete(f"/agents/{non_existent_id}")
        
        assert response.status_code == 404
        assert f"Agent with ID {non_existent_id} not found" in response.json()["detail"]

    # =============================================================================
    # POST /run-agent/{agent_id} - Run agent
    # =============================================================================
    
    @pytest.mark.skipif(
        os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true",
        reason="Skipping tests that make external API calls"
    )
    def test_run_agent_success(self, e2e_test_client, sample_agent_data):
        """Test POST /run-agent/{agent_id} - Success scenario"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "marketing-agent"  # Use a slug that exists in the system
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        agent_id = create_response.json()["id"]
        
        # Run agent
        request_data = {
            "prompt": "Give me a brief summary about artificial intelligence",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{agent_id}", json=request_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0

    def test_run_agent_not_found(self, e2e_test_client):
        """Test POST /run-agent/{agent_id} - Error scenario: agent not found"""
        non_existent_id = 99999
        request_data = {
            "prompt": "Test prompt",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{non_existent_id}", json=request_data)
        assert response.status_code == 400
        assert f"Agent with ID {non_existent_id} not found" in response.json()["detail"]

    def test_run_agent_empty_prompt(self, e2e_test_client, sample_agent_data):
        """Test POST /run-agent/{agent_id} - Error scenario: empty prompt"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "test-run-empty-prompt"  # Unique slug
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        agent_id = create_response.json()["id"]
        
        # Run agent with empty prompt
        request_data = {
            "prompt": "",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{agent_id}", json=request_data)
        
        assert response.status_code == 400
        assert "must not be empty" in response.json()["detail"]

    # =============================================================================
    # GET /agents/slug/{slug} - Get agent by slug
    # =============================================================================
    
    def test_get_agent_by_slug_success(self, e2e_test_client, sample_agent_data):
        """Test GET /agents/slug/{slug} - Success scenario"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "test-get-by-slug"  # Unique slug
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        
        # Get agent by slug
        response = e2e_test_client.get(f"/agents/slug/{agent.slug}")
        
        assert response.status_code == 200
        agent_data = response.json()
        assert agent_data["slug"] == agent.slug
        assert agent_data["name"] == sample_agent_data["name"]

    def test_get_agent_by_slug_not_found(self, e2e_test_client):
        """Test GET /agents/slug/{slug} - Error scenario: slug not found"""
        non_existent_slug = "non-existent-agent"
        response = e2e_test_client.get(f"/agents/slug/{non_existent_slug}")
        
        assert response.status_code == 404
        assert f"Agent with slug {non_existent_slug} not found" in response.json()["detail"]

    # =============================================================================
    # GET /agents/count - Get agent count
    # =============================================================================
    
    def test_get_agent_count(self, e2e_test_client):
        """Test GET /agents/count - Success scenario"""
        response = e2e_test_client.get("/agents/count")
        assert response.status_code == 200
        count_data = response.json()
        assert "count" in count_data
        assert isinstance(count_data["count"], int)
        assert count_data["count"] >= 0

    # =============================================================================
    # GET /agents/exists/{slug} - Check if agent exists by slug
    # =============================================================================
    
    def test_check_agent_exists_true(self, e2e_test_client, sample_agent_data):
        """Test GET /agents/exists/{slug} - Success scenario: agent exists"""
        # First create an agent
        agent = Agent(**sample_agent_data)
        agent.slug = "test-exists-true"  # Unique slug
        create_response = e2e_test_client.post("/create-agent", json=self._get_serializable_agent_data(agent))
        assert create_response.status_code == 200
        
        # Check if agent exists
        response = e2e_test_client.get(f"/agents/exists/{agent.slug}")
        
        assert response.status_code == 200
        exists_data = response.json()
        assert "exists" in exists_data
        assert exists_data["exists"] is True

    def test_check_agent_exists_false(self, e2e_test_client):
        """Test GET /agents/exists/{slug} - Success scenario: agent doesn't exist"""
        non_existent_slug = "definitely-non-existent-agent"
        response = e2e_test_client.get(f"/agents/exists/{non_existent_slug}")
        
        assert response.status_code == 200
        exists_data = response.json()
        assert "exists" in exists_data
        assert exists_data["exists"] is False
    
    # =============================================================================
    # New SEO and Marketing Agents E2E Tests
    # =============================================================================
    
    def test_website_audit_agent_exists(self, e2e_test_client):
        """Test that website audit agent exists in database"""
        response = e2e_test_client.get("/agents/slug/website-audit")
        assert response.status_code == 200
        agent_data = response.json()
        assert agent_data["slug"] == "website-audit"
        assert agent_data["name"] == "Website Performance Auditor"

    def test_seo_audit_agent_exists(self, e2e_test_client):
        """Test that SEO audit agent exists in database"""
        response = e2e_test_client.get("/agents/slug/seo-audit")
        assert response.status_code == 200
        agent_data = response.json()
        assert agent_data["slug"] == "seo-audit"
        assert agent_data["name"] == "SEO Auditor Agent"

    def test_marketing_copy_agent_exists(self, e2e_test_client):
        """Test that marketing copy agent exists in database"""
        response = e2e_test_client.get("/agents/slug/marketing-copy")
        assert response.status_code == 200
        agent_data = response.json()
        assert agent_data["slug"] == "marketing-copy"
        assert agent_data["name"] == "Marketing Copywriter Agent"

    @pytest.mark.skipif(
        os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true",
        reason="Skipping tests that make external API calls"
    )
    def test_run_website_audit_agent(self, e2e_test_client):
        """Test running website audit agent"""
        # Get agent by slug
        agent_response = e2e_test_client.get("/agents/slug/website-audit")
        assert agent_response.status_code == 200
        agent_id = agent_response.json()["id"]
        
        # Run agent with website URL
        request_data = {
            "prompt": "https://example.com",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{agent_id}", json=request_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0

    @pytest.mark.skipif(
        os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true",
        reason="Skipping tests that make external API calls"
    )
    def test_run_seo_audit_agent(self, e2e_test_client):
        """Test running SEO audit agent"""
        # Get agent by slug
        agent_response = e2e_test_client.get("/agents/slug/seo-audit")
        assert agent_response.status_code == 200
        agent_id = agent_response.json()["id"]
        
        # Run agent with website URL and keywords
        request_data = {
            "prompt": "https://example.com keywords: seo, marketing, optimization",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{agent_id}", json=request_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0

    @pytest.mark.skipif(
        os.environ.get("SKIP_EXTERNAL_CALLS", "true").lower() == "true",
        reason="Skipping tests that make external API calls"
    )
    def test_run_marketing_copy_agent(self, e2e_test_client):
        """Test running marketing copy agent"""
        # Get agent by slug
        agent_response = e2e_test_client.get("/agents/slug/marketing-copy")
        assert agent_response.status_code == 200
        agent_id = agent_response.json()["id"]
        
        # Run agent with website URL and audience info
        request_data = {
            "prompt": "https://example.com audience: tech startups, SaaS companies",
            "user_email": "test@example.com"
        }
        response = e2e_test_client.post(f"/run-agent/{agent_id}", json=request_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data
        assert isinstance(response_data["response"], str)
        assert len(response_data["response"]) > 0

    def test_new_agents_count_in_total(self, e2e_test_client):
        """Test that the new agents are included in the total count"""
        response = e2e_test_client.get("/agents/count")
        assert response.status_code == 200
        count_data = response.json()
        # Should include the 3 new agents plus existing ones (11 total from seed)
        assert count_data["count"] >= 11

    def test_new_agents_in_agents_list(self, e2e_test_client):
        """Test that the new agents appear in the agents list"""
        response = e2e_test_client.get("/agents")
        assert response.status_code == 200
        agents = response.json()
        
        # Extract slugs from agents list
        agent_slugs = [agent["slug"] for agent in agents]
        
        # Verify new agents are present
        assert "website-audit" in agent_slugs
        assert "seo-audit" in agent_slugs
        assert "marketing-copy" in agent_slugs
