"""
Sample script showing enhanced homepage generation with option for single agent or team approach.
"""
import os
import sys
import asyncio
from pathlib import Path
from typing import Optional, Literal, Union

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.homepage_generator import HomepageGeneratorAgent
from app.agents.homepage_generator_team import HomepageGeneratorAgentTeam


class EnhancedHomepageGenerator:
    """
    Enhanced homepage generator that supports both single-agent and team-based approaches.
    """
    
    def __init__(self, approach: Literal["single", "team"] = "team"):
        """
        Initialize the enhanced homepage generator.
        
        Args:
            approach: The approach to use - either "single" for the original single agent
                    or "team" for the team-based approach (default)
        """
        self.approach = approach
        if approach == "single":
            self.generator = HomepageGeneratorAgent()
        else:  # team approach
            self.generator = HomepageGeneratorAgentTeam()
    
    async def generate_homepage(self, url: str, output_format: str = "markdown") -> str:
        """
        Generate a homepage for the specified URL.
        
        Args:
            url: The URL of the website to analyze
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            The generated homepage content
        """
        if self.approach == "single":
            return await self.generator.generate_homepage(url, output_format)
        else:  # team approach
            return await self.generator.generate_homepage(url, output_format)
            

async def generate_homepage(url, output_format="markdown", output_file=None, approach="team"):
    """
    Generate a homepage for the specified URL.
    
    Args:
        url: The URL of the website to analyze
        output_format: The desired output format ("markdown" or "html")
        output_file: Optional path to save the output
        approach: The approach to use - either "single" for the original single agent
                or "team" for the team-based approach (default)
        
    Returns:
        The generated homepage content
    """
    print(f"Generating homepage content for: {url} using {approach} approach")
    
    # Create the generator
    generator = EnhancedHomepageGenerator(approach)
    
    # Generate the homepage
    content = await generator.generate_homepage(url, output_format)
    
    # Save to file if requested
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(exist_ok=True, parents=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        print(f"Homepage content saved to: {output_path.absolute()}")
    
    return content


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate website homepage content with enhanced options")
    parser.add_argument("--url", help="URL of the website to analyze", required=True)
    parser.add_argument("--format", choices=["markdown", "html"], default="markdown",
                      help="Output format (default: markdown)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--approach", choices=["single", "team"], default="team",
                      help="Generation approach - single agent or team (default: team)")
    
    args = parser.parse_args()
    
    # Run the generator
    content = asyncio.run(generate_homepage(
        url=args.url,
        output_format=args.format,
        output_file=args.output,
        approach=args.approach
    ))
    
    # Print a preview if not saving to file
    if not args.output:
        print("\nGenerated Content Preview (first 500 chars):\n")
        print(content[:500])
        print("...\n")
    
    print("Homepage generation complete!")


if __name__ == "__main__":
    main()
