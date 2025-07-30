import base64
from openai import OpenAI
from dotenv import load_dotenv
import os

def encode_image(image_path):
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_map_analysis(fragment_path):
    """Test if the model can correctly read and analyze a single map fragment."""
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    test_prompt = """You are an expert in urban geography. Your task is to analyze this map fragment and list ALL visible street names and landmarks you can see.

CRITICAL REQUIREMENTS:
1. List EVERY street name you can see, even if partially visible
2. List EVERY landmark or point of interest you can see
3. If you can't read something clearly, mark it as \"UNSURE: [what you can see]\"
4. DO NOT make assumptions about names you can't read clearly
5. DO NOT try to identify the city - just list what you can see

Your response MUST follow this exact structure:

1. Street Names:
   - [List each street name on a new line]
   - If unsure: \"UNSURE: [partial text]\"

2. Landmarks/Points of Interest:
   - [List each landmark on a new line]
   - If unsure: \"UNSURE: [partial text]\"

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