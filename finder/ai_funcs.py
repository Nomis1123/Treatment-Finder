import os
import google.generativeai as genai
from dotenv import load_dotenv


class GeminiClient:
    """
    A client for interacting with the Gemini AI API to generate text based on prompts.
    """
    
    def __init__(self):
        try:
            load_dotenv('.env')
            api_key = os.getenv("GEMINI_KEY")
            if not api_key:
                raise ValueError("GEMINI_KEY not found. Please create a .env file and add your key.")
            genai.configure(api_key=api_key)
            print("Gemini API configured successfully.")
        except Exception as e:
            print(f"Error configuring Gemini API: {e}")
            raise
            
        
    def generate_text(self, prompt: str, model_name: str = "gemini-2.5-flash") -> str | None:
        """
        Generates text using the specified Gemini model.

        Args:
            prompt (str): The text prompt to send to the model.
            model_name (str): The name of the model to use (e.g., 'gemini-1.5-flash').

        Returns:
            str | None: The generated text, or None if an error occurred.
        """
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)

            return response.text
        except Exception as e:
            print(f"An error occurred while generating text: {e}")
            return None
        