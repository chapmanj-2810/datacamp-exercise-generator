"""
Utility functions for the exercise generator.
"""


def load_video_content(filepath: str) -> str:
    """Load video transcript content from markdown file."""
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()
