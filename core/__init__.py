"""
DataCamp Exercise Generator - Core Package

This package contains core functionality including the learning designer.
"""

from .designer import LearningDesigner
from .utils import load_video_content

__all__ = [
    "LearningDesigner",
    "load_video_content"
]
