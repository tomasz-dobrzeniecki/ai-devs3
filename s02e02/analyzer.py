import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

MAP_ANALYSIS_PROMPT = """You are an expert in urban geography and cartography, specializing in city map analysis and identification. Your task is to analyze the provided map fragments and determine their city of origin.

CRITICAL REQUIREMENTS:
1. Analyze each map fragment INDEPENDENTLY first
2. Look for street names, landmarks, and urban layout patterns
3. One fragment might be from a different city - identify it if present
4. Provide SPECIFIC evidence for your city identification
5. If uncertain about any element, mark it as \"UNSURE\" and explain why
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