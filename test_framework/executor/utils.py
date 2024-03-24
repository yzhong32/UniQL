import re

def convert_field_to_no_brace(field_name):
    converted_name = re.sub(r'\((.*?)\)', lambda m: '_' + m.group(1), field_name)
    return converted_name

if __name__ == '__main__':
    original_field_name = "avg(longitude)"
    converted_field_name = convert_field_to_no_brace(original_field_name)
    print(converted_field_name)