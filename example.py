import os
import json
from dotenv import load_dotenv

def main():
    print("--- HustleBot Dummy Script ---")
    
    # 1. Test Dotenv Loading
    load_dotenv()
    api_keys_raw = os.getenv("GEMINI_API_KEYS", "")
    api_keys = [k.strip() for k in api_keys_raw.split(",") if k.strip()]
    
    print(f"Loaded API Keys count: {len(api_keys)}")
    if not api_keys:
        print("Warning: No GEMINI_API_KEYS found in .env file.")
    
    # 2. Test Reading input.json
    input_path = "input.json"
    if os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                category = data.get("flow_category", "Unknown")
                audience = data.get("target_audience", "Unknown")
                print(f"Successfully loaded input.json. Category: '{category}', Target Audience: '{audience}'")
            except json.JSONDecodeError:
                print("Error: input.json is not valid JSON.")
    else:
        print("Warning: input.json not found in the current directory.")
        
    print("------------------------------")
    print("Ready to run real campaigns!")

if __name__ == "__main__":
    main()
