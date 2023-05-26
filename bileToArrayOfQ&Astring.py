import re
import json


def bileToArrayOfQandAString():
    with open('output.txt', 'r') as file:
        bile = file.read()
        return bile


questions = re.findall(r"\d+-(.*?d\).*?)(?=\d+-|$)",
                       bileToArrayOfQandAString(), re.DOTALL)

formatted_questions = [question.strip() for question in questions]

# print(arrayOfQandA)


json_data = json.dumps(formatted_questions, indent=4)

with open('qna.txt', 'w') as file:
    content = file.write(json_data)
