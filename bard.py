import bardapi
import os
import json

os.environ['_BARD_API_KEY'] = 'Wgit8_Eedsm5RXifldhMrJf2YrncEivy5OKwsbipurrVyvNrMqGFSEjx7pnUgNi3B0xuKg.'


def getQ():
    with open('data/git-class38-endmod-group1.json', 'r') as file:
        array = json.load(file)
        return array


def combine_choices_and_answer(question_dict):
    question = question_dict['question']
    choices = question_dict['choices']
    answer = question_dict['answer']

    # Create a list to store the combined choices and answer
    combined_choices = []

    # Iterate over the choices dictionary and combine each choice with its key
    for key, choice in choices.items():
        combined_choices.append(f"{key}. {choice}")

    # Combine the choices and answer into a single string
    pro = "\n".join(combined_choices)
    combined_string = f"{question}\n{pro}\n\nAnswer: {answer}"

    return combined_string


array = getQ()

prompts = []

for q in array:
    prompt = "explain in a detailed argumentive academic paragraph why each choice is right or wrong" + \
        "\n\n" + combine_choices_and_answer(q)
    prompts.append(prompt)


for prompt in prompts:
    response = bardapi.core.Bard(timeout=14).get_answer(prompt)
    content = response['content']
    with open('git-class38-endmod-group1.json', 'a') as file:
        file.write(f"{prompt}\n\n {content}")
