import os
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import patheffects

# Bar
fig, ax = plt.subplots()

fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

ax.bar(fruits, counts, label=bar_labels, color=bar_colors)

ax.set_ylabel('fruit supply')
ax.set_title('Fruit supply by kind and color')
ax.legend(title='Fruit color')

plt.show()


# Plot a straight diagonal line with ticked style path
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot([0, 1], [0, 1], label="Line",
        path_effects=[patheffects.withTickedStroke(spacing=7, angle=135)])

# Plot a curved line with ticked style path
nx = 101
x = np.linspace(0.0, 1.0, nx)
y = 0.3*np.sin(x*8) + 0.4
ax.plot(x, y, label="Curve", path_effects=[patheffects.withTickedStroke()])

ax.legend()
plt.show()


# Створення даних
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = x**2

# Створення графіка
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Графік 1: Лінійний графік
axs[0, 0].plot(x, y1, label='sin(x)', color='blue', linestyle='-', linewidth=2)
axs[0, 0].plot(x, y2, label='cos(x)', color='red', linestyle='--', linewidth=2)
axs[0, 0].set_title('Лінійний графік')
axs[0, 0].set_xlabel('x')
axs[0, 0].set_ylabel('y')
axs[0, 0].legend()
axs[0, 0].grid(True)

# Графік 2: Точковий графік
axs[0, 1].scatter(x, y3, label='x^2', color='green', marker='o', s=20)
axs[0, 1].set_title('Точковий графік')
axs[0, 1].set_xlabel('x')
axs[0, 1].set_ylabel('y')
axs[0, 1].legend()
axs[0, 1].grid(True)

# Графік 3: Стовпчикова діаграма
categories = ['A', 'B', 'C', 'D']
values = [25, 15, 30, 10]
axs[1, 0].bar(categories, values, color='orange')
axs[1, 0].set_title('Стовпчикова діаграма')
axs[1, 0].set_xlabel('Категорії')
axs[1, 0].set_ylabel('Значення')

# Графік 4: Кругова діаграма
labels = ['Python', 'Java', 'C++', 'JavaScript']
sizes = [40, 30, 15, 15]
axs[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
axs[1, 1].set_title('Кругова діаграма')

# Налаштування графіка
plt.tight_layout()

# Збереження графіка у файл
dir_path = os.path.dirname(os.path.realpath(__file__))
folder = os.path.join(dir_path, "output_dir")
os.makedirs(folder, exist_ok=True)
out_file_path = os.path.join(folder, "my_plot.png")
plt.savefig(out_file_path)

# Відображення графіка
plt.show()
