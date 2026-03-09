import ollama
import os

# No API keys required for local inference!
model_name = "gemma3:4b"

with open("lore.txt", "r") as f:
    game_lore = f.read()

chat_history = f"WORLD LORE:\n{game_lore}\n\n"

print("--- System: Local NPC Engine Started (No Token Limits) ---")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history += f"\nPlayer: {user_input}"

    # Prompt structure remains similar to your Gemini version
    barnaby_prompt = f"""
    You are Barnaby, a guard. Use this history:
    {chat_history}
    
    Respond only as Barnaby.
    Barnaby:"""

    # Calling the local model
    response = ollama.generate(model=model_name, prompt=barnaby_prompt)

    # Ollama returns a dictionary; the text is in 'response'
    barnaby_text = response["response"].strip()

    print(f"\nBarnaby: {barnaby_text}")
    chat_history += f"\nBarnaby: {barnaby_text}"
