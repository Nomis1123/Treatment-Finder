import os
import google.generativeai as genai
from dotenv import load_dotenv
import TreatmentFinder.matching_engine as ds


def setup_gemini():
    """
    Loads the API key from the .env file and configures the Gemini API.
    Call this function once at the start of your application.
    """
    load_dotenv(".env")
    
    api_key = os.getenv("GEMINI_KEY")
    
    if not api_key:
        raise ValueError("GEMINI_KEY not found. Please create a .env file and add your key.")
        
    try:
        genai.configure(api_key=api_key)
        print("Gemini API configured successfully.")
    except Exception as e:
        # This can catch issues if the API key is invalid
        print(f"Error configuring Gemini API: {e}")
        raise
    
    
def generate_text(prompt: str, model_name: str = "gemini-2.5-flash") -> str | None:
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
        # This will catch errors during the API call, like network issues or bad requests
        print(f"An error occurred while generating text: {e}")
        return None
    
    
    
if __name__ == "__main__":
    
    # First, set up the API connection
    setup_gemini()

    # Now, define the prompt you want to use
    my_prompt = "Explain the concept of 'dark matter' to a 10-year-old."

    # Call the function to get the response
    generated_response = generate_text(my_prompt)

    # Always check if the response is valid before using it
    if generated_response:
        print("Gemini's Response:")
        print(generated_response)
    else:
        print("Failed to get a response from Gemini.")
        
    
