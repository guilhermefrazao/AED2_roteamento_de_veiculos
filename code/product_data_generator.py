import pandas as pd
import uuid
from faker import Faker
import random

# Inicializar o Faker para gerar dados fictícios
fake = Faker()

# Função para gerar dados de produtos fictícios
def generate_fake_products(num_products):
    product_data = []
    for i in range(1, num_products + 1):
        product_uuid = str(uuid.uuid4())
        product_name = f"product_{i}"
        quantity = random.randint(1, 100)
        price = round(random.uniform(10.0, 1000.0), 2)
        product_data.append({
            "UUID_produto": product_uuid,
            "product_name": product_name,
            "quantity": quantity,
            "price": price
        })
    return product_data

# Número de produtos fictícios que deseja gerar
num_products = 1000  # Gerar 1000 produtos fictícios

# Gerar dados de produtos
products = generate_fake_products(num_products)

# Criar um DataFrame a partir dos dados dos produtos
products_df = pd.DataFrame(products)

# Salvar os dados em um arquivo CSV
products_df.to_csv('products_data.csv', index=False)

print("Dados de produtos fictícios salvos em 'fake_products.csv'.")

# Exibir os primeiros registros do DataFrame
print(products_df.head())
