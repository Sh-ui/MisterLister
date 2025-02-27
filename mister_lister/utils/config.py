"""
Configuration management for MisterLister.
Provides consistent type conversion and value handling.
"""

import os
import json
from mister_lister.constants import (
    DEFAULT_FONT_SIZE,
    DEFAULT_ROW_SPACING,
    DEFAULT_MARGIN,
    DEFAULT_BORDER_STYLE,
    DEFAULT_BORDER_GRAY,
    DEFAULT_REMEMBER_DIR,
    DEFAULT_REMEMBER_LAYOUT,
    DEFAULT_SHOW_DIALOG
)

class Config:
    """
    Configuration manager with JSON persistence and type safety.
    
    Features:
    - JSON-based configuration storage
    - Type-safe value getting/setting
    - Centralized default values
    """
    
    def __init__(self):
        """Initialize configuration with defaults"""
        self.type_map = {
            # Layout settings
            'layout/font_size': float,
            'layout/row_spacing': float,
            'layout/remember_config': bool,
            'layout/remember_window': bool,
            'layout/window_geometry': str,
            
            # Print settings
            'print/border_style': str,
            'print/border_gray': int,
            'print/printer_name': str,
            
            # File settings
            'files/remember_dir': bool,
            'files/default_dir': str,
            'files/backup_dir': str,
            
            # Startup settings
            'startup/show_dialog': bool,
        }
        
        self.defaults = {
            # Layout defaults
            'layout/font_size': 12.0,
            'layout/row_spacing': 30.0,
            'layout/remember_config': False,
            'layout/remember_window': False,
            'layout/window_geometry': '',
            
            # Print defaults
            'print/border_style': 'solid',
            'print/border_gray': 128,
            'print/printer_name': '',
            
            # File defaults
            'files/remember_dir': False,
            'files/default_dir': '',
            'files/backup_dir': '',
            
            # Startup defaults
            'startup/show_dialog': False,
        }
        
        # Load or create config file
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.config_dir, exist_ok=True)
        self.config_file = os.path.join(self.config_dir, 'config.json')
        
        if os.path.exists(self.config_file):
            self.load_config()
        else:
            self.config = self.defaults.copy()
            self.save_config()

    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            else:
                self.config = {}
                self.save_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            self.save_config()

    def save_config(self):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_value(self, key, default=None):
        """
        Get a config value with proper type conversion.
        
        Args:
            key: Config key
            default: Optional default value (overrides class defaults)
            
        Returns:
            Value with correct type
        """
        if key not in self.type_map:
            raise ValueError(f"Unknown config key: {key}")
            
        if default is None:
            default = self.defaults.get(key)
            
        raw_value = self.config.get(key, default)
        expected_type = self.type_map[key]
        
        # Handle type conversion
        if expected_type == bool:
            if isinstance(raw_value, bool):
                return raw_value
            return str(raw_value).lower() == 'true'
        
        try:
            return expected_type(raw_value)
        except (ValueError, TypeError):
            return default

    def set_value(self, key, value):
        """
        Set a config value with type validation.
        
        Args:
            key: Config key
            value: Value to store
        """
        if key not in self.type_map:
            raise ValueError(f"Unknown config key: {key}")
            
        expected_type = self.type_map[key]
        try:
            typed_value = expected_type(value)
            self.config[key] = typed_value
            self.save_config()
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid value for {key}: {value}. Expected {expected_type.__name__}") from e

    def reset_to_defaults(self):
        """Reset all config to default values"""
        self.config = self.defaults.copy()
        self.save_config()

    # Type-specific convenience methods
    def get_bool(self, key, default=None):
        """Get a boolean config value"""
        return self.get_value(key, default)

    def get_float(self, key, default=None):
        """Get a float config value"""
        return self.get_value(key, default)

    def get_int(self, key, default=None):
        """Get an integer config value"""
        return self.get_value(key, default)

    def get_str(self, key, default=None):
        """Get a string config value"""
        return self.get_value(key, default) 