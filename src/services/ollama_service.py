import re
import json
import ollama
from typing import Dict, List


async def describe_image(image_paths: List[str]) -> Dict[str, any]:
    prompt = """
        Describe this image and extract any visible text, 
        including poster titles, actor names, and scene details. 
        Return output in JSON with fields: movie_title, actors, year, extracted_text.
    """

    try:
        response = ollama.chat(
            model="gemma3-film-extractor:latest",
            messages=[{"role": "user", "content": prompt, "images": image_paths}],
        )
    except Exception as e:
        return {"error": f"Ollama request failed: {str(e)}"}

    raw_content = response["message"]["content"]

    # Strip ```json ... ``` code block if present
    match = re.search(r"```json\s*(\{.*?\})\s*```", raw_content, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = raw_content

    # Convert string to dict
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": raw_content}
