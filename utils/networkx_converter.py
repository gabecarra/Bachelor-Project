"""
networkx_converter
Converts a JSON structured set of graphs, into an array of networkx
graphs
"""

import json

import networkx as nx


def __get_nodes(graph, nodes: dict, resolution: list, id_offset: int) -> int:
    """
    Parses a set of nodes from JSON and add the node features and id to 
    the given graph. If a resolution if given, applies a normalization
    to the (x,y) values
    :param graph: networkx graph
    :param dict nodes: dictionary of nodes
    :param list resolution: list of 2 elements [x,y] representing an
    image resolution
    :param int id_offset: the offset from witch to start counting the
    node ids, used in case multiple graphs are considered such as hands
    and pose, or hands and face
    :return: the updated id_offset
    """
    for node in nodes:
        x = node['x']
        y = node['y']
        if resolution:
            x /= resolution[0]
            y /= resolution[1]
        graph.add_node(id_offset + node['id'],
                       x=x,
                       y=y,
                       confidence=node['confidence'])
    return id_offset + nodes[-1]['id'] + 1


def __get_edges(graph, edges: dict):
    """
    Parses a set of edges from a JSON and add them on the given graph
    :param graph: networkx graph
    :param dict edges: set of edges represented as a dictionary
    """
    for edge in edges:
        for elem in edge['linked_nodes']:
            graph.add_edge(edge['ref_node'], elem)


def __get_graph(graph, person: dict, node_types: list, resolution: list):
    """
    Creates a graph representing a given person. The node_types informs
    on which type or types of node to include, such as face, hands or
    pose.
    :param graph: networkx graph
    :param dict person: a person represented as dictionary containing
    the nodes and edges for each part
    :param list node_types: list of node types. Can be one or more
    of ->['face', 'pose', 'handl', 'handr']
    :param list resolution: The resolution of the given image from witch
    the person points were taken from
    """
    id_offset = 0
    for node_type in node_types:
        # nodes
        orientation = 'right' if node_type == 'handr' else 'left'
        if node_type in ['handl', 'handr']:
            nodes = person['nodes']['hands'][orientation]
        elif node_type in ['pose', 'face']:
            nodes = person['nodes'][node_type]
        else:
            raise ValueError(node_type + ' is not supported!...')
        id_offset = __get_nodes(graph, nodes, resolution, id_offset)
        # edges
        if node_type in ['handl', 'handr']:
            edges = person['edges']['hands'][orientation]
        else:
            edges = person['edges'][node_type]
        __get_edges(graph, edges)


def get_nx_graphs(path: str, node_types: list, normalize: bool = False) -> list:
    """
    Given a file path name, and the types of graph nodes, returns a list
    of networkx graphs containing a graph for each person in the given
    file/image.
    :param bool normalize: if normalize is given, divides the (x,y)
    values from the graph by their resolution in order to normalize
    their values between 0 and 1
    :param str path: path name of a given file
    :param list node_types: list of node types. Can be one or more
    of ->['face', 'pose', 'handl', 'handr']
    :return list: list containing a graph for each person in the file
    """
    graph_list = []
    with open(path) as json_file:
        data = json.load(json_file)
        resolution = [int(x) for x in data['resolution'].split('x')] \
            if normalize else None
        for person in data['people']:
            graph = nx.Graph()
            __get_graph(graph, person, node_types, resolution)
            graph_list.append(graph)
    return graph_list
