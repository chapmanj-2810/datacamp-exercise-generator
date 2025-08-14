from setuptools import setup, find_packages

setup(
    name="datacamp-exercise-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0"
    ],
    author="DataCamp",
    description="An intelligent system for automatically generating DataCamp exercises from video content",
    python_requires=">=3.9",
)
