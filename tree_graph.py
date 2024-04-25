import pandas as pd
import matplotlib.pyplot as plt
import squarify

dtype_map = {
    'join': 'bool',
    'aggregation': 'bool',
    'subquery': 'bool'
}

# 读取CSV文件，指定列的数据类型
df = pd.read_csv("./Query_classification.csv", dtype=dtype_map)

# 计算每种组合的出现次数
combination_counts = df.groupby(['join', 'aggregation', 'subquery']).size().reset_index(name='counts')
total = combination_counts['counts'].sum()
combination_counts['proportion'] = combination_counts['counts'] / total
combination_counts['proportion_str'] = combination_counts['proportion'].apply(lambda x: f"{x * 100:.2f}%")

# labels = combination_counts.apply(lambda x: f"Join: {x['join']}\nAggregation: {x['aggregation']}\nSubquery: {x['subquery']}\nCount: {x['counts']}", axis=1)
legend_labels = []
def create_label(row):
    tags = ("J" if row["join"] else None, "A" if row['aggregation'] else None, "S" if row['subquery'] else None)
    legend_label = "+".join([tag for tag in tags if tag is not None])
    legend_label = legend_label if legend_label != "" else "Simple"
    legend_labels.append(legend_label)
    return f"{row['proportion_str']}"

labels = combination_counts.apply(create_label, axis=1)
sizes = combination_counts['proportion']
cmap = plt.get_cmap('Set3')
colors = [cmap(i) for i in range(len(sizes))]


# 绘制树形图

plt.rc('font', size=40)
plt.figure(figsize=(20, 10))
squarify.plot(sizes=sizes, label=labels, color=colors, alpha=0.7)
patches = [plt.Rectangle((0,0),1,1, facecolor=c) for c in colors]
plt.legend(patches, legend_labels, loc='upper left', bbox_to_anchor=(1, 1), title='Legend')
plt.tight_layout() 
plt.title('Feature of Queries', fontsize=56)
plt.axis('off')  # 关闭坐标轴
plt.savefig("test.png")
