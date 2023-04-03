import csv
from datetime import datetime
import re
import zhconv

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

def main(filename):
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

    print(merged_string)
    return merged_string

if __name__ == '__main__':
    filename = ''
    main(filename)