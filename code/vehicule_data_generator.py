import random
import string
from faker import Faker

# Inicialize o Faker
fake = Faker()

# Função para gerar uma placa de veículo aleatória
def generate_plate():
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    numbers = ''.join(random.choices(string.digits, k=4))
    return f"{letters}-{numbers}"

# Função para gerar dados de veículos
def generate_vehicle_data(num_records):
    vehicle_data = []
    for _ in range(num_records):
        placa = generate_plate()
        max_speed = round(random.uniform(60, 180), 2)
        max_mass = round(random.uniform(1000, 30000), 2)
        max_space = round(random.uniform(2, 40), 2)
        autonomy = round(random.uniform(200, 1000), 2)
        km_liter = round(random.uniform(5, 20), 2)
        vehicle_type = random.randint(1, 5)  # Supondo que existem 5 tipos diferentes de veículos
        vehicle_data.append((placa, max_speed, max_mass, max_space, autonomy, km_liter, vehicle_type))
    return vehicle_data

# Gerar 10 registros de exemplo
vehicle_records = generate_vehicle_data(5*100)

# Exibir os registros gerados
for record in vehicle_records:
    print(record)

# Caso queira salvar em um arquivo CSV
import csv

with open('vehicle_data.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["placa", "max_speed", "max_mass", "max_space", "autonomy", "km_liter", "vehicle_type"])
    writer.writerows(vehicle_records)

print("Dados de veículos gerados e salvos em 'vehicle_data.csv'")
