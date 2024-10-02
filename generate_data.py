import pandas as pd
import random
from faker import Faker

# Initialize Faker
fake = Faker()

# Function to generate data with some missing values
def generate_data(num_rows):
    data = []
    vehicle_types = ['Car', 'Bike', 'Truck', 'Bus', 'Scooter', 'Van']
    region_types = ['Bellandur','Marathalli','JP Nagar','Silkboard','Koramangalla']
    
    for _ in range(num_rows):
        row = {
            'name': fake.name() if random.random() > 0.05 else None,
            'email': fake.email() if random.random() > 0.1 else None,
            'address': fake.address() if random.random() > 0.1 else None,
            'roll_no': random.randint(1, 10000) if random.random() > 0.05 else None,
            'phone_no': fake.phone_number() if random.random() > 0.1 else None,
            'age': random.randint(18, 80) if random.random() > 0.1 else None,
            'motor_vehicle_type': random.choice(vehicle_types) if random.random() > 0.2 else None,
            'region_type': random.choice(region_types) if random.random() > 0.2 else None
        }

        # Ensure at least one column is not None
        while all(value is None for value in row.values()):
            # Randomly select a column and fill with a valid value
            col_to_fill = random.choice(list(row.keys()))
            if col_to_fill == 'name':
                row['name'] = fake.name()
            elif col_to_fill == 'email':
                row['email'] = fake.email()
            elif col_to_fill == 'address':
                row['address'] = fake.address()
            elif col_to_fill == 'roll_no':
                row['roll_no'] = random.randint(1, 10000)
            elif col_to_fill == 'phone_no':
                row['phone_no'] = fake.phone_number()
            elif col_to_fill == 'age':
                row['age'] = random.randint(18, 80)
            elif col_to_fill == 'motor_vehicle_type':
                row['motor_vehicle_type'] = random.choice(vehicle_types)
            elif col_to_fill == 'region_type':
                row['region_type'] = random.choice(region_types)

        data.append(row.values())
    
    return data

# Generate the data
num_rows = 1000
columns = ['name', 'email', 'region_type','address', 'roll_no', 'phone_no', 'age', 'motor_vehicle_type']
data = generate_data(num_rows)

# Create a DataFrame
df = pd.DataFrame(data, columns=columns)

# Display the first few rows of the DataFrame
df.to_csv(r'/Users/nitish/Desktop/Code for Data/Familier/PII/data.csv')
