import os
import json
import time
import requests
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Constants
ROBOT_DESCRIPTION_URL = "https://c3ntrala.ag3nts.org/data/7f6ff94a-ced2-46e2-8c90-aa4fdec3b948/robotid.json"
CENTRALA_REPORT_URL = "https://c3ntrala.ag3nts.org/report"
API_KEY = "7f6ff94a-ced2-46e2-8c90-aa4fdec3b948"

def get_robot_description():
    """Fetch the current robot description from the API."""
    try:
        response = requests.get(ROBOT_DESCRIPTION_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching robot description: {e}")
        return None

def generate_robot_image(description):
    """Generate robot image using DALL-E 3."""
    try:
        # Create a prompt that emphasizes factory setting and robot details
        prompt = f"Create a detailed image of a robot in a factory setting. {description} The image should be photorealistic and show the robot in its industrial environment."
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        # Get the URL of the generated image
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def send_to_centrala(image_url):
    """Send the image URL to Centrala."""
    payload = {
        "task": "robotid",
        "apikey": API_KEY,
        "answer": image_url
    }
    
    try:
        response = requests.post(CENTRALA_REPORT_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        if result.get('code') == 0:
            print(f"Successfully sent to Centrala: {result}")
            return True
        return False
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Centrala: {e}")
        return None

def main():
    while True:
        print(f"\n[{datetime.now()}] Starting new robot generation cycle...")
        
        # Step 1: Get robot description
        description_data = get_robot_description()
        if not description_data:
            print("Failed to get robot description. Retrying in 60 seconds...")
            time.sleep(60)
            continue
            
        print(f"Got robot description: {description_data}")
        
        # Step 2: Generate image
        image_url = generate_robot_image(description_data)
        if not image_url:
            print("Failed to generate image. Retrying in 60 seconds...")
            time.sleep(60)
            continue
            
        print(f"Generated image URL: {image_url}")
        
        # Step 3: Send to Centrala
        result = send_to_centrala(image_url)
        if result is None:
            print("Failed to send to Centrala. Retrying in 60 seconds...")
            time.sleep(60)
            continue
        elif result:
            # If we got code 0, exit the program
            break
            
        # If we got here, we need to retry after 60 seconds
        print("Waiting 60 seconds before next attempt...")
        time.sleep(60)

if __name__ == "__main__":
    main() 