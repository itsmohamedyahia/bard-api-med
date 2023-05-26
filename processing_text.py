import re


def get_file_content():

    with open('othercontent.txt', 'r') as file:
        content = file.read()
        return content


header = r"(\s+Contact : Class 38 Gastroenterology Module\s+Contents\s+\d+|\t+|\n+| {2,})"

processed_text = re.sub(header, " ", get_file_content())


# print(processed_text)


with open('output.txt', 'w', ) as file:
    file.write(processed_text)
