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
    # Generate a single, concise response
    response = inference_client.text_generation(
        prompt=prompt,
        max_new_tokens=50,     # Short limit to prevent overgeneration
        temperature=0.5,       # Strict adherence to input
        top_p=0.9,             # Focused output
        top_k=30,              # Tight token selection
        repetition_penalty=1.2, # Avoid repetition
        stop=["\n", "User:", "JARVIS:"]  # Updated to use `stop` instead of `stop_sequences`
    )
    return response.strip()

# Strict system prompt to enforce single-turn behavior
system_prompt = (
    "You are JARVIS, a highly intelligent, witty, and slightly sarcastic personal assistant inspired by Tony Stark's AI. "
    "Respond ONLY to the user's exact input with a concise, helpful, and truthful answer. "
    "Add a touch of humor if appropriate, but do NOT generate additional questions, commands, or conversation beyond the input. "
    "Stop after one response and wait for the next user input."
)

# Continuous chat loop with debug output
print("Welcome to JARVIS! Type 'exit' to quit.\n")

while True:
    # Get user prompt
    user_prompt = input("You: ").strip()

    # Check if the user wants to exit
    if user_prompt.lower() == "exit":
        print("JARVIS: Farewell, sir. Shutting down now.")
        break

    # Debug: Show what we're sending to the model
    

    # Combine system prompt with user input
    full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\nJARVIS: "

    # Call the LLM and get the response
    response = call_llm(llm_client, full_prompt)

    

    # Display the response
    print(f"JARVIS: {response}\n")