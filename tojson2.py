import re
import json


def get_file_content():

    with open('output.txt', 'r') as file:
        content = file.read()
        return content


pattern = r"(\d+)-(.*?)(?=(?:\s\d+-|\Z))"
matches = re.findall(pattern, get_file_content())

results = []

for match in matches:
    question_number = match[0]
    question_text = match[1].strip()
    choices = {}

    # Extract answer choices using a separate pattern
    choices_pattern = r"([a-d])\)\s(.*?)(?=\s[a-d]\)|\Z)"
    answer_choices = re.findall(choices_pattern, match[1])

    for choice in answer_choices:
        choice_key = choice[0]
        choice_text = choice[1].strip()
        choices[choice_key] = choice_text

    result = {
        "question_number": question_number,
        "question_text": question_text,
        "choices": choices
    }

    results.append(result)


# Convert results to JSON
json_data = json.dumps(results, indent=4)

with open('qna.txt', 'w') as file:
    content = file.write(json_data)
