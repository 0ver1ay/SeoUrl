input_file = 'texts//input.txt'
output_file = 'texts//output.txt'
search_word = 'колодки'

remaining_lines = []

with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
    for line in infile:
        if search_word in line:
            outfile.write(line)
        else:
            remaining_lines.append(line)
            
with open(input_file, 'w', encoding='utf-8') as infile:
    infile.writelines(remaining_lines)

print(f"Строки, содержащие '{search_word}', вырезаны и сохранены в {output_file}")
