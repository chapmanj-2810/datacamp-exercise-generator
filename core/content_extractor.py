"""
Content extractor for cleaning video transcript files.
"""

import re


class VideoContentExtractor:
    """Extracts meaningful content from DataCamp video transcript files."""
    
    def __init__(self):
        # Patterns to identify and extract meaningful content
        self.script_pattern = re.compile(r"`@script`\s*\n(.*?)(?=\n\n---|$)", re.DOTALL)
        self.slide_title_pattern = re.compile(r"^## (.+?)$", re.MULTILINE)
        self.part_content_pattern = re.compile(r"`@part\d+`\s*\n(.*?)(?=`@|\n\n---|$)", re.DOTALL)
        
        # YAML frontmatter pattern
        self.frontmatter_pattern = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL | re.MULTILINE)
        
        # YAML code blocks to remove (ONLY YAML - be more specific to avoid catching other languages)
        self.yaml_block_pattern = re.compile(r"```yaml\s*\n.*?\n```", re.DOTALL)
        
        # Metadata patterns to remove - compiled for performance
        self.metadata_patterns = [
            re.compile(r"`@lower_third`.*?(?=\n\n|\n`@|$)", re.DOTALL | re.MULTILINE),
            re.compile(r"key:\s*[a-f0-9]+"),
            re.compile(r"type:\s*\w+"),
            re.compile(r"disable_transition:\s*\w+"),
            re.compile(r"hide_title:\s*\w+"),
            re.compile(r"code_zoom:\s*\d+"),
            re.compile(r"video_link:.*?(?=\n\n|\n---|$)", re.DOTALL | re.MULTILINE),
            re.compile(r"mp3:\s*>-.*?(?=\n\n|\n---|$)", re.DOTALL | re.MULTILINE)
        ]
        
        # Additional compiled patterns for efficiency
        self.transition_numbers_pattern = re.compile(r"\{\{\d+\}\}")
        self.empty_bullets_pattern = re.compile(r"^\s*-\s*$", re.MULTILINE)
        self.excessive_whitespace_pattern = re.compile(r"\n\s*\n\s*\n")
        self.whitespace_filter_pattern = re.compile(r"^[&\s]*$")
    
    def has_video_structure(self, content: str) -> bool:
        """Check if content has DataCamp video structure."""
        indicators = [
            re.compile(r"`@script`"),
            re.compile(r"^## .+$", re.MULTILINE),  # Slide titles
            re.compile(r"```yaml\s*\ntype:"),
            re.compile(r"`@part\d+`"),
            re.compile(r"^---\s*$", re.MULTILINE)  # Section separators
        ]
        
        indicator_count = 0
        for pattern in indicators:
            if pattern.search(content):
                indicator_count += 1
        
        # Require at least 2 indicators to consider it structured video content
        return indicator_count >= 2
    
    def _clean_plain_text(self, content: str) -> str:
        """Clean plain text content with minimal processing."""
        # Remove excessive whitespace
        content = self.excessive_whitespace_pattern.sub("\n\n", content)
        
        # Remove empty lines at start and end
        content = content.strip()
        
        return content
    
    def extract_meaningful_content(self, video_content: str) -> str:
        """
        Extract meaningful content from either structured video files or plain text files.
        Automatically detects the file type and applies appropriate processing.
        
        Args:
            video_content: Raw file content (structured video transcript or plain text)
            
        Returns:
            Cleaned content appropriate for exercise generation
        """
        if not self.has_video_structure(video_content):
            # Plain text file - return with minimal cleaning
            return self._clean_plain_text(video_content)
        
        # Structured video file - apply full extraction
        sections = self._split_into_sections(video_content)
        meaningful_content = []
        
        for section in sections:
            extracted = self._extract_section_content(section)
            if extracted.strip():  # Only add non-empty content
                meaningful_content.append(extracted)
        
        result = "\n\n".join(meaningful_content)
        
        # Fallback: if structured extraction found nothing, treat as plain text
        if not result.strip():
            return self._clean_plain_text(video_content)
        
        return result
    
    def _split_into_sections(self, content: str) -> list[str]:
        """Split video content into individual slide sections."""
        # Remove frontmatter first
        content = self.frontmatter_pattern.sub("", content)
        
        # Split on slide separators (---)
        sections = re.split(r"\n---\n", content)
        return [section.strip() for section in sections if section.strip()]
    
    def _extract_section_content(self, section: str) -> str:
        """Extract meaningful content from a single slide section."""
        extracted_parts = []
        
        # Extract slide title
        title_match = self.slide_title_pattern.search(section)
        if title_match:
            extracted_parts.append(f"# {title_match.group(1)}")
        
        # IMPORTANT: Remove YAML blocks BEFORE extracting other content
        # Only remove ```yaml blocks, preserve all other code blocks
        section = self.yaml_block_pattern.sub("", section)
        
        # Extract script content
        script_matches = self.script_pattern.findall(section)
        for script in script_matches:
            cleaned_script = self._clean_script_content(script.strip())
            if cleaned_script:
                extracted_parts.append(cleaned_script)
        
        # Extract slide content (from @part1, @part2, etc.) - PRESERVING ALL CODE BLOCKS
        part_matches = self.part_content_pattern.findall(section)
        for part in part_matches:
            cleaned_part = self._clean_slide_content(part.strip())
            if cleaned_part:
                extracted_parts.append(cleaned_part)
        
        return "\n\n".join(extracted_parts)
    
    def _clean_script_content(self, script: str) -> str:
        """Clean script content by removing metadata and formatting."""
        # Remove slide transition numbers like {{1}}, {{2}}
        script = self.transition_numbers_pattern.sub("", script)
        
        # Remove empty lines and extra whitespace
        lines = [line.strip() for line in script.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def _clean_slide_content(self, content: str) -> str:
        """Clean slide content while aggressively PRESERVING ALL CODE BLOCKS."""
        # Remove slide transition numbers
        content = self.transition_numbers_pattern.sub("", content)
        
        # First, extract and preserve ALL code blocks before any other processing
        code_blocks = []
        code_block_pattern = re.compile(r"```(\w+)?\s*\n(.*?)\n```", re.DOTALL)
        
        def preserve_code_block(match):
            """Preserve code blocks by replacing with placeholder."""
            nonlocal code_blocks
            placeholder = f"__CODE_BLOCK_{len(code_blocks)}__"
            code_blocks.append(match.group(0))  # Store entire code block
            return placeholder
        
        # Replace all code blocks with placeholders
        content = code_block_pattern.sub(preserve_code_block, content)
        
        # Remove metadata patterns (now safe since code blocks are preserved)
        for pattern in self.metadata_patterns:
            content = pattern.sub("", content)
        
        # Clean up empty bullet points
        content = self.empty_bullets_pattern.sub("", content)
        
        # Remove excessive whitespace
        content = self.excessive_whitespace_pattern.sub("\n\n", content)
        
        # Filter out empty lines and single characters
        lines = []
        for line in content.split('\n'):
            stripped_line = line.strip()
            if len(stripped_line) > 1 and not self.whitespace_filter_pattern.match(stripped_line):
                lines.append(line)
        
        content = '\n'.join(lines)
        
        # Restore all code blocks
        for i, code_block in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_{i}__"
            content = content.replace(placeholder, code_block)
        
        return content
    
def extract_video_content(video_content: str) -> str:
    """Convenience function to extract meaningful content from video transcript."""
    extractor = VideoContentExtractor()
    return extractor.extract_meaningful_content(video_content)
