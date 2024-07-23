import os
import random
import osmnx as ox
import networkx as nx
from typing import List, Tuple
import folium

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

def solve_random_vrp(G: nx.MultiDiGraph, num_vehicles: int, depot: int) -> List[List[int]]:
    nodes = list(G.nodes)
    routes = []
    for _ in range(num_vehicles):
        route_length = random.randint(5, 10)
        route = [depot] + random.sample(nodes, route_length) + [depot]
        routes.append(route)
    return routes

def generate_graph_routes(G: nx.MultiDiGraph, routes: List[List[int]]) -> List[List[int]]:
    graph_routes = []
    for route in routes:
        graph_route = []
        for i in range(len(route) - 1):
            try:
                path = nx.astar_path(G, source=route[i], target=route[i + 1], weight='length')
                graph_route.extend(path)
            except nx.NetworkXNoPath:
                pass
        graph_routes.append(graph_route)
    return graph_routes

def save_route_map(G: nx.MultiDiGraph, route: List[int], depot: int, map_id: int, base_path: str):
    try:
        m = folium.Map(location=get_node_coords(G, depot, for_map=True), zoom_start=14, tiles='cartodbpositron')
        folium.Marker(location=get_node_coords(G, depot, for_map=True), popup="Início", icon=folium.Icon(color="green")).add_to(m)
        
        path_coords = [get_node_coords(G, node, for_map=True) for node in route]
        folium.PolyLine(path_coords, color="green", weight=2.5, opacity=0.8).add_to(m)
        
        map_path = os.path.join(base_path, f"map_{map_id}.html")
        m.save(map_path)
        return map_path
    except Exception as e:
        raise RuntimeError(f"Error saving route map: {e}")

def generate_and_save_maps(location_point: Tuple[float, float], num_vehicles: int, base_path: str) -> List[str]:
    try:
        G = get_graph(location_point)
        depot = random.choice(list(G.nodes))
        routes = solve_random_vrp(G, num_vehicles, depot)
        graph_routes = generate_graph_routes(G, routes)

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        map_paths = []
        for i, route in enumerate(graph_routes, start=1):
            map_path = save_route_map(G, route, depot, i, base_path)
            map_paths.append(map_path)

        return map_paths
    except Exception as e:
        raise RuntimeError(f"Error in map generation and saving process: {e}")

if __name__ == "__main__":
    location_point = (-16.6037, -49.2616)
    base_path = "static/maps"
    map_paths = generate_and_save_maps(location_point, num_vehicles=3, base_path=base_path)
    print("Generated maps:", map_paths)
