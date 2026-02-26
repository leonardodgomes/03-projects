import random
import pandas as pd
from faker import Faker

fake = Faker()

# Define Path
path = 'C:/Users/a070127/OneDrive - Ageas Portugal/00.LEONARDO/Work/PowerBi/SalesTeamProfile/data/'

# Generate people data
people_data = []
sellers_names = ['Amanda James', 'Derrick Russo', 'Kevin Walsh', 'Marie Freeman', 'Sarah Blair']
for i in range(1, 6):  # Generate 5 people/sellers
    birthday_date = pd.Timestamp(fake.date_of_birth(minimum_age=25, maximum_age=40))  # Convert to Timestamp object
    start_date = pd.Timestamp(fake.date_between(start_date='-5y', end_date='-1y'))  # Convert to Timestamp object

    people_data.append({
        'person_id': i,
        'person_name': sellers_names[i - 1],
        'birthday_date': birthday_date,
        'age': (pd.Timestamp('now') - birthday_date).days // 365,  # Calculate age based on the difference between current date and birthday
        'store_id': random.randint(1, 3),  # Randomly assign a store ID to each person/seller
        'start_date_at_store': start_date,
        'years_of_experience': (pd.Timestamp('now') - start_date).days // 365  # Calculate years of experience based on the difference between current date and start date
    })

people_df = pd.DataFrame(people_data)

# Generate store data
store_data = []
for i in range(1, 4):  # Generate 3 stores
    store_name = f'Cycle First {fake.first_name()}'
    location = fake.city()
    store_data.append({
        'store_id': i,
        'store_name': store_name,
        'location': location
    })

store_df = pd.DataFrame(store_data)

# Generate products data
products_data = [
    # Bicycles
    {'product_id': 1, 'product_name': 'Scott Spark Full 2023', 'category': 'Bicycles'},
    {'product_id': 2, 'product_name': 'Trek X-caliber 9', 'category': 'Bicycles'},
    {'product_id': 3, 'product_name': 'Specialized Evo', 'category': 'Bicycles'},
    # Parts
    {'product_id': 4, 'product_name': 'Chain', 'category': 'Parts'},
    {'product_id': 5, 'product_name': 'Derailleur', 'category': 'Parts'},
    {'product_id': 6, 'product_name': 'Tires', 'category': 'Parts'},
    # Clothes
    {'product_id': 7, 'product_name': 'Jersey', 'category': 'Clothes'},
    {'product_id': 8, 'product_name': 'Gloves', 'category': 'Clothes'},
    {'product_id': 9, 'product_name': 'Helmet', 'category': 'Clothes'}
]

products_df = pd.DataFrame(products_data)

# Generate sales data
sales_data = []
for i in range(1, 1001):  # Generate 1000 sales
    seller_id = random.randint(1, 5)  # Randomly assign a seller ID to each sale
    store_id = random.choice(people_df[people_df['person_id'] == seller_id]['store_id'].values)  # Get the store ID associated with the seller

    sale_date = fake.date_between(start_date='-2y', end_date='today')  # Random date within the past 2 years

    # Adjust sales frequency during summer and Christmas seasons
    if sale_date.month in [6, 7, 8]:  # Summer months
        quantity = random.randint(5, 15)  # Higher quantity during summer
    elif sale_date.month == 12:  # December (Christmas month)
        quantity = random.randint(10, 20)  # Higher quantity during Christmas
    else:
        quantity = random.randint(1, 10)  # Regular quantity

    # Adjust sales for one of the stores to sell more
    if store_id == 1:  # Store ID 1 sells more
        quantity *= random.uniform(1.2, 1.5)  # Increase quantity by 20-50%

    sales_data.append({
        'sale_id': i,
        'product_id': random.randint(1, 9),  # Random product ID from 1 to 9
        'store_id': store_id,  # Use the store ID associated with the seller
        'seller_id': seller_id,  # Add the seller ID to the sales table
        'sale_date': pd.Timestamp(sale_date),  # Convert to Timestamp object
        'quantity': round(quantity),  # Adjusted quantity based on season and store
        'revenue': round(random.uniform(10, 5000), 2)  # Random revenue between 10 and 5000 with two decimal places
    })

sales_df = pd.DataFrame(sales_data)


# Generate sales target data
sales_target_data = []
for i in range(1, 6):  # Generate sales targets for 5 sellers
    years_of_experience = people_df.loc[people_df['person_id'] == i, 'years_of_experience'].values[0]
    target_multiplier = 1 + (years_of_experience * 0.05)  # Increase target by 5% per year of experience

    for year in range(2022, 2024):  # Generate targets for 2022 and 2023
        for quarter in range(1, 5):  # Generate targets for each quarter
            target = round(random.uniform(5000, 15000) * target_multiplier, 2)  # Random target between 5000 and 15000, adjusted based on experience
            sales_target_data.append({
                'person_id': i,
                'year': year,
                'quarter': quarter,
                'target': target
            })

sales_target_df = pd.DataFrame(sales_target_data)


# Save the dataframes to CSV files
people_df.to_csv(path + 'people.csv', index=False)
store_df.to_csv(path + 'store.csv', index=False)
products_df.to_csv(path + 'products.csv', index=False)
sales_df.to_csv(path + 'sales.csv', index=False)
sales_target_df.to_csv(path + 'sales_target.csv', index=False)