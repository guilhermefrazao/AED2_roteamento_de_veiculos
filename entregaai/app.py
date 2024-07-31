import streamlit as st
import folium
from streamlit.components.v1 import html
from route_generator import *
from banco_de_dados import *
import random
import psycopg2
import pandas as pd



# Título e Imagem do Projeto
st.title("EntregaAI")
# st.image("static/images/logo.png") # Descomente e ajuste o caminho se tiver uma imagem para exibir

# Formulário para Parâmetros do Algoritmo
st.sidebar.header("Configuração do Algoritmo")
latitude = st.sidebar.number_input("Latitude", value=-16.6037)
longitude = st.sidebar.number_input("Longitude", value=-49.2616)
num_vehicles = st.sidebar.number_input("Número de Veículos", min_value=1, max_value=10, value=3)
num_points = st.sidebar.number_input("Número de Pontos", min_value=1, max_value=20, value=5)

if st.sidebar.button("Executar"):
    clientes = execute_query(f"SELECT * FROM clients_data ORDER BY RANDOM() LIMIT {num_points*num_vehicles}")
    print("clientes", clientes)
    produtos_entregues = []
    

    location_point = (latitude, longitude)
    G = get_graph(location_point)
    depot = random.choice(list(G.nodes))
    routes, points_of_interest_all_routes = solve_random_vrp(G, num_vehicles, depot, num_points)
    graph_routes = generate_graph_routes(G, routes)
    
    maps = []
    colors = get_colors(num_vehicles)
    valid_colors = {'darkgreen', 'blue', 'green', 'pink', 'lightgray', 'purple', 'lightblue', 'beige', 'darkblue', 'orange', 'darkpurple', 'gray', 'black', 'cadetblue', 'darkred', 'lightred', 'red', 'lightgreen'}

    for i, (route, points_of_interest, color) in enumerate(zip(graph_routes, points_of_interest_all_routes, colors), start=1):
        if color not in valid_colors:
            color = random.choice(list(valid_colors))
        m = folium.Map(location=get_node_coords(G, depot, for_map=True), zoom_start=14, tiles='cartodbpositron')
        folium.Marker(location=get_node_coords(G, depot, for_map=True), popup="Início", icon=folium.Icon(color="green")).add_to(m)
        path_coords = [get_node_coords(G, node, for_map=True) for node in route]
        folium.PolyLine(path_coords, color=color, weight=2.5, opacity=0.8).add_to(m)
        
        # Adicionar marcadores para os pontos de interesse no mapa
        for j, node in enumerate(points_of_interest, start=1):
            produtos_entregues.append(clientes[(j*i)-1][-1]) 
            print("produtos_entregues", produtos_entregues)
            update = execute_query(f"UPDATE products_data SET status = 'Entregue' WHERE product_name = '{produtos_entregues[(j*i)-1]}'")
            consulta = execute_query(f"SELECT * FROM products_data WHERE product_name = '{produtos_entregues[(j*i)-1]}'")
            print("consulta", consulta)
            retorna = execute_query(f"UPDATE products_data SET status = 'Entregue' WHERE status = 'Não entregue'")
            print("retornando banco de dados",retorna)
            folium.Marker(location=get_node_coords(G, node, for_map=True), icon=folium.Icon(color=color), popup=f'{j} Ponto').add_to(m)
        
        maps.append(m)

    
    # Mapa combinado com todas as rotas
    combined_map = create_combined_map(G, graph_routes, points_of_interest_all_routes, depot)
    maps.append(combined_map)
    
    # Armazenar os mapas na sessão
    st.session_state['maps'] = maps

# Carrossel de Mapas
if 'maps' in st.session_state and st.session_state['maps']:
    maps = st.session_state['maps']
    current_map = st.selectbox("Selecionar Mapa", range(len(maps)))
    map_html = maps[current_map]._repr_html_()
    html(map_html, height=600)
