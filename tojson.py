import re
import json


def get_file_content():

    with open('output.txt', 'r') as file:
        content = file.read()
        return content


# pattern = r"(\d+)-(.+?)\s(?:a\)|b\)|c\)|d\))\s(.+?)(?=\s\d|$)"
# pattern = r"(\d+)-(.+?)\s(a\))\s(.+?)\s(b\))\s(.+?)\s(c\))\s(.+?)\s(d\))\s(.+?)(?=\s\d|$)"

pattern = r"(\d+)-(.+?)\s(?:a\))\s(.+?)\s(?:b\))\s(.+?)\s(?:c\))\s(.+?)\s(?:d\))\s(.+?)(?=\s\d|$)"


matches = re.findall(pattern, get_file_content())

questions = []

# for match in matches:
#     question_number = match[0]
#     question_text = match[1]
#     choice_a = match[2] + match[3]
#     choice_b = match[4] + match[5]
#     choice_c = match[6] + match[7]
#     choice_d = match[8] + match[9]
#     questions.append({
#         "question_number": question_number,
#         "question_text": question_text,
#         "choices": {
#             "a": choice_a,
#             "b": choice_b,
#             "c": choice_c,
#             "d": choice_d
#         }
#     })


for match in matches:
    question_number = match[0]
    question_text = match[1]
    choices = {
        "a": match[2].strip(),
        "b": match[3].strip(),
        "c": match[4].strip(),
        "d": match[5].strip()
    }

    result = {
        "question_number": question_number,
        "question_text": question_text,
        "choices": choices
    }

    questions.append(result)


# for match in matches:
#     question_number = match[0]
#     question_text = match[1].strip()
#     choices = {
#         "a": match[2].strip(),
#         "b": "",
#         "c": "",
#         "d": ""
#     }
#     questions.append({
#         "question_number": question_number,
#         "question_text": question_text,
#         "choices": {
#             "a": choice_a,
#             "b": choice_b,
#             "c": choice_c,
#             "d": choice_d
#         }
#     })

json_data = json.dumps(questions, indent=4)

with open('qna.txt', 'w') as file:
    content = file.write(json_data)
