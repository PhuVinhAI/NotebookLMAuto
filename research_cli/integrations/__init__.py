"""
Integration modules for Research CLI
"""

from .notebooklm_client import NotebookLMIntegration
from .automation import ResearchAutomation

__all__ = ['NotebookLMIntegration', 'ResearchAutomation']