"""
LinkedIn Writer Agent Implementation
AI specialist in professional LinkedIn content and networking posts.
"""

from .base_agent import BaseAgent


class LinkedInWriterAgent(BaseAgent):
    """LinkedIn content creation agent"""
    
    def __init__(self):
        super().__init__(
            name="LinkedIn Content Writer", 
            description="An AI specialist in professional LinkedIn content and networking posts."
        )
    
    def get_response(self, prompt: str, **kwargs) -> str:
        """Generate LinkedIn post content"""
        return f"""
**LinkedIn Post**

🚀 {prompt}

Here's what I've learned:

✅ Key insight #1: Professional growth requires continuous learning
✅ Key insight #2: Networking is about building genuine relationships
✅ Key insight #3: Sharing knowledge creates value for the community

💡 **My takeaway:** Success in today's professional landscape demands adaptability and collaboration.

What's your experience with {prompt.lower()}? Share your thoughts in the comments!

#ProfessionalDevelopment #Leadership #CareerGrowth #Networking

---
*Follow for more insights on professional development and industry trends.*
        """
