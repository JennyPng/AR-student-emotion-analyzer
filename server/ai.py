import os
from openai import OpenAI
import json

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def read_file(file_path="clarify_prompt.txt"):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            return file_content
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def clarify_lecture(transcript):
    prompt = read_file() + transcript
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100
    )
    response = response.choices[0].text
    print(response)
    # parse json
    try:
        data = json.loads(response)
        print(data) 
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        data = {'confusing_topics': []}

    return data

if __name__ == "__main__":
    data = clarify_lecture("linear programming")
    print(data)