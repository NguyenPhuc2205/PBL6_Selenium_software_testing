"""
Utility functions for JSON operations
"""
import json
from typing import Any, Dict, List


class JsonUtils:
    """JSON utility functions"""
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
        """Write data to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    
    @staticmethod
    def validate_json(data: str) -> bool:
        """Validate JSON string"""
        try:
            json.loads(data)
            return True
        except json.JSONDecodeError:
            return False
    
    @staticmethod
    def pretty_print(data: Dict[str, Any]) -> str:
        """Pretty print JSON data"""
        return json.dumps(data, indent=2, ensure_ascii=False)
