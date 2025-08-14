"""
Utility functions for the exercise generator.
"""

from .content_extractor import extract_video_content


def load_video_content(filepath: str, extract_content: bool = True) -> str:
    """
    Load video transcript content from markdown file.
    
    Args:
        filepath: Path to the video transcript file
        extract_content: If True, extracts only meaningful content (scripts, titles, slide content)
                        If False, returns raw file content
    
    Returns:
        Video content (extracted or raw based on extract_content parameter)
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        raw_content = file.read()
    
    if extract_content:
        return extract_video_content(raw_content)
    else:
        return raw_content


def load_video_content_raw(filepath: str) -> str:
    """Load raw video transcript content without any extraction."""
    return load_video_content(filepath, extract_content=False)


def load_video_content_extracted(filepath: str) -> str:
    """Load video transcript content with meaningful content extraction."""
    return load_video_content(filepath, extract_content=True)
