import os
import random
import osmnx as ox
import networkx as nx
from typing import List, Tuple
import folium
import matplotlib.colors as mcolors

def get_graph(location_point: Tuple[float, float], radius: int = 4000) -> nx.MultiDiGraph:
    try:
        G = ox.graph_from_point(location_point, dist=radius, network_type='drive')
        G = nx.convert_node_labels_to_integers(G)
        return G
    except Exception as e:
        raise RuntimeError(f"Error obtaining graph: {e}")

def get_node_coords(G: nx.MultiDiGraph, node: int, for_map: bool = False) -> Tuple[float, float]:
    try:
        if for_map:
            return G.nodes[node]['y'], G.nodes[node]['x']
        return G.nodes[node]['x'], G.nodes[node]['y']
    except KeyError:
        raise ValueError(f"Node {node} not found in graph")

def solve_random_vrp(G: nx.MultiDiGraph, num_vehicles: int, depot: int, num_points: int) -> Tuple[List[List[int]], List[List[int]]]:
    nodes = list(G.nodes)
    routes = []
    points_of_interest_all_routes = []
    for _ in range(num_vehicles):
        points_of_interest = random.sample(nodes, num_points)
        route = [depot] + points_of_interest + [depot]
        routes.append(route)
        points_of_interest_all_routes.append(points_of_interest)
    return routes, points_of_interest_all_routes

def generate_graph_routes(G: nx.MultiDiGraph, routes: List[List[int]]) -> List[List[int]]:
    graph_routes = []
    for route in routes:
        graph_route = []
        for i in range(len(route) - 1):
            try:
                path = nx.astar_path(G, source=route[i], target=route[i + 1], weight='length')
                graph_route.extend(path if not graph_route else path[1:])
            except nx.NetworkXNoPath:
                pass
        graph_routes.append(graph_route)
    return graph_routes

def get_colors(num_colors: int) -> List[str]:
    colors = list(mcolors.CSS4_COLORS.keys())
    random.shuffle(colors)
    return colors[:num_colors]

def create_combined_map(G: nx.MultiDiGraph, graph_routes: List[List[int]], points_of_interest_all_routes: List[List[int]], depot: int) -> folium.Map:
    m = folium.Map(location=get_node_coords(G, depot, for_map=True), zoom_start=14, tiles='cartodbpositron')
    folium.Marker(location=get_node_coords(G, depot, for_map=True), popup="Início", icon=folium.Icon(color="green")).add_to(m)
    
    colors = get_colors(len(graph_routes))
    valid_colors = {'darkgreen', 'blue', 'green', 'pink', 'purple', 'lightblue', 'beige', 'darkblue', 'orange', 'darkpurple', 'gray', 'black', 'cadetblue', 'darkred', 'lightred', 'red', 'lightgreen'}
    
    for route, points_of_interest, color in zip(graph_routes, points_of_interest_all_routes, colors):
        if color not in valid_colors:
            color = random.choice(list(valid_colors))
        path_coords = [get_node_coords(G, node, for_map=True) for node in route]
        folium.PolyLine(path_coords, color=color, weight=2.5, opacity=0.8).add_to(m)
        # Adicionar marcadores para os pontos de interesse no mapa
        for node in points_of_interest:
            folium.Marker(location=get_node_coords(G, node, for_map=True), icon=folium.Icon(color=color)).add_to(m)
        
    return m
