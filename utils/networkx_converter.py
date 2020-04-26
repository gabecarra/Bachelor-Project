"""
networkx_converter
Converts a JSON structured set of graphs, into an array of networkx graphs
"""

import json

import networkx as nx


def get_nx_graph(path: str, node_type: str = 'pose'):
    """
    Given a file path name, and the type of graph nodes, returns a list of networkx graphs
    :param str path: path name of a given file
    :param str node_type: type of graph nodes wanted. Can be one of: 'pose', 'handl', 'handr', 'face'
    :return list or None: list containing a graph for each person in the file
    """
    out = []
    orientation = 'right' if node_type == 'handr' else 'left'
    with open(path) as json_file:
        data = json.load(json_file)
        for person in data['people']:
            graph = nx.Graph()
            if node_type in ['handl', 'handr']:
                nodes = person['nodes']['hands'][orientation]
            else:
                nodes = person['nodes'][node_type]
            for node in nodes:
                graph.add_node(node['id'], x=node['x'], y=node['y'], confidence=node['confidence'])
            if node_type in ['handl', 'handr']:
                edges = person['edges']['hands'][orientation]
            else:
                edges = person['edges'][node_type]
            for edge in edges:
                for elem in edge['linked_nodes']:
                    graph.add_edge(edge['ref_node'], elem)
            out.append(graph)
    return out
