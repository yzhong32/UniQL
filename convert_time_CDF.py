import fnmatch
import os
import re
from typing import List
import numpy as np
import matplotlib.pyplot as plt

def extract_convert_times(text):
    # 正则表达式匹配 "convert time:" 后的浮点数
    pattern = r"convert time:(\d+\.\d+) s"
    # 使用 re.findall 来找出所有匹配的浮点数
    matches = re.findall(pattern, text)
    # 将匹配到的字符串浮点数转换为浮点类型
    float_numbers = [float(num) for num in matches]
    return float_numbers

def read_log_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "文件未找到，请检查路径是否正确。"
    except Exception as e:
        return f"读取文件时出现错误: {e}"
    
def get_log_names(database:str, directory:str) -> List[str]:
    matching_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if fnmatch.fnmatch(filename, 'benchmark-{}-*-True-*.log'.format(database)):
                matching_files.append(os.path.join(root, filename))
    return matching_files

def draw_CDF(data_list: List[List[float]], labels: List[str], output: str):
    plt.figure(figsize=(8, 4))  # 设置图形大小
    for data, label in zip(data_list, labels):
        # 对数据进行排序
        data_sorted = np.sort(data)
        # 计算累积概率
        p = np.arange(1, len(data) + 1) / len(data)
        # 绘制CDF图
        plt.step(data_sorted, p, where="post", label=label)


    plt.xlabel("Conversion Time (seconds)", fontsize=24)  # 横坐标标签
    plt.ylabel("P(X ≤ time)", fontsize=24)  # 纵坐标标签
    plt.title("Conversion Time of Different Databases", fontsize=24)  # 图形标题
    plt.grid(True)  # 显示网格
    plt.legend()  # 显示图例
    plt.xlim((0, 25))
    plt.tight_layout() 

    plt.savefig(output)


if __name__ == '__main__':
    # databases = ["ES", "mongodb", "neo4j"]
    # convert_times_list = []
    # for db in databases:
    #     log_names = get_log_names(db, "./logs")
    #     convert_times = []
    #     for name in log_names:
    #         log_content = read_log_from_file(name)
    #         convert_times.extend(extract_convert_times(log_content))
    #     convert_times_list.append(convert_times)
    # draw_CDF(convert_times_list, databases, "cdf.png")
    log_content = read_log_from_file("./logs/benchmark-neo4j-wedding.json-gpt-4-turbo-True-2024-04-24#20:49:53.log")
    times = extract_convert_times(log_content)
    average = sum(times) / len(times)
    print(average)
