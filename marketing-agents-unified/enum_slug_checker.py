#!/usr/bin/env python3
"""
Enum and Slug Verification Script
Thoroughly checks all enum values, slugs, and their consistency across the codebase.
"""

import sys
import os
from pathlib import Path

# Add the app directory to path for testing
app_path = Path(__file__).parent / 'app'
sys.path.insert(0, str(app_path))

def check_enum_definitions():
    """Check that enum definitions are correct"""
    print("🔍 Checking enum definitions...")
    
    try:
        from app.agents.enum import AgentType
        
        print("✅ AgentType imported successfully")
        print("📋 Current enum values:")
        
        for agent_type in AgentType:
            print(f"   {agent_type.name} = \"{agent_type.value}\"")
        
        # Verify expected values
        expected_values = {
            "MARKETING_AGENT": "marketing-agent",
            "TECH_BLOG_WRITER": "tech-blog-writer", 
            "LINKEDIN_WRITER": "linkedin-writer",
            "LIFESTYLE_BLOG_WRITER": "lifestyle-blog-writer"
        }
        
        print("\n🎯 Verifying expected values:")
        errors = []
        
        for enum_name, expected_value in expected_values.items():
            try:
                enum_member = getattr(AgentType, enum_name)
                if enum_member.value == expected_value:
                    print(f"   ✅ {enum_name}: {expected_value}")
                else:
                    error_msg = f"{enum_name} has value '{enum_member.value}' but expected '{expected_value}'"
                    errors.append(error_msg)
                    print(f"   ❌ {error_msg}")
            except AttributeError:
                error_msg = f"Missing enum member: {enum_name}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        return errors
        
    except Exception as e:
        print(f"❌ Failed to import AgentType: {e}")
        return [f"Enum import failed: {e}"]

def check_factory_mapping():
    """Check that factory properly maps all enum values"""
    print("\n🏭 Checking factory mapping...")
    
    try:
        from app.agents.enum import AgentType
        from app.agents.agent_factory import AgentFactory
        
        print("✅ Factory imported successfully")
        
        errors = []
        enum_values = set(AgentType)
        factory_keys = set(AgentFactory._agents.keys())
        
        print(f"📊 Enum has {len(enum_values)} values, Factory has {len(factory_keys)} mappings")
        
        # Check for missing mappings
        missing_in_factory = enum_values - factory_keys
        if missing_in_factory:
            for missing in missing_in_factory:
                error_msg = f"Enum value {missing.name} ({missing.value}) missing in factory"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        # Check for extra mappings
        extra_in_factory = factory_keys - enum_values
        if extra_in_factory:
            for extra in extra_in_factory:
                error_msg = f"Factory has extra mapping for {extra.name} ({extra.value})"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        # Test each mapping
        print("\n🧪 Testing factory agent creation:")
        for agent_type in AgentType:
            try:
                agent = AgentFactory.get_agent(agent_type)
                print(f"   ✅ {agent_type.name} → {agent.__class__.__name__}: {agent.name}")
            except Exception as e:
                error_msg = f"Factory failed to create agent for {agent_type.name}: {e}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        return errors
        
    except Exception as e:
        print(f"❌ Factory mapping check failed: {e}")
        return [f"Factory mapping check failed: {e}"]

def check_service_integration():
    """Check service layer integration with enum values"""
    print("\n🔗 Checking service integration...")
    
    try:
        from app.agents.enum import AgentType
        
        # Simulate what the service does: AgentType(agent.slug)
        print("🎯 Testing slug-to-enum conversion:")
        
        slug_mappings = {
            "marketing-agent": "MARKETING_AGENT",
            "tech-blog-writer": "TECH_BLOG_WRITER",
            "linkedin-writer": "LINKEDIN_WRITER", 
            "lifestyle-blog-writer": "LIFESTYLE_BLOG_WRITER"
        }
        
        errors = []
        for slug, expected_enum_name in slug_mappings.items():
            try:
                # This is what the service layer does
                agent_type = AgentType(slug)
                if agent_type.name == expected_enum_name:
                    print(f"   ✅ \"{slug}\" → {agent_type.name}")
                else:
                    error_msg = f"Slug '{slug}' mapped to {agent_type.name} but expected {expected_enum_name}"
                    errors.append(error_msg)
                    print(f"   ❌ {error_msg}")
            except ValueError:
                error_msg = f"Slug '{slug}' cannot be converted to AgentType enum"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        return errors
        
    except Exception as e:
        print(f"❌ Service integration check failed: {e}")
        return [f"Service integration check failed: {e}"]

