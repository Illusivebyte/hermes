from abc import ABC, abstractmethod
from typing import Dict, List

class Formatter(ABC):
    @staticmethod
    @abstractmethod
    def get_name() -> str:
        return ""
    
    @staticmethod
    @abstractmethod
    def format(json_obj: Dict) -> List:
        return ""
