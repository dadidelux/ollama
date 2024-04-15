import os
import textwrap
from bs4 import BeautifulSoup

def extract_text_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        return soup.get_text(separator=' ', strip=True)

def combine_texts_from_folder(folder_path):
    combined_text = set()
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.html'):
            file_path = os.path.join(folder_path, file_name)
            text = extract_text_from_html(file_path)
            combined_text.update(text.split())
    return ' '.join(combined_text)

def save_combined_text(combined_text, output_folder, file_name='combined_document.txt', width=80):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_path = os.path.join(output_folder, file_name)
    wrapped_text = textwrap.fill(combined_text, width=width)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(wrapped_text)
    print(f'Combined text saved to {output_path}')

# Example usage
folder_path = 'menu/menu'
combined_text = combine_texts_from_folder(folder_path)

output_folder = 'combined'
save_combined_text(combined_text, output_folder, width=80)

