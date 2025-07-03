from enum import Enum


class AgentType(Enum):
    MARKETING_AGENT = "marketing-agent"
    AI_AGENT = "ai-agent"
    LINKEDIN_WRITER_AGENT = "linkedin-writer-agent"
    TECH_BLOG_WRITER_AGENT = "tech-blog-writer-agent"
    LIFESTYLE_BLOG_WRITER_AGENT = "lifestyle-blog-writer-agent"
    WEBSITE_PERFORMANCE_AUDITOR = "website-audit"
    SEO_AUDIT = "seo-audit"
    MARKETING_COPYWRITER_AGENT = "marketing-copy"
    SALES_INTELLIGENCE_AGENT = "lead-enrichment"
    COMPETITIVE_INSIGHT_AGENT = "competitor-analysis"
    NEWS_AGGREGATOR_AGENT = "news-aggregator"
    BRAND_VISIBILITY_AGENT = "company-presence"
    DRUG_SAFETY_MONITOR_AGENT = "drug-safety-monitor"
    MEDICATION_SAFETY_GUARDIAN = "patient-medication"
    MEDICATION_INTERACTION_MONITOR_AGENT = "drug-interaction-assessment"
    MEDICATION_INTERACTION_AGENT = "drug-interaction-assessment"
    LOCATION_HEALTH_INTELLIGENCE_AGENT = "geo-health-alerts"
    CLINICAL_DECISION_AGENT = "safety-insights"
    
    # Sub-agent enums (for internal prompt access)
    GEOGRAPHIC_CONTEXT_AGENT = "geographic-context"
    EPIDEMIOLOGICAL_INTELLIGENCE_AGENT = "epidemiological-intelligence"
    HEALTHCARE_RESOURCE_MAPPING_AGENT = "healthcare-resource-mapping"
    RISK_ASSESSMENT_ALERT_AGENT = "risk-assessment-alert"