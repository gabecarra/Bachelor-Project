"""
@author Carraretto Gabriel H.
@license MIT
Converts a JSON structured set of graphs, into an array of networkx
graphs
"""

import json

import networkx as nx


def __get_nodes(graph, nodes, resolution, id_offset):
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


def __get_edges(graph, edges):
    """
    Parses a set of edges from a JSON and add them on the given graph
    :param graph: networkx graph
    :param dict edges: set of edges represented as a dictionary
    """
    for edge in edges:
        for elem in edge['linked_nodes']:
            graph.add_edge(edge['ref_node'], elem)


def __get_graph(graph, person, node_types, resolution):
    """
    Creates a graph representing a given person. The node_types informs
    on which type or types of node to include, such as face, hands or
    pose.
    :param graph: networkx graph
    :param dict person: a person represented as dictionary containing
    the nodes and edges for each part
    :param dict node_types: list of node types. Can be one or more
    of ->['face', 'pose', 'handl', 'handr']
    :param list resolution: The resolution of the given image from witch
    the person points were taken from
    """
    id_offset = 0
    if node_types['pose']:
        pose_nodes = person['nodes']['pose']
        pose_edges = person['edges']['pose']
        id_offset = __get_nodes(graph, pose_nodes, resolution, id_offset)
        __get_edges(graph, pose_edges)
    if node_types['hand']:
        l_nodes = person['nodes']['hands']['left']
        l_edges = person['edges']['hands']['left']
        if len(l_nodes) != 0:
            id_offset = __get_nodes(graph, l_nodes, resolution, id_offset)
            __get_edges(graph, l_edges)
        r_nodes = person['nodes']['hands']['right']
        r_edges = person['edges']['hands']['right']
        if len(r_nodes) != 0:
            id_offset = __get_nodes(graph, r_nodes, resolution, id_offset)
            __get_edges(graph, r_edges)
    if node_types['face']:
        face_nodes = person['nodes']['face']
        face_edges = person['edges']['face']
        __get_nodes(graph, face_nodes, resolution, id_offset)
        __get_edges(graph, face_edges)


def get_nx_graphs(data, node_types, normalize=False):
    """
    Given dictionary, and the types of nodes the dictionary contains,
    returns a list of networkx graphs containing a graph for each person
    in the given data.
    :param dict data: dictionary of keypoints
    :param dict node_types: dict of flags representing the node types.
    :param bool normalize: if normalize is given, divides the (x,y)
    values from the graph by their resolution in order to normalize
    their values between 0 and 1
    :return list: list containing a graph for each person in the file
    """
    graph_list = []
    resolution = [int(x) for x in data['resolution']] \
        if normalize else None
    for person in data['people']:
        graph = nx.Graph()
        __get_graph(graph, person, node_types, resolution)
        graph_list.append(graph)
    return graph_list
