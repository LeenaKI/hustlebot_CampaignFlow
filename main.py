import os
import json
from google import genai
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
api_keys = os.getenv("GEMINI_API_KEYS", "").split(",")

def generate_campaign(input_file):
    # 1. Load the dynamic user input
    with open(input_file, 'r', encoding='utf-8') as f:
        user_data = json.load(f)

    # 2. Define the Architectural System Prompt
    system_prompt = """
    You are an expert HustleBot Drip Campaign Architect.
    
    INSTRUCTIONS:
    1. Step Count: Generate exactly the number of steps requested in 'flow_length_(steps)'.
    2. Anonymization: NEVER use employee names. Use functional titles (e.g., 'Sales Advisory Team', 'Quality Assurance Team').
    3. Mandatory Feedback: After the visitor selects a time slot, always append: "Our team will attend to you ASAP."
    4. Output: Return RAW JSON ONLY. No markdown (```json), no pre-amble, no conversational filler.
    5. Logic: Use the provided JSON input to drive the campaign structure. If 'Additional_context' is provided, extract business facts and weave them into the copy.
    """

    # 3. Execution with Failover Logic
    for key in api_keys:
        try:
            client = genai.Client(api_key=key.strip())
            
            prompt = f"System: {system_prompt}\n\nUser Campaign Data: {json.dumps(user_data)}"
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            
            # 4. Save Output
            with open("campaign_output.json", "w", encoding="utf-8") as f:
                f.write(response.text)
            
            print(f"Success! Campaign generated. Saved to campaign_output.json")
            return
            
        except Exception as e:
            print(f"Key failed, trying next... Error: {e}")
            continue
            
    print("Failed to generate campaign after trying all keys.")

if __name__ == "__main__":
    generate_campaign("input.json")