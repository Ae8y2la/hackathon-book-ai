import re
import os
from typing import List, Dict, Any, Tuple
import markdown
from pathlib import Path


def extract_title_from_markdown(content: str) -> str:
    """
    Extract the title from markdown content.
    Looks for the first H1 heading or uses the filename if no H1 is found.
    """
    # Look for H1 headings in markdown
    h1_pattern = r'^#\s+(.+)$'
    matches = re.findall(h1_pattern, content, re.MULTILINE)

    if matches:
        return matches[0].strip()

    return "Untitled Document"


def extract_headers_from_markdown(content: str) -> List[str]:
    """
    Extract all headers from markdown content.
    """
    # Match all headings (h1-h6)
    header_pattern = r'^(#{1,6})\s+(.+)$'
    matches = re.findall(header_pattern, content, re.MULTILINE)

    headers = []
    for level, header in matches:
        headers.append(header.strip())

    return headers


def parse_markdown_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a markdown file and extract content and metadata.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    title = extract_title_from_markdown(content)
    headers = extract_headers_from_markdown(content)

    # Convert markdown to HTML to clean up the content
    html_content = markdown.markdown(content)

    return {
        'content': content,
        'title': title,
        'headers': headers,
        'html_content': html_content,
        'file_path': file_path
    }


def chunk_markdown_content(content: str, max_chunk_size: int = 1000, overlap_size: int = 100) -> List[str]:
    """
    Chunk markdown content into smaller pieces with overlap.
    Uses semantic chunking by splitting on paragraph boundaries.
    """
    # Split content into paragraphs
    paragraphs = content.split('\n\n')

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        # If adding the paragraph would exceed the max size
        if len(current_chunk) + len(paragraph) > max_chunk_size and current_chunk:
            # Add the current chunk to the list
            chunks.append(current_chunk.strip())

            # Start a new chunk with overlap
            if overlap_size > 0:
                # Add overlap from the end of the current chunk
                words = current_chunk.split()
                overlap_words = words[-(overlap_size // 5):]  # Approximate overlap
                current_chunk = ' '.join(overlap_words) + ' ' + paragraph
            else:
                current_chunk = paragraph
        else:
            # Add the paragraph to the current chunk
            current_chunk += '\n\n' + paragraph if current_chunk else paragraph

    # Add the last chunk if it exists
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # If any chunk is still too large, split by sentences
    final_chunks = []
    for chunk in chunks:
        if len(chunk) > max_chunk_size:
            # Split by sentences
            sentences = re.split(r'(?<=[.!?]) +', chunk)
            temp_chunk = ""

            for sentence in sentences:
                if len(temp_chunk) + len(sentence) > max_chunk_size and temp_chunk:
                    final_chunks.append(temp_chunk.strip())
                    temp_chunk = sentence
                else:
                    temp_chunk += ' ' + sentence if temp_chunk else sentence

            if temp_chunk.strip():
                final_chunks.append(temp_chunk.strip())
        else:
            final_chunks.append(chunk)

    # Filter out empty chunks
    final_chunks = [chunk for chunk in final_chunks if chunk.strip()]

    return final_chunks


def get_all_markdown_files(docs_dir: str) -> List[str]:
    """
    Get all markdown files from the docs directory recursively.
    """
    md_files = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.lower().endswith(('.md', '.markdown')):
                md_files.append(os.path.join(root, file))
    return md_files