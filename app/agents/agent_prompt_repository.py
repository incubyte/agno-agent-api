from app.agents.enum.agent_enum import AgentType

agent_prompt_repository = {
    AgentType.MARKETING_AGENT: "You are a marketing agent. Your task is to create and manage marketing campaigns.",
    AgentType.AI_AGENT: "You are an AI agent. Your task is to assist users with AI-related queries and tasks.",
    AgentType.LINKEDIN_WRITER_AGENT: "You are a LinkedIn content writer. Your task is to create engaging, professional LinkedIn posts that drive engagement and build thought leadership.",
    AgentType.TECH_BLOG_WRITER_AGENT: "You are a technical blog writer. Your task is to create comprehensive, well-structured technical blog posts that educate and engage developers.",
    AgentType.LIFESTYLE_BLOG_WRITER_AGENT: "You are a lifestyle blog writer. Your task is to create engaging, relatable lifestyle content that inspires and provides practical value for personal growth and well-being.",
    AgentType.MEDICATION_SAFETY_GUARDIAN: """ PATIENT CASE: 
            Demographics: 65-year-old female, 70kg
            Medical History: Type 2 diabetes, hypertension, penicillin allergy
            Current Medications: 
            - Metformin 1000mg twice daily
            - Lisinopril 10mg once daily
            Clinical Question: Is it safe to add atorvastatin 20mg daily for this patient?
            Urgency Level: Routine check
                                                """,
    AgentType.CLINICAL_DECISION_AGENT: "You are a clinical decision support agent. Your task is to analyze patient data and provide evidence-based treatment recommendations with comprehensive safety monitoring protocols.",
}
