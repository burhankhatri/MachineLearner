import os
from typing import Optional, List

class FileManager:
    def __init__(self, base_path: str = "models"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def save_model(self, model_name: str, code: str) -> str:
        """Save model code to file"""
        file_path = os.path.join(self.base_path, f"{model_name}.py")
        with open(file_path, "w") as f:
            f.write(code)
        return file_path
    
    def load_model(self, model_name: str) -> Optional[str]:
        """Load model code from file"""
        file_path = os.path.join(self.base_path, f"{model_name}.py")
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r") as f:
            return f.read()
    
    def list_models(self) -> List[str]:
        """List all saved models"""
        if not os.path.exists(self.base_path):
            return []
        return [f.replace(".py", "") for f in os.listdir(self.base_path) 
                if f.endswith(".py")] 