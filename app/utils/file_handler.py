import os
import json
import yaml
import logging
from typing import Dict, Any, Optional, Union, List
from pathlib import Path

logger = logging.getLogger(__name__)

class FileHandler:
    """Utility for handling file operations in the application"""
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """Read JSON file and return as dictionary"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            logger.error(f"Error reading JSON file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
        """Write dictionary to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent)
            return True
        except Exception as e:
            logger.error(f"Error writing JSON file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """Read YAML file and return as dictionary"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.error(f"Error reading YAML file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any]) -> bool:
        """Write dictionary to YAML file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, default_flow_style=False)
            return True
        except Exception as e:
            logger.error(f"Error writing YAML file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def read_text(file_path: str) -> str:
        """Read text file and return content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def write_text(file_path: str, content: str) -> bool:
        """Write content to text file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return True
        except Exception as e:
            logger.error(f"Error writing text file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def list_files(directory: str, pattern: Optional[str] = None) -> List[str]:
        """List files in directory, optionally filtered by pattern"""
        try:
            path = Path(directory)
            if pattern:
                return [str(f) for f in path.glob(pattern) if f.is_file()]
            else:
                return [str(f) for f in path.iterdir() if f.is_file()]
        except Exception as e:
            logger.error(f"Error listing files in {directory}: {str(e)}")
            return []
    
    @staticmethod
    def ensure_directory(directory: str) -> bool:
        """Ensure directory exists, create if it doesn't"""
        try:
            os.makedirs(directory, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Error creating directory {directory}: {str(e)}")
            return False
    
    @staticmethod
    def get_workflow_path(workflow_name: str) -> str:
        """Get the path to a workflow YAML file"""
        base_dir = os.path.join(os.getcwd(), "app", "workflow")
        return os.path.join(base_dir, f"{workflow_name}.yaml")
    
    @staticmethod
    def load_workflow(workflow_name: str) -> Dict[str, Any]:
        """Load a workflow from its YAML file"""
        workflow_path = FileHandler.get_workflow_path(workflow_name)
        return FileHandler.read_yaml(workflow_path)