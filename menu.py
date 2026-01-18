import google.generativeai as ai
import json
from PIL import Image
import cv2
import numpy as np

API_KEY = "AIzaSyBIlu0zn3FGanmkBnq7KZsnw81M1mn44hQ"
ai.configure(api_key=API_KEY)

# 1.5 doesnt work only 2.5 flash
# 3 flash-preview also working
model = ai.GenerativeModel("gemini-2.5-flash")


image_file = Image.open("menu.jpg")


# image rotateer

if image_file.height > image_file.width:
    print("Rotated")
    image_file = image_file.rotate(90, expand=True)

# image cvt black and white
grey_img = cv2.cvtColor(np.array(image_file), cv2.COLOR_BGR2GRAY)
cv2.imwrite("grey_image.jpg", grey_img)

# change array back to image format
final_img = Image.fromarray(grey_img)

'''
# PROMPT
prompt = """
Look at this mess menu image. Extract the data into this exact JSON format:

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

Rules:
1. Type 1 is Breakfast, 2 is Lunch, 3 is Snacks, 4 is Dinner.
2. Convert dates to YYYY-MM-DD.
3. If a slot is empty, just leave the string empty.
4. Give me ONLY the JSON code. No extra text.
5. IMPORTANT: Never use '\n' (newlines) inside the menu strings. If text is on multiple lines, join them with a comma and a space.
"""

print("Image sent to api")
response = model.generate_content([prompt, final_img])

# added by claude removes that json added by gemini in output
clean_json = response.text.replace("```json", "").replace("```", "").strip()


# save

with open("menu.json", "w") as my_file:
    my_file.write(clean_json)

print("Saved")
'''
