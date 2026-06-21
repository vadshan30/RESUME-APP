import os
import pdfplumber
from typing import Dict, Optional

class ResumeParser:
    """Service for parsing resumes from PDF and text files."""
    
    @staticmethod
    def extract_text(file_path: str, file_type: str) -> Dict[str, any]:
        """
        Extract text from resume file.
        
        Args:
            file_path: Path to the uploaded file
            file_type: MIME type of the file
            
        Returns:
            Dictionary with extracted text and metadata
        """
        try:
            if file_type == 'application/pdf':
                text = ResumeParser._extract_from_pdf(file_path)
            elif file_type == 'text/plain':
                text = ResumeParser._extract_from_text(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            return {
                'success': True,
                'text': text,
                'word_count': len(text.split()),
                'char_count': len(text)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': ''
            }
    
    @staticmethod
    def _extract_from_pdf(file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            # Fallback to PyPDF2 if pdfplumber fails
            try:
                import PyPDF2
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except:
                raise Exception(f"Failed to extract text from PDF: {str(e)}")
        
        return text.strip()
    
    @staticmethod
    def _extract_from_text(file_path: str) -> str:
        """Extract text from plain text file."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read().strip()
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize extracted text."""
        # Remove extra whitespace
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        # Remove duplicate lines
        seen = set()
        unique_lines = []
        for line in lines:
            if line.lower() not in seen:
                seen.add(line.lower())
                unique_lines.append(line)
        return '\n'.join(unique_lines)

