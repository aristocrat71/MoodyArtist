import requests
import os
from typing import Dict, Any

class HuggingFaceClient:
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        self.api_token = os.getenv('HF_API_KEY')
        
        if not self.api_token:
            raise ValueError("HF_API_KEY environment variable not set")
    
    def generate_idea(self, prompt: str) -> Dict[str, Any]:
        """
        Generate creative idea using HuggingFace Mistral model
        """
        try:
            headers = {"Authorization": f"Bearer {self.api_token}"}
            payload = {"inputs": prompt}
            
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract the generated text from the response
                if isinstance(result, list) and len(result) > 0:
                    idea = result[0].get('generated_text', '').strip()
                    # Clean up the response to get just the generated part
                    if '[/INST]' in idea:
                        idea = idea.split('[/INST]')[-1].strip()
                else:
                    idea = str(result).strip()
                
                return {"success": True, "idea": idea}
            else:
                return {
                    "success": False, 
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False, 
                "error": f"Request failed: {str(e)}"
            } 