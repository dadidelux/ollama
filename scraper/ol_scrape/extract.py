import re
import json

def extract_information(combined_text):
    company_services_match = re.findall(r"\"company_services\": \[(.*?)\],", combined_text, re.DOTALL)
    if company_services_match:
        company_services = company_services_match[0].split(',')
    else:
        company_services = []
    company_services = re.findall(r"\"company_services\": \[(.*?)\],", combined_text, re.DOTALL)[0].split(',')
    company_services = [service.strip().strip('"') for service in company_services]
    phone_numbers = re.findall(r"\"phone_numbers\": {(.*?)},", combined_text, re.DOTALL)[0].split(',')
    phone_numbers = {re.search(r"\"(.*?)\":", num).group(1): re.search(r"\"(.*?)\"$", num).group(1) for num in phone_numbers}
    email_addresses = re.findall(r"\"email_addresses\": {(.*?)},", combined_text, re.DOTALL)[0].split(',')
    email_addresses = {re.search(r"\"(.*?)\":", email).group(1): re.search(r"\"(.*?)\"$", email).group(1) for email in email_addresses}
    office_locations = re.findall(r"\"office_locations\": \[(.*?)\],", combined_text, re.DOTALL)[0].split(',')
    office_locations = [location.strip().strip('"') for location in office_locations]
    website = re.search(r"\"website\": \"(.*?)\",", combined_text).group(1)
    social_media_links = re.findall(r"\"social_media_links\": {(.*?)},", combined_text, re.DOTALL)[0].split(',')
    social_media_links = {re.search(r"\"(.*?)\":", link).group(1): re.search(r"\"(.*?)\"$", link).group(1) for link in social_media_links}
    company_history = re.search(r"\"company_history\": \"(.*?)\",", combined_text, re.DOTALL).group(1)
    job_openings = re.findall(r"\"job_openings\": \[(.*?)\],", combined_text, re.DOTALL)[0].split(',')
    job_openings = [job.strip().strip('"') for job in job_openings]
    employee_size = re.search(r"\"employee_size\": \"(.*?)\",", combined_text).group(1)
    key_people = re.findall(r"\"key_people\": \[(.*?)\]", combined_text, re.DOTALL)[0].split('},')
    key_people = [{"name": re.search(r"\"name\": \"(.*?)\",", person).group(1), "title": re.search(r"\"title\": \"(.*?)\"$", person).group(1)} for person in key_people if person]

    company_info = {
        "company_name": company_name,
        "company_services": company_services,
        "company_contact_details": {
            "phone_numbers": phone_numbers,
            "email_addresses": email_addresses,
            "office_locations": office_locations,
            "website": website,
            "social_media_links": social_media_links
        },
        "company_history": company_history,
        "job_openings": job_openings,
        "employee_size": employee_size,
        "key_people": key_people
    }

    return company_info

# Read the combined text file
with open('combined/combined_document.txt', 'r') as file:
    combined_text = file.read()

# Extract information
company_info = extract_information(combined_text)

# Save the information as a JSON file using the company name
json_filename = f'extracted_output/{company_info["company_name"].replace(" ", "_").lower()}_info.json'
with open(json_filename, 'w') as json_file:
    json.dump(company_info, json_file, indent=4)

