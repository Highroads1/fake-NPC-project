import os
from dotenv import load_dotenv
from google import genai

# 1. Environment Setup
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
model_name = "gemini-2.5-flash-lite"

# 2. Load the "Lore" from your txt file
with open("lore.txt", "r") as f:
    game_lore = f.read()

# 3. Define the NPCs
npc1_name = "Barnaby (The Curious Guard)"
npc2_name = "Sora (The Wise Traveler)"

# 4. NPC 1 initiates a question
q_prompt = f"""
Context: {game_lore}
You are {npc1_name}. You heard a rumor about a new island but aren't sure of the details.
Ask {npc2_name} a specific question about the new island's name or how to get there.
Keep it casual and in-character.
"""

# We store the FULL response object so we can access usage_metadata later
q_response = client.models.generate_content(model=model_name, contents=q_prompt)
question_text = q_response.text.strip()
print(f"{npc1_name}: {question_text}\n")

# 5. NPC 2 answers using the lore file
a_prompt = f"""
Context: {game_lore}
You are {npc2_name}. You know the facts found in the Context.
{npc1_name} just asked: "{question_text}"
Answer the question accurately using ONLY the information in the Context. 
If the info isn't there, say you don't know. Keep it in-character.
"""

a_response = client.models.generate_content(model=model_name, contents=a_prompt)
answer_text = a_response.text.strip()
print(f"{npc2_name}: {answer_text}")

# 6. Session Stats (using the metadata from the last response)
usage = a_response.usage_metadata
print("\n" + "-" * 30)
print("📊 SESSION STATS:")
print(f"Tokens Used (Last Turn): {usage.total_token_count}")
print(f"Daily Quota: ~{1000}")
print("-" * 30)
