import os
import json
from bs4 import BeautifulSoup

def extract_info_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    info = {
        'services': [],
        'contact_details': [],
        'description': '',
        'social_media_links': []
    }

    # Extract services
    services_section = soup.find('section', id='services')
    if services_section:
        services = services_section.find_all('li')
        info['services'] = [service.get_text().strip() for service in services]

    # Extract contact details
    contact_section = soup.find('section', id='contact-details')
    if contact_section:
        contacts = contact_section.find_all('li')
        info['contact_details'] = [contact.get_text().strip() for contact in contacts]

    # Extract description
    description_section = soup.find('section', id='description')
    if description_section:
        info['description'] = description_section.get_text().strip()

    # Extract social media links
    social_media_section = soup.find('section', id='social-media')
    if social_media_section:
        social_media_links = social_media_section.find_all('a')
        info['social_media_links'] = [link['href'].strip() for link in social_media_links]

    return info

def extract_info_from_files(directory):
    all_info = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
                info = extract_info_from_html(html_content)
                all_info.append(info)

    return all_info

def main():
    directory = 'menu'
    info = extract_info_from_files(directory)
    print(json.dumps(info, indent=4))

if __name__ == '__main__':
    main()
