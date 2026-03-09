import ollama
import os

# 1. Configuration
# Make sure to run: ollama create barnaby-model -f Modelfile in Bash/Powershell
MODEL_NAME = "barnaby-model"
LORE_FILE = "lore.txt"
HISTORY_LIMIT = 6  # Keeps the last 6 exchanges (Player + NPC)

# 2. Load the "Truth"
if not os.path.exists(LORE_FILE):
    with open(LORE_FILE, "w") as f:
        f.write("The island of Whispering Reach is to the North. Level 20 required.")

with open(LORE_FILE, "r") as f:
    game_lore = f.read()

# 3. Initialize History List
chat_history_list = []


def get_formatted_context(history_list):
    """Trims history to the limit and formats it for the prompt."""
    recent = history_list[-HISTORY_LIMIT:]
    return "\n".join(recent)


print(f"--- System: Connected to Local Model '{MODEL_NAME}' ---")
print("--- Type 'exit' to quit. ---\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    chat_history_list.append(f"Player: {user_input}")
    context_window = get_formatted_context(chat_history_list)

    full_prompt = (
        f"### LORE:\n{game_lore}\n\n### HISTORY:\n{context_window}\n\nBarnaby:"
    )

    try:
        # The 'response' object is actually a dictionary with metadata
        response = ollama.generate(model=MODEL_NAME, prompt=full_prompt)

        barnaby_text = response["response"].strip()

        # 1. Extract the durations (Ollama returns these in nanoseconds)
        # total_duration includes loading the model, prompt eval, and generation
        total_sec = response["total_duration"] / 1e9
        # eval_duration is just the time spent "typing" the response
        gen_sec = response["eval_duration"] / 1e9

        print(f"\nBarnaby: {barnaby_text}")

        # 2. Display the performance stats
        print(f"[⏱️ Response: {total_sec:.2f}s | 🧠 Gen: {gen_sec:.2f}s]\n")

        chat_history_list.append(f"Barnaby: {barnaby_text}")

    except Exception as e:
        print(f"Error: {e}")
        break

print("\n--- Session Ended ---")
