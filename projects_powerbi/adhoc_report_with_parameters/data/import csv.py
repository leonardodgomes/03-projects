import os
import csv
from faker import Faker
import random

fake = Faker()

def generate_clients_dataset(num_companies, num_clients_per_company):
    dataset = []
    companies = []

    for _ in range(num_companies):
        company_name = fake.company()
        companies.append(company_name)

        for _ in range(num_clients_per_company):
            client = {
                'company': company_name,
                'name': fake.name(),
                'email': fake.email(),
                'phone': fake.phone_number(),
                'address': fake.address().replace('\n', ', '),
                'job_title': fake.job(),
                'age': random.randint(18, 65),
                'credit_card_number': fake.credit_card_number(),
                'credit_card_provider': fake.credit_card_provider(),
                'credit_card_expires': fake.credit_card_expire(),
                'username': fake.user_name(),
                'password': fake.password(),
            }

            dataset.append(client)

    return dataset, companies

# Generate a dataset with 20 companies and 200 clients (10 clients per company)
clients_dataset, company_list = generate_clients_dataset(20, 10)

# Get the path of the Python file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Save the dataset to a CSV file in the same directory
filename = os.path.join(script_dir, 'clients_dataset.csv')
fieldnames = clients_dataset[0].keys()

with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(clients_dataset)

print(f'Dataset saved to {filename} successfully.')
print(f'Companies: {", ".join(company_list)}')
