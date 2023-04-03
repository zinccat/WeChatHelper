import csv
from datetime import datetime
import re
import zhconv
import openai
import os

# use your own OPENAI API key
openai.api_key = 'sk-xxxxxxxxxxx'

def formatting(s, user):
    # s, flag = formatting_ref(s)
    flag = False
    ref_type = is_ref(s)
    if ref_type == 1:
        s, flag = formatting_ref(s, user)
    elif ref_type == 2:
        s, flag = formatting_ref2(s, user)
    s, _ = formatting_cn(s)
    if flag:
        return s
    s, flag = formatting_at(s, user)
    if flag:
        return s
    else:
        return f"[{user}]说'{s}'. ".format(user=user, output_text=s)

def formatting_cn(s):
    # 繁简转换
    s = zhconv.convert(s, 'zh-cn')
    return s, False

def is_ref(s):
    if re.search(r"- - - - - - - - - - - - - - - -", s):
        if re.search(r"<", s):
            # complex
            return 2
        return 1
    else:
        return 0

def formatting_ref(s, user):
    # Use regular expressions to extract the three parts of the string
    match = re.search(r'「(.*?)：(.*?)」\n.*?\n(.*?)$', s, re.DOTALL)
    if match is None:
        return s, False
    # Format the extracted parts into the desired output string
    user2 = match.group(1)
    last_message = match.group(2).lstrip('\n')
    message = match.group(3)
    if len(last_message) > 50:
        s = "[{}]回复[{}]说'{}'. ".format(user, user2, message)
    else:
        s = "[{}]回复[{}]说的'{}', 说'{}'. ".format(user, user2, last_message, message)
    return s, True


def formatting_ref2(s, user):
    pattern = r'- - - - - - - - - - - - - - - -\n(.*)'
    # Use re.search() to find the first occurrence of the pattern in the input string
    match = re.search(pattern, s)
    if match is None:
        return s, False
    # Extract the string after the delimiter
    extracted_str = match.group(1)
    return extracted_str, False

def formatting_at(s, user):
    if s[0] == '@' and ' ' in s:
        splitted = s.split(' ')
        user2 = splitted[0][1:]
        if len(splitted) > 1:
            message = ' '.join(splitted[1:])
        else:
            message = ""
        s = "[{}]对[{}]说'{}'. ".format(user, user2, message)
        return s, True
    return s, False

def merge(filename):
    # filename = ''
    data = []
    with open(filename, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            data.append(row)

    # Filter data with time as today
    today = datetime.now().strftime('%Y-%m-%d')
    filtered_data = [row for row in data if row['Time'].startswith(today)]

    # Merge all data into a single string
    merged_string = ''
    for row in filtered_data:
        input_text = row['Text']
        # output_text = re.sub(r'<[^>]*>', '', input_text)
        # output_text = re.sub(r'[-」]+', '', output_text)
        output_text = formatting(input_text, user=row['User'])
        merged_string += output_text

    return merged_string

def gpt(inputs: str, model: str = "gpt-3.5-turbo", temperature: float = 0.3) -> str:
    prompt = """你是一个群聊信息助手, 请为以下群聊消息按照话题分点撰写详细的总结, 其中[]扩起的为用户昵称, ''扩起的为消息.

格式:
1.
2.
3."""

    output = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": inputs},
        ],
        temperature=temperature
    )
    return output.choices[0]['message']['content']

if __name__ == '__main__':
    filename = 'filepath'
    merged_string = merge(filename)
    print("Before summary:\n", merged_string)
    print("-"*80)
    print("After summary:\n", gpt(merged_string)) #, model='gpt-4'))