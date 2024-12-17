
input_file_path = 'cleaned_urls.txt'


output_file_path = 'corrected_urls.txt'


with open(input_file_path, 'r') as file:
    urls = file.readlines()


base_url = "https://renokom.ru"
corrected_urls = [base_url + url.strip() if not url.startswith(base_url) else url.strip() for url in urls]


with open(output_file_path, 'w') as file:
    for url in corrected_urls:
        file.write(url + '\n')

print(f"URL были сохранены в '{output_file_path}'")
