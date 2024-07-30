import osmnx as ox
import pandas as pd
import random
import uuid
from faker import Faker

# Coordenadas do Campus Samambaia da UFG
campus_coords = (-16.603422, -49.265381)  # Latitude e longitude aproximadas

# Definir o raio em metros
radius = 4000  # 4 km

# Coletar o grafo de ruas dentro do raio especificado
G = ox.graph_from_point(campus_coords, dist=radius, network_type='drive')

# Extrair nós
nodes, _ = ox.graph_to_gdfs(G)

# Inicializar o Faker para gerar dados fictícios
fake = Faker()

# Função para gerar dados de clientes fictícios
def generate_fake_clients(nodes, num_clients):
    client_data = []
    node_ids = nodes.index.to_list()  # Lista de IDs dos nós
    for _ in range(num_clients):
        node = nodes.loc[random.choice(node_ids)]
        client_uuid = str(uuid.uuid4())
        client_name = fake.name()
        client_phone = fake.phone_number()
        client_data.append({
            "uuid": client_uuid,
            "name": client_name,
            "phone": client_phone,
            "x": node['x'],
            "y": node['y']
        })
    return client_data

# Número de clientes fictícios que deseja gerar
num_clients = 1000  # Gerar 1000 clientes fictícios

# Gerar dados de clientes
clients = generate_fake_clients(nodes, num_clients)

# Criar um DataFrame a partir dos dados dos clientes
clients_df = pd.DataFrame(clients)

# Salvar os dados em um arquivo CSV
clients_df.to_csv('clients_data.csv', index=False)

print("Dados de clientes fictícios salvos em 'clients_data.csv'.")

# Exibir os primeiros registros do DataFrame
print(clients_df.head())
