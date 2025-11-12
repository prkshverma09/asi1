import os
import requests
import base64
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("ASI_ONE_API_KEY")

API_KEY = os.getenv("ASI_ONE_API_KEY")
BASE_URL = "https://api.asi1.ai/v1"

headers = {
"Authorization": f"Bearer {API_KEY}",
"Content-Type": "application/json",
}

payload = {
"prompt": "A futuristic city skyline at sunset with flying cars",
"size": "1024x1024",
"model": "asi1-mini",
}

response = requests.post(
f"{BASE_URL}/image/generate",
headers=headers,
json=payload,
)

# Parse JSON response and save the image

if response.status_code == 200:
    result = response.json()

    # Extract base64 image from url field
    if "images" in result and len(result["images"]) > 0:
        image_url = result["images"][0]["url"]

        # Check if it's a data URL with base64
        if image_url.startswith("data:image/"):
            # Extract base64 data (remove data:image/png;base64, prefix)
            base64_data = image_url.split(",", 1)[1]

            # Decode base64 to binary
            image_data = base64.b64decode(base64_data)

            # Save to file
            with open("generated_image.png", "wb") as f:
                f.write(image_data)
            print("Image saved as 'generated_image.png'")
        else:
            print(f"Unexpected URL format: {image_url[:100]}...")
    else:
        print("No images found in response")

else:
    print(f"Error: {response.status_code}")
    print(response.text)

