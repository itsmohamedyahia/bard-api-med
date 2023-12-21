import bardapi
import os
import json
import time
import random

######### CONSTANTS ########
##'b,b,b,c,b,e,a,e,c,a,b,d,a,a,b,b,a,a,c,a,e,c,c,b,a,d,a,e,a,c,b'

INPUT_DIR = '#input'  

########### DEFINITIONS ###########

def confirmFileInInput(): 
    answer_to_file_confirm = input('new file in #input? (yes/y)').lower()
    if answer_to_file_confirm != 'yes' and answer_to_file_confirm != 'y':
        print(answer_to_file_confirm)
        confirmFileInInput()

def get_file():
    '''return file path, name in #input dir'''
    print('Checking file in #input')
    
    all_items = os.listdir(INPUT_DIR)

    if len(all_items) == 1:  # Check if there's only one item in the folder
        file_path = os.path.join(INPUT_DIR, all_items[0])
        print('Successful selection of #input file')
        
        file_name = file_path.split("\\")[1].split('.')[0]
        
        return {
            'file_path': file_path,
            'file_name': file_name
        }
    else:
        print("Multiple/No Files Detected. Put only one file in #input dir")
    return -1

def getData(file):
    '''Return list (array in js)'''
    with open(file, 'r') as file:
        array = json.load(file)
        
        returnValue = {
          'data_list': array,
          'data_len': len(array)  
        } 
        return returnValue

def get_answers(data_len):
    answers = input('Answers (in a,b,a,c format)?')
    answers_list = answers.split(',')
    if len(answers_list) != data_len:
        print('Not valid. Try again')
        get_answers(data_len)
    print('ANSWERS. OK.')
    return answers_list

def combine_choices_and_answer(question_dict, noans):
    question = question_dict['question']
    choices = question_dict['choices']
    answer = question_dict['answer']

    # Create a list to store the combined choices and answer
    combined_choices = []

    # Iterate over the choices dictionary and combine each choice with its key
    for key, choice in choices.items():
        combined_choices.append(f"{key}. {choice}")

    if noans == "default":
        # Combine the choices and answer into a single string
        combined_choices_text = "\n".join(combined_choices)
        combined_string = f"{question}\n{combined_choices_text}\n\nAnswer: {answer}"

    elif noans == "noans":
        combined_choices_text = "> " + "\n\n> ".join(combined_choices)
        combined_string = f"{question}\n\n{combined_choices_text}\n\n**Answer** : {answer}"

    return combined_string

def add_answer_key_to_list_of_question_objects(list, answers):
    '''add answer and explanation keys to list of question objects'''
    list_with_answerKey = []
    for index, obj in enumerate(list):
        # new_obj = question(obj.question, obj.choices, answer=answers[index])
        new_obj = {**obj, "answer": answers[index]}
        list_with_answerKey.append(new_obj)
    return list_with_answerKey

def makePrompts(list, prompt_header="", prompt_footer = ""):
    '''Takes a list of question objects and returns a list of prompt strings'''
    prompts = []
    prompt_header = 'explain why answer is correct with terminology'
    prompt_footer = 'WHY (start with the right answer first)'
    for q in list:
        prompt = prompt_header + \
            "\n\n" + combine_choices_and_answer(q, 'default')+  \
            "\n\n" + prompt_footer
        prompts.append(prompt)
    return prompts

def getBardExplanations(prompts):
    '''Takes a list of prompts and returns a list of explanations strings'''
    explanations = []
    
    print('gettting Bard Response') 
    
    for prompt in prompts:
        explanation = getBardExplanation(prompt)
        explanations.append(explanation)
        time.sleep(random.randint(3, 4, 5 ))
        
    print('SUCCESSFUL RESPONSE.')
    return explanations

def getBardExplanation(prompt):
    
    response = bardapi.core.Bard(timeout=25).get_answer(prompt)
    content = response['content']
    # if len(content) < 80:
    #     getBardExplanation(prompt)
    
    return content
    
def addExplanationsToListOfQuesObj(list, explanations):
    new_list = []

    for index, obj in enumerate(list):
        new_obj = {**obj, 'explanation': explanations[index]}
        new_list.append(new_obj)

    return new_list

def store_in_json(file_name, list):
    path = f"#output/{file_name}.json"
    json_data = json.dumps(list, indent=4)

    with open(path, 'w') as file:
        file.write('')
    with open(path, 'a') as file:
        file.write(json_data)

def store_in_read_mode(file_name, list):
    path = f"#output/read_{file_name}.md"
    increment = 0
    with open(path, 'w') as file:
        file.write("")

    with open(path, 'a',encoding="utf-8") as file:
        for obj in list:
            text = f"**Question{obj['question_number']}** : " + combine_choices_and_answer(obj, 'noans') + '\n\n' + \
                f"**Explanation** :\n\n{obj['explanation']}"
            file.write(text)
            file.write("\n\n----------------------------------------\n\n")
            increment += 1
    return

########### APP ###########
os.environ['_BARD_API_KEY'] = input('Secure-1PSID Key? ')
confirmFileInInput()

fileDict = get_file()
file_path = fileDict['file_path']
file_name = fileDict['file_name']

data = getData(file_path)
data_list = data['data_list']
data_len = data['data_len']

answers_list = get_answers(data_len)

data_list_with_ans_key = add_answer_key_to_list_of_question_objects(
    data_list, answers_list)

prompts = makePrompts(data_list_with_ans_key)
explanations = getBardExplanations(prompts)

data_list_with_exp = addExplanationsToListOfQuesObj(
    data_list_with_ans_key, explanations)

store_in_read_mode(file_name, data_list_with_exp)

store_in_json(file_name, data_list_with_exp)

print('DONE')

