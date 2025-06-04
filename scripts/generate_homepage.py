"""
Sample script showing how to use the Homepage Generator Agent.
"""
import os
import sys
import asyncio
from pathlib import Path

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents.homepage_generator import HomepageGeneratorAgent


async def generate_homepage(url, output_format="markdown", output_file=None):
    """
    Generate a homepage for the specified URL.
    
    Args:
        url: The URL of the website to analyze
        output_format: The desired output format ("markdown" or "html")
        output_file: Optional path to save the output
        
    Returns:
        The generated homepage content
    """
    print(f"Generating homepage content for: {url}")
    
    # Create the generator agent
    generator = HomepageGeneratorAgent()
    
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
    
    parser = argparse.ArgumentParser(description="Generate website homepage content")
    parser.add_argument("--url", help="URL of the website to analyze")
    parser.add_argument("--format", choices=["markdown", "html"], default="markdown",
                      help="Output format (default: markdown)")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    # Run the generator
    content = asyncio.run(generate_homepage(
        url=args.url,
        output_format=args.format,
        output_file=args.output
    ))
    
    # Print a preview if not saving to file
    if not args.output:
        print("\nGenerated Content Preview (first 500 chars):\n")
        print(content[:500])
        print("...\n")
    
    print("Homepage generation complete!")


if __name__ == "__main__":
    main()
