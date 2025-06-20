# Migration Guide: Old vs New Agent Structure

## Overview
This guide helps you migrate from the old monolithic `agent_system.py` to the new modular agent structure.

## Before (Old Structure)
```python
# Old way - everything in one file
from app.agents.agent_system import AgentFactory, AgentType, BaseAgent

# Create agents
agent = AgentFactory.get_agent(AgentType.MARKETING_AGENT)
```

## After (New Structure)
```python
# New way - modular imports
from app.agents.enum import AgentType
from app.agents.agent_factory import AgentFactory
from app.agents import MarketingAgent

# Option 1: Use factory (same as before)
agent = AgentFactory.get_agent(AgentType.MARKETING_AGENT)

# Option 2: Direct import (new capability)
agent = MarketingAgent()
```

## Migration Steps

### 1. Update Import Statements

#### Old Imports ❌
```python
from app.agents.agent_system import AgentFactory, AgentType, BaseAgent
from app.agents.agent_system import MarketingAgent, TechBlogWriter
```

#### New Imports ✅
```python
# For enums
from app.agents.enum import AgentType

# For factory pattern
from app.agents.agent_factory import AgentFactory

# For base class
from app.agents.base_agent import BaseAgent

# For specific agents (new capability)
from app.agents import MarketingAgent, LinkedInWriterAgent, TechBlogWriterAgent, LifestyleBlogWriterAgent

# Or import individual agents
from app.agents.marketing_agents import MarketingAgent
from app.agents.lifestyle_blog_writer_agent import LifestyleBlogWriterAgent
```

### 2. Update Agent Enum Values

#### Old Enum Values ❌
```python
AgentType.MARKETING_AGENT        # "marketing-agent"
AgentType.TECH_BLOG_WRITER       # "tech-blog-writer"  
AgentType.LINKEDIN_WRITER        # "linkedin-writer"
AgentType.LIFESTYLE_BLOG_WRITER  # "lifestyle-blog-writer"
```

#### New Enum Values ✅
```python
AgentType.MARKETING_AGENT            # "marketing-agent"
AgentType.TECH_BLOG_WRITER           # "tech-blog-writer"
AgentType.LINKEDIN_WRITER            # "linkedin-writer"
AgentType.LIFESTYLE_BLOG_WRITER      # "lifestyle-blog-writer"
```

### 3. Update Class Names

#### Old Class Names ❌
```python
TechBlogWriter       # Old name
LinkedInWriter       # Old name
LifestyleBlogWriter  # Old name
```

#### New Class Names ✅
```python
TechBlogWriterAgent       # New name
LinkedInWriterAgent       # New name
LifestyleBlogWriterAgent  # New name
MarketingAgent           # Unchanged
```

## Code Examples

### Creating Agents

#### Old Way
```python
from app.agents.agent_system import AgentFactory, AgentType

# Only way to create agents
marketing_agent = AgentFactory.get_agent(AgentType.MARKETING_AGENT)
tech_agent = AgentFactory.get_agent(AgentType.TECH_BLOG_WRITER)
```

#### New Way
```python
from app.agents.enum import AgentType
from app.agents.agent_factory import AgentFactory
from app.agents import MarketingAgent, TechBlogWriterAgent

# Method 1: Factory pattern (backward compatible)
marketing_agent = AgentFactory.get_agent(AgentType.MARKETING_AGENT)
tech_agent = AgentFactory.get_agent(AgentType.TECH_BLOG_WRITER)

# Method 2: Direct instantiation (new!)
marketing_agent = MarketingAgent()
tech_agent = TechBlogWriterAgent()
```

### Using Agents

#### Usage (No Change)
```python
# This part stays exactly the same
response = agent.get_response("Create a marketing strategy")
print(response)
```

### Custom Agent Development

#### Old Way
```python
# Had to modify the large agent_system.py file
class MyCustomAgent(BaseAgent):
    # Implementation
    pass

# Add to factory in same file
class AgentFactory:
    _agents = {
        # ... existing agents
        AgentType.MY_CUSTOM: MyCustomAgent  # Add here
    }
```

#### New Way
```python
# Create a new file: app/agents/my_custom_agent.py
from .base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="My Custom Agent",
            description="Description of what it does"
        )
    
    def get_response(self, prompt: str, **kwargs) -> str:
        # Implementation
        return "Custom response"

# Add to enum: app/agents/enum/agent_enum.py
class AgentType(Enum):
    # ... existing types
    MY_CUSTOM_AGENT = "my-custom-agent"

# Add to factory: app/agents/agent_factory.py  
from .my_custom_agent import MyCustomAgent

class AgentFactory:
    _agents = {
        # ... existing agents
        AgentType.MY_CUSTOM_AGENT: MyCustomAgent
    }

# Add to package: app/agents/__init__.py
from .my_custom_agent import MyCustomAgent

__all__ = [
    # ... existing exports
    "MyCustomAgent"
]
```

## Benefits of New Structure

### ✅ **Advantages**
- **Modularity**: Each agent in its own file
- **Maintainability**: Easier to find and modify specific agents
- **Scalability**: Simple to add new agents
- **Clean Imports**: Import only what you need
- **Better IDE Support**: Better autocompletion and navigation
- **Reduced Conflicts**: Less merge conflicts when multiple developers work on different agents

### 🔄 **Backward Compatibility**
- Factory pattern still works exactly the same
- Existing code using `AgentFactory.get_agent()` requires minimal changes
- All agent functionality preserved

### 🆕 **New Capabilities**
- Direct agent instantiation: `MarketingAgent()`
- Selective imports: `from app.agents import MarketingAgent`
- Cleaner file organization
- Easier testing of individual agents

## Quick Migration Checklist

- [ ] Update import statements to use new paths
- [ ] Update enum values (add `_AGENT` suffix where needed)
- [ ] Update class names (add `Agent` suffix where needed)  
- [ ] Test that existing functionality still works
- [ ] Consider using direct imports for better performance
- [ ] Update any custom agents to follow new file structure

## Need Help?

If you encounter issues during migration:

1. **Check the test script**: Run `python test_agent_structure.py`
2. **Verify imports**: Make sure all import paths are updated
3. **Check enum values**: Ensure you're using the correct enum values
4. **Review the backup**: The original `agent_system.py.backup` is available for reference

The migration should be straightforward, and the new structure provides much better organization while maintaining full backward compatibility! 🚀
