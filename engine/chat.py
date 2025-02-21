from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the Hugging Face token from the .env file
api_token = os.getenv("HF_TOKEN")

# Check if the token is loaded
if not api_token:
    raise ValueError("Hugging Face token not found. Make sure it's in the .env file as HF_TOKEN.")

# Initialize the Hugging Face InferenceClient
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm_client = InferenceClient(
    model=repo_id,
    token=api_token,
    timeout=120
)

def call_llm(inference_client: InferenceClient, prompt: str):
    # Use the text_generation method to get the model's response
    response = inference_client.text_generation(
        prompt=prompt,
        max_new_tokens=250,
        temperature=0.8
    )
    return response

# Continuous chat loop
print("Welcome to the Chatbot! Type 'exit' to quit.\n")

while True:
    # Get user prompt
    user_prompt = input("You: ")

    # Check if the user wants to exit
    if user_prompt.lower() == "exit":
        print("Exiting the chat. Goodbye!")
        break

    # Call the LLM with the user's prompt and display the response
    response = call_llm(llm_client, user_prompt)
    print(f"Chatbot: {response}\n")
