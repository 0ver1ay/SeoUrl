import os
import pandas as pd

# Шаг 1: Считываем ключевые слова из файла
input_file = ''
with open(input_file, 'r', encoding='utf-8') as f:
    keywords = [line.strip() for line in f.readlines()]

# Пример ключевых слов для фильтрации по группам
group_keywords = {
    'перед': ['перед', 'передняя', 'передней'],
    'зад': ['зад', 'задняя', 'задней'],
}

# Шаг 2: Функция для назначения кластера на основе ключевых слов
def assign_cluster(keyword):
    for group, words in group_keywords.items():
        if any(word in keyword for word in words):
            return group
    return None  # Возвращаем None, если не подходит ни один кластер

# Шаг 3: Создаем DataFrame с ключевыми словами
clusters = pd.DataFrame({'keyword': keywords})
clusters['cluster'] = clusters['keyword'].apply(assign_cluster)

# Шаг 4: Определяем выходную директорию
output_folder = os.path.join(os.path.dirname(input_file), 'clustered_output')
os.makedirs(output_folder, exist_ok=True)

# Шаг 5: Сохраняем каждую группу в отдельный файл
for cluster_name, group in clusters.groupby('cluster'):
    if cluster_name:  # Пропускаем None (оставшиеся слова)
        output_file = os.path.join(output_folder, f"{cluster_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(group['keyword']))

# Шаг 6: Сохраняем оставшиеся слова в файл remainder.txt
remainder = clusters[clusters['cluster'].isna()]['keyword']
remainder_file = os.path.join(output_folder, 'remainder.txt')
with open(remainder_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(remainder))

print(f"Результаты кластеризации сохранены в папке {output_folder}, оставшиеся слова — в remainder.txt")
