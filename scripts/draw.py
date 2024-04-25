import matplotlib.pyplot as plt
import numpy as np

# Data for MongoDB and Neo4j with and without memory for different accuracy types
mongodb_data = {
    'Without Memory': [71.42857143, 43.33333333, 44.21052632, 10],
    'With Memory': [79.46428571, 50, 54.73684211, 20]
}
neo4j_data = {
    'Without Memory': [93.75, 36.66666667, 49.47368421, 30],
    'With Memory': [83.92857143, 76.66666667, 57.89473684, 50]
}

# Labels for accuracy types and databases
accuracy_types = ['Simple Query Accuracy', 'Aggregation Accuracy', 'Join Query Accuracy', 'Join & Aggregation Accuracy']
databases = ['MongoDB', 'Neo4j']
colors = ['lightcoral', 'firebrick']  # Colors for bars

# Adjusting the font size to match the title's size
plt.rcParams.update({'font.size': 20})  # Increase font size for better visibility

bar_width = 0.35  # Width of the bars

# Creating a figure with 4 subplots (2x2 grid)
fig, axs = plt.subplots(2, 2, figsize=(8, 6), sharey='row')  # Share y-axis within rows

for i, ax in enumerate(axs.flatten()):
    # Positioning for MongoDB and Neo4j bars
    positions_mongo = np.array([0, bar_width])
    positions_neo = np.array([1, 1 + bar_width])

    # MongoDB bars
    ax.bar(positions_mongo[0], mongodb_data['Without Memory'][i], width=bar_width, color=colors[0], label='Pure Prompts')
    ax.bar(positions_mongo[1], mongodb_data['With Memory'][i], width=bar_width, color=colors[1], label='With RAG')

    # Neo4j bars
    ax.bar(positions_neo[0], neo4j_data['Without Memory'][i], width=bar_width, color=colors[0])
    ax.bar(positions_neo[1], neo4j_data['With Memory'][i], width=bar_width, color=colors[1])

    # Setting titles and labels
    ax.set_title(accuracy_types[i], fontsize=20)
    if i % 2 == 0:  # Only add y-label to the first column
        ax.set_ylabel('Accuracy (%)', fontsize=20)
    ax.set_xticks([0.175, 1.175])  # Centering the labels between the two bars
    ax.set_xticklabels(databases, fontsize=20)

    # Custom y-axis limits based on the subplot index
    if i < 2:
        ax.set_ylim(0, 100)
    else:
        ax.set_ylim(0, 80)

# Adjust the layout before adding the legend
plt.tight_layout(rect=[0, 0, 1, 0.9])  # Leave space at the top for the legend

# Adding a single legend for the whole figure outside the plot area
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1), ncol=2, fontsize=20)

# Display the plot
plt.show()
