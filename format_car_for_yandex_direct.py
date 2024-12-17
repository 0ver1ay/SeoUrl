# Определите исходный и целевой файлы
input_file = 'texts//input.txt'
output_file = 'texts//output.txt'
search_word = 'колодки'  # Замените на нужное слово или часть слова

# Создадим список для строк, которые нужно оставить в исходном файле
remaining_lines = []

# Откроем исходный файл для чтения и целевой файл для записи
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        # Если строка содержит искомое слово, вырезаем (записываем в другой файл)
        if search_word in line:
            outfile.write(line)
        else:
            # Если строка не содержит слово, сохраняем её для записи обратно в исходный файл
            remaining_lines.append(line)

# Перезаписываем исходный файл, оставив только строки без искомого слова
with open(input_file, 'w', encoding='utf-8') as infile:
    infile.writelines(remaining_lines)

print(f"Строки, содержащие '{search_word}', вырезаны и сохранены в {output_file}")