def check_legacy_compatibility():
    """Check compatibility with legacy marketing agent endpoint"""
    print("\n🔄 Checking legacy compatibility...")
    
    try:
        from app.agents.enum import AgentType
        
        # The router looks for "marketing-agent" by slug
        expected_marketing_slug = "marketing-agent"
        
        try:
            marketing_type = AgentType(expected_marketing_slug)
            if marketing_type.name == "MARKETING_AGENT":
                print(f"   ✅ Legacy marketing slug '{expected_marketing_slug}' works correctly")
                return []
            else:
                error_msg = f"Marketing slug maps to wrong enum: {marketing_type.name}"
                print(f"   ❌ {error_msg}")
                return [error_msg]
        except ValueError:
            error_msg = f"Legacy marketing slug '{expected_marketing_slug}' not found in enum"
            print(f"   ❌ {error_msg}")
            return [error_msg]
            
    except Exception as e:
        print(f"❌ Legacy compatibility check failed: {e}")
        return [f"Legacy compatibility check failed: {e}"]

def check_class_name_consistency():
    """Check that class names are consistent with enum names"""
    print("\n🏗️ Checking class name consistency...")
    
    try:
        from app.agents.enum import AgentType
        from app.agents.agent_factory import AgentFactory
        
        # Expected class mappings
        expected_classes = {
            AgentType.MARKETING_AGENT: "MarketingAgent",
            AgentType.TECH_BLOG_WRITER: "TechBlogWriterAgent", 
            AgentType.LINKEDIN_WRITER: "LinkedInWriterAgent",
            AgentType.LIFESTYLE_BLOG_WRITER: "LifestyleBlogWriterAgent"
        }
        
        errors = []
        for agent_type, expected_class_name in expected_classes.items():
            try:
                agent = AgentFactory.get_agent(agent_type)
                actual_class_name = agent.__class__.__name__
                
                if actual_class_name == expected_class_name:
                    print(f"   ✅ {agent_type.name} → {actual_class_name}")
                else:
                    error_msg = f"{agent_type.name} creates {actual_class_name} but expected {expected_class_name}"
                    errors.append(error_msg)
                    print(f"   ❌ {error_msg}")
                    
            except Exception as e:
                error_msg = f"Failed to check class for {agent_type.name}: {e}"
                errors.append(error_msg)
                print(f"   ❌ {error_msg}")
        
        return errors
        
    except Exception as e:
        print(f"❌ Class name consistency check failed: {e}")
        return [f"Class name consistency check failed: {e}"]

def main():
    """Run all enum and slug checks"""
    print("🔍 COMPREHENSIVE ENUM AND SLUG VERIFICATION")
    print("=" * 60)
    
    all_errors = []
    
    # Run all checks
    all_errors.extend(check_enum_definitions())
    all_errors.extend(check_factory_mapping())
    all_errors.extend(check_service_integration())
    all_errors.extend(check_legacy_compatibility())
    all_errors.extend(check_class_name_consistency())
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION RESULTS")
    
    if all_errors:
        print(f"❌ FOUND {len(all_errors)} ISSUES:")
        for i, error in enumerate(all_errors, 1):
            print(f"   {i}. {error}")
        print("\n🔧 Please fix these issues for proper enum/slug consistency.")
        return 1
    else:
        print("🎉 ALL ENUM AND SLUG CHECKS PASSED!")
        print("✅ Perfect consistency across the entire system.")
        print("\n📋 Summary:")
        print("   • Enum definitions are correct")
        print("   • Factory mappings are complete") 
        print("   • Service integration works properly")
        print("   • Legacy compatibility maintained")
        print("   • Class names are consistent")
        print("\n🚀 The enum/slug system is ready for production!")
        return 0

if __name__ == "__main__":
    exit(main())
