"""
Knowledge Base Service - Search and retrieve product documentation
"""
import os
import sys
from typing import List, Dict, Any, Optional
from pathlib import Path
import re

# Add parent path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


class KnowledgeBaseService:
    """Service for searching and retrieving knowledge base articles"""

    def __init__(self, kb_path: str = None):
        """Initialize knowledge base service
        
        Args:
            kb_path: Path to knowledge base directory
        """
        if kb_path is None:
            # Go up one level from services to backend, then into knowledge_base
            kb_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'knowledge_base')
        
        self.kb_path = kb_path
        self.documents: Dict[str, str] = {}
        self.index: Dict[str, List[str]] = {}
        self._load_documents()

    def _load_documents(self):
        """Load all markdown documents from knowledge base"""
        kb_dir = Path(self.kb_path)

        if not kb_dir.exists():
            print(f"[WARNING] Knowledge base directory not found: {self.kb_path}")
            return

        for file_path in kb_dir.glob("*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    doc_name = file_path.stem
                    self.documents[doc_name] = content
                    self._index_document(doc_name, content)
                    print(f"[INFO] Loaded: {doc_name}")
            except Exception as e:
                print(f"[ERROR] Error loading {file_path}: {str(e)}")

    def _index_document(self, doc_name: str, content: str):
        """Create simple keyword index for document
        
        Args:
            doc_name: Document name
            content: Document content
        """
        # Extract keywords from headings and important terms
        keywords = set()
        
        # Extract headings (# Heading)
        headings = re.findall(r'^#\s+(.+)$', content, re.MULTILINE | re.IGNORECASE)
        for heading in headings:
            keywords.update(heading.lower().split())
        
        # Extract subheadings (## Subheading)
        subheadings = re.findall(r'^##\s+(.+)$', content, re.MULTILINE | re.IGNORECASE)
        for sub in subheadings:
            keywords.update(sub.lower().split())
        
        # Extract Q&A pairs
        qa_pairs = re.findall(r'^###?\s*Q:\s*(.+)$', content, re.MULTILINE | re.IGNORECASE)
        for qa in qa_pairs:
            keywords.update(qa.lower().split())
        
        # Store index
        self.index[doc_name] = list(keywords)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search knowledge base for relevant articles

        Args:
            query: Search query string
            top_k: Number of results to return

        Returns:
            List of relevant document sections with scores
        """
        query_lower = query.lower()
        query_words = set(query_lower.split())

        results = []

        for doc_name, content in self.documents.items():
            score = 0
            matched_sections = []

            # Check if query words appear in document
            doc_lower = content.lower()

            # Exact phrase match (highest score)
            if query_lower in doc_lower:
                score += 10
                matched_sections.append(("exact_match", query))

            # Word matches
            for word in query_words:
                if len(word) < 3:
                    continue

                # Count occurrences
                count = doc_lower.count(word)
                if count > 0:
                    score += min(count * 2, 10)  # Cap at 10 per word

                    # Find the section where word appears
                    sections = self._find_sections_with_word(content, word)
                    matched_sections.extend(sections)

            # Keyword index match
            if doc_name in self.index:
                for keyword in self.index[doc_name]:
                    if keyword in query_words:
                        score += 3

            if score > 0:
                # Get relevant excerpt
                excerpt = self._get_relevant_excerpt(content, query_words)

                results.append({
                    "document": doc_name,
                    "score": score,
                    "excerpt": excerpt,
                    "matched_sections": list(set(matched_sections))[:5],
                    "full_content": content
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:top_k]

    def _find_sections_with_word(self, content: str, word: str) -> List[tuple]:
        """Find sections containing a specific word
        
        Args:
            content: Document content
            word: Word to search for
            
        Returns:
            List of (section_type, section_title) tuples
        """
        sections = []
        lines = content.split('\n')
        
        current_section = "Introduction"
        
        for line in lines:
            if line.startswith('###'):
                current_section = line.replace('#', '').strip()
            
            if word.lower() in line.lower():
                sections.append(("section", current_section))
        
        return sections

    def _get_relevant_excerpt(self, content: str, query_words: set, max_length: int = 300) -> str:
        """Get relevant excerpt from document
        
        Args:
            content: Document content
            query_words: Set of query words
            max_length: Maximum excerpt length
            
        Returns:
            Relevant excerpt string
        """
        lines = content.split('\n')
        best_excerpt = ""
        best_score = 0
        
        for i, line in enumerate(lines):
            line_score = 0
            for word in query_words:
                if len(word) < 3:
                    continue
                if word.lower() in line.lower():
                    line_score += 1
            
            if line_score > best_score:
                best_score = line_score
                # Get context (previous and next lines)
                start = max(0, i - 2)
                end = min(len(lines), i + 3)
                best_excerpt = '\n'.join(lines[start:end])
        
        if not best_excerpt and lines:
            # Fallback to first section
            best_excerpt = '\n'.join(lines[:5])
        
        # Truncate if too long
        if len(best_excerpt) > max_length:
            best_excerpt = best_excerpt[:max_length] + "..."
        
        return best_excerpt.strip()

    def get_article(self, doc_name: str) -> Optional[str]:
        """Get full article by name
        
        Args:
            doc_name: Document name
            
        Returns:
            Document content or None
        """
        return self.documents.get(doc_name)

    def get_all_articles(self) -> List[str]:
        """Get list of all article names
        
        Returns:
            List of document names
        """
        return list(self.documents.keys())

    def get_article_summary(self, doc_name: str) -> Optional[Dict[str, Any]]:
        """Get article summary with headings
        
        Args:
            doc_name: Document name
            
        Returns:
            Dictionary with title, headings, and word count
        """
        content = self.documents.get(doc_name)
        if not content:
            return None
        
        # Extract main title
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else doc_name
        
        # Extract all headings
        headings = re.findall(r'^(#{1,3})\s+(.+)$', content, re.MULTILINE)
        
        # Word count
        word_count = len(content.split())
        
        return {
            "title": title,
            "headings": [h[1] for h in headings],
            "word_count": word_count,
            "preview": content[:200] + "..."
        }


# Singleton instance
knowledge_base = KnowledgeBaseService()


# Export functions for MCP tools
def search_knowledge_base(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Search knowledge base for relevant articles
    
    Args:
        query: Search query
        top_k: Number of results
        
    Returns:
        List of relevant articles
    """
    return knowledge_base.search(query, top_k)


def get_article(doc_name: str) -> Optional[str]:
    """Get full article by name"""
    return knowledge_base.get_article(doc_name)


def get_all_articles() -> List[str]:
    """Get list of all articles"""
    return knowledge_base.get_all_articles()
