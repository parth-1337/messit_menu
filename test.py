import google.generativeai as genai

# PASTE YOUR KEY HERE
API_KEY = "AIzaSyBIlu0zn3FGanmkBnq7KZsnw81M1mn44hQ"
genai.configure(api_key=API_KEY)

print("Fetching available models...")
try:
    for m in genai.list_models():
        # We only want models that can generate text (content)
        if "generateContent" in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error fetching models: {e}")
