import google.generativeai as ai
import glob
import os
from PIL import Image

# API KEY
MY_API_KEY = "AIzaSyAXuNYzRF7CBfTpCOQ8VGfJzBu9KD14y50"
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
1. **EXPAND ALL DATE RANGES:** If the image says "7th - 9th", you MUST create three separate entries: one for the 7th, one for the 8th, and one for the 9th. All with the same food.
2. **NO SKIPPED DAYS:** Look at the start date and end date on the page. Ensure every single day in between is listed in the JSON.
3. **HANDLE 'DITTO' OR 'SAME':** If a day says "Same as above" or "Ditto", copy the food items from the previous day. Do not leave it blank.
4. **FORMAT:** - Type 1=Breakfast, 2=Lunch, 3=Snacks, 4=Dinner.
   - Date format: YYYY-MM-DD.
   - No newlines (\\n) in menu strings; use commas.
   - Return ONLY valid JSON.
"""


response = model.generate_content([prompt] + loaded_images)

# added by claude removes that json added by gemini in output
clean_json = response.text.replace("```json", "").replace("```", "").strip()
clean_json = clean_json.replace("\\n", ", ")

with open("menu.json", "w") as f:
    f.write(clean_json)

print("Saved")
