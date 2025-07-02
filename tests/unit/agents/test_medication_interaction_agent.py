"""
Test file for Medication Interaction Agent
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.agents.medication_interaction_agent import MedicationInteractionAgent
from app.agents.enum.agent_enum import AgentType


class TestMedicationInteractionAgent:
    
    def setup_method(self):
        """Setup test fixtures"""
        with patch('app.agents.medication_interaction_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_storage.db"
            self.agent = MedicationInteractionAgent()
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        assert self.agent is not None
        assert hasattr(self.agent, 'medication_team')
        assert hasattr(self.agent, 'drug_search_tool')
    
    @patch('app.agents.medication_interaction_agent.Claude')
    def test_drug_parser_agent_creation(self, mock_claude):
        """Test drug parser agent is created with correct configuration"""
        parser_agent = self.agent.create_drug_parser_agent()
        
        assert parser_agent is not None
        assert parser_agent.name == "Drug Parser & Standardization Agent"
        assert "pharmaceutical data specialist" in parser_agent.role
    
    @patch('app.agents.medication_interaction_agent.Claude')
    def test_interaction_detector_agent_creation(self, mock_claude):
        """Test interaction detector agent is created correctly"""
        detector_agent = self.agent.create_interaction_detector_agent()
        
        assert detector_agent is not None
        assert detector_agent.name == "Interaction Detection & Risk Assessment Agent"
        assert "clinical pharmacologist" in detector_agent.role
    
    @patch('app.agents.medication_interaction_agent.Claude')
    def test_patient_context_agent_creation(self, mock_claude):
        """Test patient context agent is created correctly"""
        context_agent = self.agent.create_patient_context_agent()
        
        assert context_agent is not None
        assert context_agent.name == "Patient Context & Personalization Agent"
        assert "clinical pharmacist" in context_agent.role
    
    @patch('app.agents.medication_interaction_agent.Claude')
    def test_alert_generator_agent_creation(self, mock_claude):
        """Test alert generator agent is created correctly"""
        alert_agent = self.agent.create_alert_generator_agent()
        
        assert alert_agent is not None
        assert alert_agent.name == "Alert Generation & Recommendation Agent"
        assert "clinical communication specialist" in alert_agent.role
    
    def test_might_be_drug_method(self):
        """Test the drug detection heuristic"""
        # Should return True for potential drug names
        assert self.agent._might_be_drug("aspirin") == True
        assert self.agent._might_be_drug("metformin") == True
        
        # Should return False for common words
        assert self.agent._might_be_drug("patient") == False
        assert self.agent._might_be_drug("taking") == False
        assert self.agent._might_be_drug("drug") == False
        
        # Should return False for short words
        assert self.agent._might_be_drug("is") == False
        assert self.agent._might_be_drug("the") == False
    
    @patch.object(MedicationInteractionAgent, '_create_medication_interaction_team')
    def test_get_response_basic_functionality(self, mock_team):
        """Test basic get_response functionality"""
        # Mock the team response
        mock_response = Mock()
        mock_response.content = "# Test Analysis\nNo interactions found."
        mock_team.return_value.run.return_value = [mock_response]
        
        # Test basic prompt (note: using 'url' parameter for BaseAgent compatibility)
        response = self.agent.get_response("Check aspirin and warfarin interaction")
        
        # Verify that the team was called
        mock_team.return_value.run.assert_called_once()
        assert "Test Analysis" in response
    
    @patch('app.tools.duckduckgo_search.FreeDrugSearchTool')
    def test_enhance_with_search(self, mock_search_tool):
        """Test search enhancement functionality"""
        # Mock search tool
        mock_search_instance = Mock()
        mock_search_instance.search_drug_info.return_value = "Aspirin: Common pain reliever and anti-inflammatory drug..."
        mock_search_tool.return_value = mock_search_instance
        
        # Create fresh agent with mocked search tool
        with patch('app.agents.medication_interaction_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_storage.db"
            agent = MedicationInteractionAgent()
            agent.drug_search_tool = mock_search_instance
        
        # Test enhancement
        result = agent._enhance_with_search("Check aspirin and warfarin")
        
        # Should have attempted to search for potential drugs
        assert "aspirin" in result.lower() or "search" in result.lower()
    
    def test_error_handling_in_get_response(self):
        """Test error handling in get_response method"""
        # Mock the team to raise an exception
        with patch.object(self.agent, 'medication_team') as mock_team:
            mock_team.run.side_effect = Exception("Test error")
            
            response = self.agent.get_response("test prompt")
            
            # Should return error message
            assert "Error in Medication Analysis" in response
            assert "Test error" in response


class TestMedicationAgentIntegration:
    """Integration tests for medication agent"""
    
    def test_agent_type_enum_exists(self):
        """Test that the agent type is properly defined"""
        assert hasattr(AgentType, 'MEDICATION_INTERACTION_AGENT')
        assert AgentType.MEDICATION_INTERACTION_AGENT.value == "medication-interaction"
    
    def test_agent_factory_integration(self):
        """Test that the agent can be created through factory"""
        from app.agents.agent_factory import AgentFactory
        
        # This should not raise an exception
        agent = AgentFactory.get_agent(AgentType.MEDICATION_INTERACTION_AGENT)
        assert isinstance(agent, MedicationInteractionAgent)
    
    def test_agent_prompt_repository_integration(self):
        """Test that the agent prompt is defined"""
        from app.agents.agent_prompt_repository import agent_prompt_repository
        
        prompt = agent_prompt_repository.get(AgentType.MEDICATION_INTERACTION_AGENT)
        assert prompt is not None
        assert "medication interaction specialist" in prompt.lower()


# Example usage tests
class TestMedicationAgentUsage:
    """Test real usage scenarios"""
    
    def setup_method(self):
        with patch('app.agents.medication_interaction_agent.settings') as mock_settings:
            mock_settings.AGENT_STORAGE = "test_storage.db"
            self.agent = MedicationInteractionAgent()
    
    @patch.object(MedicationInteractionAgent, '_create_medication_interaction_team')
    def test_simple_drug_interaction_query(self, mock_team):
        """Test a simple drug interaction query"""
        # Mock response
        mock_response = Mock()
        mock_response.content = """
        # Drug Interaction Analysis
        
        ## Drugs Analyzed
        - Aspirin 81mg
        - Warfarin 5mg
        
        ## Interaction Found
        **Severity**: Major
        **Mechanism**: Additive anticoagulant effects
        **Recommendation**: Monitor INR closely
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("Check interaction between aspirin and warfarin")
        
        assert "Drug Interaction Analysis" in response
        assert "Major" in response
        assert "anticoagulant" in response
    
    @patch.object(MedicationInteractionAgent, '_create_medication_interaction_team')
    def test_multiple_drug_analysis(self, mock_team):
        """Test analysis of multiple drugs"""
        mock_response = Mock()
        mock_response.content = """
        # Comprehensive Medication Analysis
        
        ## Executive Summary
        Multiple interactions detected requiring attention.
        
        ## Drug List
        1. Aspirin 81mg daily
        2. Warfarin 5mg daily  
        3. Metformin 500mg twice daily
        
        ## Interactions
        - Aspirin + Warfarin: Major interaction
        - No other significant interactions
        """
        mock_team.return_value.run.return_value = [mock_response]
        
        response = self.agent.get_response("Analyze medications: aspirin 81mg, warfarin 5mg, metformin 500mg")
        
        assert "Comprehensive Medication Analysis" in response
        assert "Multiple interactions" in response


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
