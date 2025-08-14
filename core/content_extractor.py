"""
Content extractor for cleaning video transcript files.
"""

import re


class VideoContentExtractor:
    """Extracts meaningful content from DataCamp video transcript files."""
    
    def __init__(self):
        # Patterns to identify and extract meaningful content
        self.script_pattern = r"`@script`\s*\n(.*?)(?=\n\n---|$)"
        self.slide_title_pattern = r"^## (.+?)$"
        self.part_content_pattern = r"`@part\d+`\s*\n(.*?)(?=`@|\n\n---|$)"
        
        # YAML frontmatter pattern
        self.frontmatter_pattern = r"^---\s*\n.*?\n---\s*\n"
        
        # YAML code blocks to remove
        self.yaml_block_pattern = r"```yaml\s*\n.*?\n```"
        
        # Metadata patterns to remove
        self.metadata_patterns = [
            r"`@lower_third`.*?(?=\n\n|\n`@|$)",
            r"key:\s*[a-f0-9]+",
            r"type:\s*\w+",
            r"disable_transition:\s*\w+",
            r"hide_title:\s*\w+",
            r"code_zoom:\s*\d+",
            r"video_link:.*?(?=\n\n|\n---|$)",
            r"mp3:\s*>-.*?(?=\n\n|\n---|$)"
        ]
    
    def extract_meaningful_content(self, video_content: str) -> str:
        """
        Extract only meaningful content (titles, scripts, slide content) from video file.
        
        Args:
            video_content: Raw video transcript content
            
        Returns:
            Cleaned content with only titles, scripts, and slide content
        """
        sections = self._split_into_sections(video_content)
        meaningful_content = []
        
        for section in sections:
            extracted = self._extract_section_content(section)
            if extracted.strip():  # Only add non-empty content
                meaningful_content.append(extracted)
        
        return "\n\n".join(meaningful_content)
    
    def _split_into_sections(self, content: str) -> list[str]:
        """Split video content into individual slide sections."""
        # Remove frontmatter first
        content = re.sub(self.frontmatter_pattern, "", content, flags=re.DOTALL | re.MULTILINE)
        
        # Split on slide separators (---)
        sections = re.split(r"\n---\n", content)
        return [section.strip() for section in sections if section.strip()]
    
    def _extract_section_content(self, section: str) -> str:
        """Extract meaningful content from a single slide section."""
        extracted_parts = []
        
        # Extract slide title
        title_match = re.search(self.slide_title_pattern, section, re.MULTILINE)
        if title_match:
            extracted_parts.append(f"# {title_match.group(1)}")
        
        # Remove YAML blocks
        section = re.sub(self.yaml_block_pattern, "", section, flags=re.DOTALL)
        
        # Extract script content
        script_matches = re.findall(self.script_pattern, section, re.DOTALL)
        for script in script_matches:
            cleaned_script = self._clean_script_content(script.strip())
            if cleaned_script:
                extracted_parts.append(cleaned_script)
        
        # Extract slide content (from @part1, @part2, etc.)
        part_matches = re.findall(self.part_content_pattern, section, re.DOTALL)
        for part in part_matches:
            cleaned_part = self._clean_slide_content(part.strip())
            if cleaned_part:
                extracted_parts.append(cleaned_part)
        
        return "\n\n".join(extracted_parts)
    
    def _clean_script_content(self, script: str) -> str:
        """Clean script content by removing metadata and formatting."""
        # Remove slide transition numbers like {{1}}, {{2}}
        script = re.sub(r"\{\{\d+\}\}", "", script)
        
        # Remove empty lines and extra whitespace
        lines = [line.strip() for line in script.split('\n') if line.strip()]
        return ' '.join(lines)
    
    def _clean_slide_content(self, content: str) -> str:
        """Clean slide content by removing metadata while preserving formatting."""
        # Remove slide transition numbers
        content = re.sub(r"\{\{\d+\}\}", "", content)
        
        # Remove metadata patterns
        for pattern in self.metadata_patterns:
            content = re.sub(pattern, "", content, flags=re.DOTALL | re.MULTILINE)
        
        # Clean up empty bullet points only
        content = re.sub(r"^\s*-\s*$", "", content, flags=re.MULTILINE)  # Empty bullets
        
        # Remove excessive whitespace
        content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)
        
        # Filter out lines that are just whitespace or single characters
        lines = []
        for line in content.split('\n'):
            line = line.strip()
            if len(line) > 1 and not re.match(r"^[&\s]*$", line):
                lines.append(line)
        
        return '\n'.join(lines)
    
    def get_content_summary(self, video_content: str) -> dict[str, int]:
        """Get statistics about original vs extracted content."""
        extracted = self.extract_meaningful_content(video_content)
        
        return {
            "original_chars": len(video_content),
            "extracted_chars": len(extracted),
            "reduction_percentage": round((1 - len(extracted) / len(video_content)) * 100, 1),
            "original_lines": len(video_content.split('\n')),
            "extracted_lines": len(extracted.split('\n'))
        }


def extract_video_content(video_content: str) -> str:
    """Convenience function to extract meaningful content from video transcript."""
    extractor = VideoContentExtractor()
    return extractor.extract_meaningful_content(video_content)
