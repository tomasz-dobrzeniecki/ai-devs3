import cv2
import numpy as np
import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Prompt engineering
MAP_ANALYSIS_PROMPT = """You are an expert in urban geography and cartography, specializing in city map analysis and identification. Your task is to analyze the provided map fragments and determine their city of origin.

CRITICAL REQUIREMENTS:
1. Analyze each map fragment INDEPENDENTLY first
2. Look for street names, landmarks, and urban layout patterns
3. One fragment might be from a different city - identify it if present
4. Provide SPECIFIC evidence for your city identification
5. If uncertain about any element, mark it as "UNSURE" and explain why
6. NEVER guess or make assumptions about unclear elements
7. NEVER provide a city name without concrete evidence
8. Pay special attention to Droga Wojewódzka 534 (DW534) - this road passes through the city we're looking for

Your response MUST follow this exact structure:

1. Fragment Analysis (for each fragment):
   - Visible street names: [List]
   - Notable landmarks: [List]
   - Urban layout features: [Description]
   - Any unique characteristics: [Description]
   - DW534 presence/visibility: [Yes/No/Partial] and details if visible

2. City Identification:
   - City Name: [Name]
   - Confidence: [High/Medium/Low]
   - Key Evidence: [List specific streets/landmarks that confirm this city]
   - DW534 connection: [How this road connects to the city identification]

3. Inconsistency Check:
   - Is there a fragment from a different city? [Yes/No]
   - If Yes:
     * Which fragment: [Description]
     * Why different: [Explanation]
     * Possible origin: [City name]
     * Evidence: [List]

4. Verification:
   - How verified: [Explanation]
   - Uncertainties: [List if any]
   - DW534 verification: [How the road's presence supports the identification]

5. Additional Notes:
   - Patterns: [Description]
   - Limitations: [Description]
   - DW534 observations: [Any specific details about the road's path or features]

IMPORTANT: 
1. If you identify a city, you MUST provide specific street names or landmarks that exist in that city as evidence. Do not rely on general patterns alone.
2. The presence of DW534 is a crucial clue - if you see it, note its exact path and any intersections or landmarks along it."""

def split_image_into_maps(image_path):
    """Split the input image into separate map fragments using horizontal and vertical line detection."""
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")
    
    # Convert to grayscale and threshold
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)
    
    height, width = binary.shape
    print(f"Image size: {width}x{height}")
    
    # Find horizontal lines
    horizontal_lines = [0]  # Start with top edge
    for y in range(height):
        if np.all(binary[y, :] == 255):  # White line
            horizontal_lines.append(y)
    horizontal_lines.append(height)  # Add bottom edge
    
    # Find vertical lines for each horizontal section
    map_fragments = []
    for i in range(len(horizontal_lines) - 1):
        y1, y2 = horizontal_lines[i], horizontal_lines[i + 1]
        if y2 - y1 < 100:  # Skip small fragments
            continue
            
        fragment = binary[y1:y2, :]
        if np.mean(fragment) > 250:  # Skip mostly white fragments
            continue
        
        # Find vertical lines in this section
        vertical_lines = [0]  # Start with left edge
        for x in range(width):
            if np.all(fragment[:, x] == 255):  # White line
                vertical_lines.append(x)
        vertical_lines.append(width)  # Add right edge
        
        # Create fragments
        for j in range(len(vertical_lines) - 1):
            x1, x2 = vertical_lines[j], vertical_lines[j + 1]
            if x2 - x1 < 100:  # Skip small fragments
                continue
                
            sub_fragment = fragment[:, x1:x2]
            if np.mean(sub_fragment) > 250:  # Skip mostly white fragments
                continue
                
            if np.mean(sub_fragment) < 255 * 0.95:  # Keep fragments with text
                map_fragments.append((x1, y1, x2, y2))
    
    # Sort fragments by position
    map_fragments.sort(key=lambda x: (x[1], x[0]))
    
    # Save fragments
    fragment_paths = []
    for i, (x1, y1, x2, y2) in enumerate(map_fragments):
        fragment = img[y1:y2, x1:x2]
        fragment_path = f"map_fragment_{i}.jpg"
        cv2.imwrite(fragment_path, fragment)
        fragment_paths.append(fragment_path)
        print(f"Saved fragment {i} (size: {x2-x1}x{y2-y1})")
    
    print(f"Found {len(fragment_paths)} map fragments")
    return fragment_paths

