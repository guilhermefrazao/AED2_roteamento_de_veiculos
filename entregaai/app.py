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
    clientes_entregues = []
    valor_final_j = 0
    

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
            produtos_entregues.append(clientes[valor_final_j][-1])     

            update = update_query(f"UPDATE products_data SET status = 'Entregue' WHERE product_name = '{produtos_entregues[valor_final_j]}'")
            consulta1 = execute_query(f"SELECT product_name, quantity, price, status FROM products_data WHERE product_name = '{produtos_entregues[valor_final_j]}'")
            consulta2 = execute_query(f"SELECT name FROM clients_data WHERE produto_comprado = '{produtos_entregues[valor_final_j]}' LIMIT 1;")
            print("consulta2",consulta2)
            
            clientes_entregues.append(consulta2 + consulta1)

            retorna = update_query(f"UPDATE products_data SET status = 'Não entregue' WHERE status = 'Entregue'")
            folium.Marker(location=get_node_coords(G, node, for_map=True), icon=folium.Icon(color=color), popup=f'{j} Ponto').add_to(m)
            valor_final_j = valor_final_j + 1
        maps.append(m)

    
    # Mapa combinado com todas as rotas
    combined_map = create_combined_map(G, graph_routes, points_of_interest_all_routes, depot)
    maps.append(combined_map)
    
    # Armazenar os mapas na sessão
    st.session_state['maps'] = maps
    print("estado da seção:",st.session_state)
    st.session_state['banco_de_dados'] = pd.DataFrame(clientes_entregues)

# Carrossel de Mapas
if 'maps' in st.session_state and st.session_state['maps']:
    maps = st.session_state['maps']
    current_map = st.selectbox("Selecionar Mapa", range(len(maps)))
    map_html = maps[current_map]._repr_html_()
    html(map_html, height=600)

#Visualização do banco de dados
if 'banco_de_dados' in st.session_state and not st.session_state['banco_de_dados'].empty:
    banco_de_dados = st.session_state['banco_de_dados']
    print(banco_de_dados.dtypes)
    banco_de_dados = banco_de_dados.astype(str)

    print("Banco de dados na seção:",banco_de_dados)
    st.write("Banco de dados das entregas realizadas:")

    st.dataframe(banco_de_dados,width=1000, height=500)
