import google.generativeai as ai
import glob
import os
from PIL import Image

# API KEY
MY_API_KEY = "API KEY"
ai.configure(api_key=MY_API_KEY)
model = ai.GenerativeModel("gemini-2.5-flash")

# glob will find all jpg in images folder
image_folder = "images"
image_paths = glob.glob(os.path.join(image_folder, "*.jpg"))


loaded_images = []

for path in image_paths:
    img = Image.open(path)

    # ROTATER
    if img.height > img.width:
        img = img.rotate(90, expand=True)

    loaded_images.append(img)


print("Sent")

prompt = """
Look at these mess menu images. Extract the data into this exact JSON format:
[
  {
    "date": "YYYY-MM-DD",
    "menu": [
      { "type": 1, "menu": "Food items here" },
      { "type": 2, "menu": "Food items here" },
      { "type": 3, "menu": "Food items here" },
      { "type": 4, "menu": "Food items here" }
    ]
  }
]

CRITICAL RULES:
1. **VISUALS ONLY:** Only extract dates that are EXPLICITLY printed on the page. Do NOT guess missing days.
2. **ALLOW GAPS:** If the menu jumps from the 8th to the 15th, your JSON must also jump. Do NOT fill in the 9th-14th.
3. **PARTIAL DATA:** If I only upload one week, only give me that one week. Do not generate a full month.
4. **EXPAND RANGES:** If a specific text says "7th - 9th", you MUST create separate entries for 7, 8, and 9.
5. **FORMAT:** - Type 1=Breakfast, 2=Lunch, 3=Snacks, 4=Dinner.
   - Date format: YYYY-MM-DD.
   - No newlines (\\n) in menu strings; use commas.
"""


response = model.generate_content([prompt] + loaded_images)

# added by claude removes that json added by gemini in output
clean_json = response.text.replace("```json", "").replace("```", "").strip()
clean_json = clean_json.replace("\\n", ", ")

with open("menu.json", "w") as f:
    f.write(clean_json)

print("Saved")
