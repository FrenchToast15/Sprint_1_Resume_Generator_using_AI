import json


def save_to_json(content, filename="response.json"):
    """Saves the generated Markdown response to a JSON file."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"markdown": content}, f, indent=4, ensure_ascii=False)
        print(f"\nResponse saved to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")
