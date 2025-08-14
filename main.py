"""
DataCamp Exercise Generator - Main Usage Examples

This file demonstrates different ways to use the exercise generator system.
"""

from .core import LearningDesigner, load_video_content
from .generators import get_exercise_generator


def main():
    """Main function demonstrating different usage patterns."""
    try:
        # Load video content
        video_content = load_video_content('conceptual_video.md')
        
        # Create learning designer
        designer = LearningDesigner(model="gpt-4o")
        
        # OPTION 1: Intelligent design with your own learning objectives
        learning_objectives = [
            "Understand what fragile evaluation is and why it's problematic",
            "Identify strategies for robust evaluation of AI systems",
            "Recognize the importance of diverse, real-world testing scenarios"
        ]
        
        learning_plan = designer.create_learning_plan(video_content, learning_objectives)
        exercises = designer.execute_learning_plan(video_content, learning_plan, use_plan_objectives=True)
        
        # OPTION 2: Intelligent design with auto-generated objectives
        # learning_plan = designer.create_learning_plan(video_content, provided_objectives=None)
        # exercises = designer.execute_learning_plan(video_content, learning_plan, use_plan_objectives=True)
        
        # OPTION 3: Manual single-type generation
        # generator = get_exercise_generator("single_mcq", model="gpt-4o")
        # exercises = generator.generate_markdown_exercises(video_content, learning_objectives)
        
        # Output the exercises
        for i, exercise_md in enumerate(exercises, 1):
            if i > 1:
                print("\n---\n")
            print(exercise_md)
            
    except FileNotFoundError:
        print("Error: 'conceptual_video.md' file not found. Please ensure the file exists in the current directory.")
    except Exception as e:
        print(f"Error in learning design process: {e}")


if __name__ == "__main__":
    main()
