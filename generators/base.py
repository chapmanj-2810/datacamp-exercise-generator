"""
Base exercise generator abstract class.
"""

import os
import json
import re
import time
from abc import ABC, abstractmethod
from openai import OpenAI
from ..models.exercises import Exercise


class ExerciseGenerator(ABC):
    def __init__(self, model: str = "gpt-4o", temperature: float = 0, max_retries: int = 3) -> None:
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.model = model
        self.max_retries = max_retries
        
        # GPT-5 models only support temperature=1
        if model.startswith("gpt-5"):
            self.temperature = 1.0
            if temperature != 0:  # Only warn if user explicitly set a different temperature
                print(f"Warning: {model} only supports temperature=1. Adjusting from {temperature} to 1.0")
        else:
            self.temperature = temperature
    
    @abstractmethod
    def get_exercise_type(self) -> str:
        pass
    
    @abstractmethod
    def get_examples_section(self) -> str:
        pass
    
    @abstractmethod
    def get_json_schema(self) -> str:
        pass
    
    @abstractmethod
    def parse_exercises(self, parsed_json: dict) -> list[Exercise]:
        pass
    
    def clean_json_response(self, content: str) -> str:
        """Enhanced JSON cleaning to handle various model quirks."""
        content = content.strip()
        
        # Remove wrapping markdown code blocks more carefully
        # Only remove if they wrap the entire content, not internal code blocks
        
        # Check for opening markdown block at start
        opening_patterns = [
            r"^```json\s*\n",
            r"^```\s*\n", 
            r"^```json\s*",
            r"^```\s*"
        ]
        
        for pattern in opening_patterns:
            if re.match(pattern, content, re.MULTILINE):
                content = re.sub(pattern, "", content, count=1, flags=re.MULTILINE)
                break
        
        # Check for closing markdown block at end
        if content.endswith('\n```'):
            content = content[:-4]
        elif content.endswith('```'):
            content = content[:-3]
        
        content = content.strip()
        
        # Remove common prefixes models add (only at the very start)
        prefixes = ["Here's the JSON:", "The JSON response is:", "Response:", "JSON:"]
        for prefix in prefixes:
            if content.startswith(prefix):
                content = content[len(prefix):].strip()
                break
        
        # More robust JSON boundary detection
        json_content = self._extract_main_json_object(content)
        return json_content.strip() if json_content else content.strip()
    
    def _extract_main_json_object(self, content: str) -> str:
        """Extract the main JSON object using bracket counting for proper nesting."""
        # Find the first opening brace
        start_pos = content.find('{')
        if start_pos == -1:
            return content  # No JSON found, return as-is
        
        # Count braces to find the matching closing brace
        brace_count = 0
        in_string = False
        escape_next = False
        
        for i, char in enumerate(content[start_pos:], start_pos):
            if escape_next:
                escape_next = False
                continue
                
            if char == '\\':
                escape_next = True
                continue
                
            if char == '"' and not escape_next:
                in_string = not in_string
                continue
                
            if not in_string:
                if char == '{':
                    brace_count += 1
                elif char == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Found the matching closing brace
                        return content[start_pos:i + 1]
        
        # If we get here, braces weren't balanced - return from start to end
        return content[start_pos:]
    
    def generate_single_attempt(self, video_content: str, learning_objectives: list[str] | None = None) -> list[Exercise]:
        """Generate exercises in a single attempt (no retries)."""
        # Format objectives section
        if learning_objectives:
            objectives_list = "\n".join(f"- {obj}" for obj in learning_objectives)
            objectives_section = f"""Learning Objectives for this video:
{objectives_list}

IMPORTANT: Create exactly {len(learning_objectives)} exercise(s), with each exercise targeting one specific learning objective from the list above."""
            count_instruction = f"Create exactly {len(learning_objectives)} exercise(s), one for each learning objective."
        else:
            objectives_section = ""
            count_instruction = "Create 2-4 exercises covering different key concepts from the video."
        
        json_prompt = f"""You are an expert curriculum designer for DataCamp. Based on the provided video transcript, create {self.get_exercise_type()} exercises that test key concepts from the video.

{objectives_section}

{count_instruction}

Each exercise should:
1. Have a clear, engaging title
2. Provide relevant context or scenario that creates an immersive learning experience
3. Ask a specific question about video content
4. Include helpful guidance for learners
5. Provide constructive feedback
6. Test understanding without giving away answers
7. Use DIFFERENT examples, scenarios, and contexts than those shown in the video - this tests true conceptual understanding rather than memorization

IMPORTANT: Do not reuse the same examples, company names, scenarios, or specific use cases from the video content. Create fresh, original examples that apply the same concepts in new contexts.

{self.get_examples_section()}

Video Content:
{video_content}

Create exercises with rich, engaging contexts similar to the examples above. Use NEW scenarios, different company names, alternative use cases, and fresh code examples where appropriate to make the exercises test conceptual understanding rather than recall.

{self.get_json_schema()}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": json_prompt}],
            temperature=self.temperature
        )
        
        # Enhanced JSON cleaning
        content = self.clean_json_response(response.choices[0].message.content)
        
        # Parse JSON and validate with Pydantic
        parsed = json.loads(content)
        return self.parse_exercises(parsed)
    
    def generate_exercises(self, video_content: str, learning_objectives: list[str] | None = None) -> list[Exercise]:
        """Generate exercises with automatic retry on JSON parsing failures."""
        last_exception: Exception | None = None
        
        for attempt in range(self.max_retries):
            try:
                return self.generate_single_attempt(video_content, learning_objectives)
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Log the failure and retry
                    print(f"Generation failed on attempt {attempt + 1}/{self.max_retries} for {self.get_exercise_type()}: {str(e)}")
                    print("Retrying with exponential backoff...")
                    time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s
                    continue
                else:
                    # Final attempt failed, raise detailed error
                    break
        
        # All attempts failed
        raise Exception(
            f"Failed to generate valid {self.get_exercise_type()} exercises after {self.max_retries} attempts. "
            f"Last error: {last_exception}"
        ) from last_exception
    
    @abstractmethod
    def generate_markdown_exercises(self, video_content: str, learning_objectives: list[str] | None = None) -> list[str]:
        """Generate exercises and format them as markdown strings."""
        pass
