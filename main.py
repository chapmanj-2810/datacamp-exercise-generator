"""
DataCamp Exercise Generator - CLI and Examples

This provides both a CLI and example functions for easy notebook usage.
"""

import argparse
from .core import LearningDesigner, load_video_content


def generate_exercises_intelligent(video_file: str, objectives: list[str] = None, exercise_types: list[str] = None, model: str = "gpt-4o") -> list[str]:
    """
    Generate exercises using intelligent design.
    
    Perfect for Jupyter notebooks and Python scripts.
    
    Args:
        video_file: Path to video transcript
        objectives: Optional learning objectives  
        exercise_types: Optional list of exercise types to use (e.g., ["single_mcq", "drag_drop_classify"])
                       If provided, exercises will be distributed across these types instead of auto-selected
        model: OpenAI model to use
        
    Returns:
        List of formatted exercise strings
    """
    video_content = load_video_content(video_file)
    designer = LearningDesigner(model=model)
    
    learning_plan = designer.create_learning_plan(video_content, objectives, exercise_types)
    return designer.execute_learning_plan(video_content, learning_plan)


def print_exercises(exercises: list[str]):
    """Helper function to print exercises with separators."""
    for i, exercise in enumerate(exercises, 1):
        if i > 1:
            print("\n---\n")
        print(exercise)


# CLI functionality
def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Generate DataCamp exercises from video content")
    
    parser.add_argument("video_file", help="Path to the video transcript markdown file")
    parser.add_argument("--objectives", nargs="+", help="Learning objectives (optional)")
    parser.add_argument("--exercise-types", nargs="+", 
                       choices=["single_mcq", "multiple_mcq", "drag_drop_classify", "drag_drop_order", "coding"],
                       help="Specific exercise types to use (optional)")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--output", help="Output file (optional, prints to stdout if not provided)")
    
    args = parser.parse_args()
    
    # Warn about GPT-5 temperature restrictions upfront
    if args.model.startswith("gpt-5"):
        print(f"Note: {args.model} automatically uses temperature=1.0 (required by OpenAI)")
    
    try:
        # Generate exercises using intelligent design
        exercises = generate_exercises_intelligent(
            args.video_file, 
            args.objectives, 
            getattr(args, 'exercise_types', None),  # Handle hyphenated argument
            args.model
        )
        
        # Format output
        output = "\n---\n".join(exercises)
        
        # Write to file or print
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Exercises written to {args.output}")
        else:
            print(output)
            
    except FileNotFoundError:
        print(f"Error: Video file '{args.video_file}' not found.")
    except Exception as e:
        print(f"Error generating exercises: {e}")


if __name__ == "__main__":
    main()