def encode_image(image_path):
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_map_fragments(fragment_paths, excluded_cities=None):
    """Analyze map fragments using GPT-4.1-mini."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    # Add excluded cities to prompt if any
    prompt = MAP_ANALYSIS_PROMPT
    if excluded_cities:
        prompt += f"\n\nEXCLUDED CITIES (these are definitely NOT the correct answer): {', '.join(excluded_cities)}"
    
    # Prepare messages with images
    messages = [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            *[{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64.b64encode(open(path, 'rb').read()).decode('utf-8')}"}} 
              for path in fragment_paths]
        ]
    }]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=4096,
            temperature=0.3
        )
        
        response_text = response.choices[0].message.content
        with open("llm_response.txt", 'w', encoding='utf-8') as f:
            f.write(response_text)
        
        print("\nAnalysis complete! Response saved to llm_response.txt")
        
        return response_text
        
    except Exception as e:
        print(f"Error during API call: {str(e)}")
        return None

def test_map_analysis(fragment_path):
    """Test if the model can correctly read and analyze a single map fragment."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    test_prompt = """You are an expert in urban geography. Your task is to analyze this map fragment and list ALL visible street names and landmarks you can see.

CRITICAL REQUIREMENTS:
1. List EVERY street name you can see, even if partially visible
2. List EVERY landmark or point of interest you can see
3. If you can't read something clearly, mark it as "UNSURE: [what you can see]"
4. DO NOT make assumptions about names you can't read clearly
5. DO NOT try to identify the city - just list what you can see

Your response MUST follow this exact structure:

1. Street Names:
   - [List each street name on a new line]
   - If unsure: "UNSURE: [partial text]"

2. Landmarks/Points of Interest:
   - [List each landmark on a new line]
   - If unsure: "UNSURE: [partial text]"

3. Additional Observations:
   - [Any other notable features or text you can see]"""
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": test_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(fragment_path)}"}}
            ]
        }
    ]
    
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            max_tokens=1024,
            temperature=0.1  # Very low temperature for most accurate reading
        )
        
        test_response = response.choices[0].message.content
        print("\nTest Analysis Results:")
        print("=" * 50)
        print(test_response)
        print("=" * 50)
        
        # Save test response
        with open("test_analysis.txt", 'w', encoding='utf-8') as f:
            f.write(test_response)
        
        return test_response
        
    except Exception as e:
        print(f"Error during test analysis: {str(e)}")
        return None

def main():
    """Main execution function."""
    map_path = "map2.jpg"
    if not os.path.exists(map_path):
        print(f"Error: {map_path} not found!")
        return
    
    try:
        # Split map into fragments
        print("Splitting map into fragments...")
        fragment_paths = split_image_into_maps(map_path)
        
        if not fragment_paths:
            print("Error: No valid map fragments found!")
            return
        
        # Test analysis of first fragment
        print("\nTesting map fragment analysis...")
        test_result = test_map_analysis(fragment_paths[0])
        if not test_result:
            print("Warning: Test analysis failed! The model might not be able to read the map correctly.")
            return
        
        # Analyze fragments
        print("\nAnalyzing fragments...")
        excluded_cities = ["Bielsko-Biała", "Toruń", "Kraków", "Warszawa", "Olsztyn", "Bydgoszcz"]
        response = analyze_map_fragments(fragment_paths, excluded_cities=excluded_cities)
        
        if response:
            print("\nAnalysis complete! Please check llm_response.txt for full details.")
            print("Remember to enter the city name in the 'Znaleziona Flaga' field in the UI.")
        
    except Exception as e:
        print(f"Error during execution: {str(e)}")

if __name__ == "__main__":
    main() 