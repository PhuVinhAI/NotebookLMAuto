"""
Configuration management utilities
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def get_config_dir() -> Path:
    """Get configuration directory"""
    home = Path.home()
    config_dir = home / '.research_cli'
    config_dir.mkdir(exist_ok=True)
    return config_dir


def get_config_file() -> Path:
    """Get configuration file path"""
    return get_config_dir() / 'config.json'


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    config_file = get_config_file()
    
    if not config_file.exists():
        return get_default_config()
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except (json.JSONDecodeError, IOError):
        return get_default_config()


def save_config(config: Dict[str, Any]) -> bool:
    """Save configuration to file"""
    try:
        config_file = get_config_file()
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_default_config() -> Dict[str, Any]:
    """Get default configuration"""
    return {
        'youtube': {
            'default_max_results': 10,
            'default_min_views': 1000,
            'default_sort_by': 'relevance'
        },
        'notebooklm': {
            'default_language': 'en',
            'auto_wait_for_processing': True,
            'default_output_dir': '.'
        },
        'output': {
            'default_format': 'human',
            'show_progress': True,
            'verbose': False
        }
    }


def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting"""
    config = load_config()
    keys = key.split('.')
    
    current = config
    for k in keys:
        if isinstance(current, dict) and k in current:
            current = current[k]
        else:
            return default
    
    return current


def set_setting(key: str, value: Any) -> bool:
    """Set a specific setting"""
    config = load_config()
    keys = key.split('.')
    
    current = config
    for k in keys[:-1]:
        if k not in current:
            current[k] = {}
        current = current[k]
    
    current[keys[-1]] = value
    return save_config(config)