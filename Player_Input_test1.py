import os
from dotenv import load_dotenv
from google import genai

# 1. Setup
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = "gemini-2.5-flash-lite"

with open("lore.txt", "r") as f:
    game_lore = f.read()

# Initialize a simple memory for the session
chat_history = f"WORLD LORE:\n{game_lore}\n\nCONVERSATION LOG:"

print("--- System: You have entered the Whispering Reach testing zone. ---")
print("--- Type 'exit' to leave. ---\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history += f"\nPlayer: {user_input}"

    # --- BARNABY'S TURN ---
    barnaby_prompt = f"""
    SYSTEM: You are Barnaby, the abbrasive Guard. Use the following conversation history for context.
    DO NOT repeat the history. ONLY provide Barnaby's next line of dialogue.
    
    <history>
    {chat_history}
    </history>
    
    Barnaby:"""  # We end the prompt right here to "anchor" the response

    b_response = client.models.generate_content(
        model=model_name, contents=barnaby_prompt
    )
    barnaby_text = b_response.text.strip()

    # Clean up any accidental "Barnaby:" prefix the AI might have added anyway
    barnaby_text = barnaby_text.replace("Barnaby:", "").strip()

    chat_history += f"\nBarnaby: {barnaby_text}"
    print(f"\nBarnaby: {barnaby_text}")

    # --- SORA'S TURN ---
    sora_prompt = f"""
    SYSTEM: You are Sora, the wise Traveler. Use the history below. 
    Respond ONLY as Sora reacting to Barnaby's last statement. 
    DO NOT summarize the Player or Barnaby. 20% chance that Sora 
    simply says "..." meaning he had nothing to add to the conversation
    
    <history>
    {chat_history}
    </history>
    
    Sora:"""

    s_response = client.models.generate_content(model=model_name, contents=sora_prompt)
    sora_text = s_response.text.strip().replace("Sora:", "").strip()

    chat_history += f"\nSora: {sora_text}"
    print(f"Sora: {sora_text}\n")

    # 5. Token Check
    print(f"[Tokens used this turn: {s_response.usage_metadata.total_token_count}]")
