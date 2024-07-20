import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random

def get_graph_from_location(location_point, dist=2000, network_type='drive'):
    """Obter e converter o grafo a partir de uma localização."""
    G = ox.graph_from_point(location_point, dist=dist, network_type=network_type)
    return nx.convert_node_labels_to_integers(G)

def generate_random_routes(G, num_vehicles, depot, min_length=5, max_length=10):
    """Gerar rotas aleatórias para os veículos."""
    nodes = list(G.nodes)
    routes = []
    for _ in range(num_vehicles):
        route_length = random.randint(min_length, max_length)
        route = [depot] + random.sample(nodes, route_length) + [depot]
        routes.append(route)
    return routes

def calculate_routes_in_graph(G, routes):
    """Calcular as rotas no grafo usando o algoritmo de caminho mais curto."""
    graph_routes = []
    for route in routes:
        graph_route = []
        for i in range(len(route) - 1):
            try:
                path = nx.shortest_path(G, source=route[i], target=route[i + 1], weight='length')
                graph_route.extend(path)
            except nx.NetworkXNoPath:
                pass  # Ignora se não houver caminho
        graph_routes.append(graph_route)
    return graph_routes

def plot_routes(G, graph_routes, depot, waypoints):
    """Visualizar as rotas no grafo."""
    colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    fig, ax = ox.plot_graph(G, show=False, close=False, node_size=0)
    
    for route, color, points in zip(graph_routes, colors, waypoints):
        route_nodes = [get_node_coords(G, node) for node in route]
        x, y = zip(*route_nodes)
        ax.plot(x, y, color)
        point_coords = [get_node_coords(G, point) for point in points]
        px, py = zip(*point_coords)
        ax.scatter(px, py, c=color, s=50, zorder=5)
    
    # Destacar o ponto de origem em amarelo
    depot_coords = get_node_coords(G, depot)
    ax.scatter(*depot_coords, c='yellow', s=100, zorder=5)
    
    plt.show()

def get_node_coords(G, node):
    """Extrair coordenadas de um nó."""
    return G.nodes[node]['x'], G.nodes[node]['y']

def main():
    location_point = (-16.6037, -49.2616)  # Coordenadas aproximadas do Campus Samambaia da UFG
    G = get_graph_from_location(location_point)
    
    depot = random.choice(list(G.nodes))  # Seleciona um nó aleatório como ponto de origem
    random_routes = generate_random_routes(G, 3, depot)
    graph_routes = calculate_routes_in_graph(G, random_routes)

    if graph_routes:
        plot_routes(G, graph_routes, depot, random_routes)
    else:
        print("Nenhuma solução encontrada.")

if __name__ == "__main__":
    main()
