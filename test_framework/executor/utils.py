import re

def format_sql_field(field_name):
    converted_name = re.sub(r'\((.*?)\)', lambda m: '_' + m.group(1), field_name)
    converted_name = converted_name.replace('.', '_')
    return converted_name

if __name__ == '__main__':
    original_field_name = "avg(longitude)"
    converted_field_name = format_sql_field(original_field_name)
    print(converted_field_name)

    original_field_name = "students.score"
    converted_field_name = format_sql_field(original_field_name)
    print(converted_field_name)

    original_field_name = "avg(students.score)"
    converted_field_name = format_sql_field(original_field_name)
    print(converted_field_name)