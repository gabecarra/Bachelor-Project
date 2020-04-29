"""
Carraretto Gabriel H.
edges_ref
Contains all the OpenPose edge references for face, hands and pose
"""


def get_edges(node_type: str):
    """
    Given a node type (pose, face, hand), returns the given edge set
    :param str node_type: the type of nodes needed
    :return list or None: list of edges, otherwise None
    """
    if node_type == 'pose':
        edges_list = [
            {'ref_node': 0, 'linked_nodes': [1, 15, 16]},
            {'ref_node': 1, 'linked_nodes': [0, 2, 5, 8]},
            {'ref_node': 2, 'linked_nodes': [1, 3]},
            {'ref_node': 3, 'linked_nodes': [2, 4]},
            {'ref_node': 4, 'linked_nodes': [3]},
            {'ref_node': 5, 'linked_nodes': [1, 6]},
            {'ref_node': 6, 'linked_nodes': [5, 7]},
            {'ref_node': 7, 'linked_nodes': [6]},
            {'ref_node': 8, 'linked_nodes': [1, 9, 12]},
            {'ref_node': 9, 'linked_nodes': [8, 10]},
            {'ref_node': 10, 'linked_nodes': [9, 11]},
            {'ref_node': 11, 'linked_nodes': [10, 22, 24]},
            {'ref_node': 12, 'linked_nodes': [8, 13]},
            {'ref_node': 13, 'linked_nodes': [12, 14]},
            {'ref_node': 14, 'linked_nodes': [13, 19, 21]},
            {'ref_node': 15, 'linked_nodes': [0, 17]},
            {'ref_node': 16, 'linked_nodes': [0, 18]},
            {'ref_node': 17, 'linked_nodes': [15]},
            {'ref_node': 18, 'linked_nodes': [16]},
            {'ref_node': 19, 'linked_nodes': [14, 20]},
            {'ref_node': 20, 'linked_nodes': [19]},
            {'ref_node': 21, 'linked_nodes': [14]},
            {'ref_node': 22, 'linked_nodes': [23, 11]},
            {'ref_node': 23, 'linked_nodes': [22]},
            {'ref_node': 24, 'linked_nodes': [11]}
        ]
    elif node_type in ['handl', 'handr']:
        edges_list = [
            {'ref_node': 0, 'linked_nodes': [1, 5, 9, 13, 17]},
            {'ref_node': 1, 'linked_nodes': [0, 2]},
            {'ref_node': 2, 'linked_nodes': [1, 3]},
            {'ref_node': 3, 'linked_nodes': [2, 4]},
            {'ref_node': 4, 'linked_nodes': [3]},
            {'ref_node': 5, 'linked_nodes': [0, 6]},
            {'ref_node': 6, 'linked_nodes': [5, 7]},
            {'ref_node': 7, 'linked_nodes': [6, 8]},
            {'ref_node': 8, 'linked_nodes': [7]},
            {'ref_node': 9, 'linked_nodes': [0, 10]},
            {'ref_node': 10, 'linked_nodes': [9, 11]},
            {'ref_node': 11, 'linked_nodes': [10, 12]},
            {'ref_node': 12, 'linked_nodes': [11]},
            {'ref_node': 13, 'linked_nodes': [0, 14]},
            {'ref_node': 14, 'linked_nodes': [13, 15]},
            {'ref_node': 15, 'linked_nodes': [14, 16]},
            {'ref_node': 16, 'linked_nodes': [15]},
            {'ref_node': 17, 'linked_nodes': [0, 18]},
            {'ref_node': 18, 'linked_nodes': [17, 19]},
            {'ref_node': 19, 'linked_nodes': [18, 20]},
            {'ref_node': 20, 'linked_nodes': [19]}
        ]
    elif node_type == 'face':
        edges_list = [
            {'ref_node': 0, 'linked_nodes': [1]},
            {'ref_node': 1, 'linked_nodes': [0, 2]},
            {'ref_node': 2, 'linked_nodes': [1, 3]},
            {'ref_node': 3, 'linked_nodes': [2, 4]},
            {'ref_node': 4, 'linked_nodes': [3, 5]},
            {'ref_node': 5, 'linked_nodes': [4, 6]},
            {'ref_node': 6, 'linked_nodes': [5, 7]},
            {'ref_node': 7, 'linked_nodes': [6, 8]},
            {'ref_node': 8, 'linked_nodes': [7, 9]},
            {'ref_node': 9, 'linked_nodes': [8, 10]},
            {'ref_node': 10, 'linked_nodes': [9, 11]},
            {'ref_node': 11, 'linked_nodes': [10, 12]},
            {'ref_node': 12, 'linked_nodes': [11, 13]},
            {'ref_node': 13, 'linked_nodes': [12, 14]},
            {'ref_node': 14, 'linked_nodes': [13, 15]},
            {'ref_node': 15, 'linked_nodes': [14, 16]},
            {'ref_node': 16, 'linked_nodes': [15]},
            {'ref_node': 17, 'linked_nodes': [18]},
            {'ref_node': 18, 'linked_nodes': [17, 19]},
            {'ref_node': 19, 'linked_nodes': [18, 20]},
            {'ref_node': 20, 'linked_nodes': [19, 21]},
            {'ref_node': 21, 'linked_nodes': [20]},
            {'ref_node': 22, 'linked_nodes': [23]},
            {'ref_node': 23, 'linked_nodes': [22, 24]},
            {'ref_node': 24, 'linked_nodes': [23, 25]},
            {'ref_node': 25, 'linked_nodes': [24, 26]},
            {'ref_node': 26, 'linked_nodes': [25]},
            {'ref_node': 27, 'linked_nodes': [28]},
            {'ref_node': 28, 'linked_nodes': [27, 29]},
            {'ref_node': 29, 'linked_nodes': [28, 30]},
            {'ref_node': 30, 'linked_nodes': [29]},
            {'ref_node': 31, 'linked_nodes': [32]},
            {'ref_node': 32, 'linked_nodes': [31, 33]},
            {'ref_node': 33, 'linked_nodes': [32, 34]},
            {'ref_node': 34, 'linked_nodes': [33, 35]},
            {'ref_node': 35, 'linked_nodes': [34]},
            {'ref_node': 36, 'linked_nodes': [37, 41]},
            {'ref_node': 37, 'linked_nodes': [36, 38]},
            {'ref_node': 38, 'linked_nodes': [37, 39]},
            {'ref_node': 39, 'linked_nodes': [38, 40]},
            {'ref_node': 40, 'linked_nodes': [39, 41]},
            {'ref_node': 41, 'linked_nodes': [36, 40]},
            {'ref_node': 42, 'linked_nodes': [43, 47]},
            {'ref_node': 43, 'linked_nodes': [42, 44]},
            {'ref_node': 44, 'linked_nodes': [43, 45]},
            {'ref_node': 45, 'linked_nodes': [44, 46]},
            {'ref_node': 46, 'linked_nodes': [45, 47]},
            {'ref_node': 47, 'linked_nodes': [42, 46]},
            {'ref_node': 48, 'linked_nodes': [49, 59]},
            {'ref_node': 49, 'linked_nodes': [48, 50]},
            {'ref_node': 50, 'linked_nodes': [49, 51]},
            {'ref_node': 51, 'linked_nodes': [50, 52]},
            {'ref_node': 52, 'linked_nodes': [51, 53]},
            {'ref_node': 53, 'linked_nodes': [52, 54]},
            {'ref_node': 54, 'linked_nodes': [53, 55]},
            {'ref_node': 55, 'linked_nodes': [54, 56]},
            {'ref_node': 56, 'linked_nodes': [55, 57]},
            {'ref_node': 57, 'linked_nodes': [56, 58]},
            {'ref_node': 58, 'linked_nodes': [57, 59]},
            {'ref_node': 59, 'linked_nodes': [48, 58]},
            {'ref_node': 60, 'linked_nodes': [61, 67]},
            {'ref_node': 61, 'linked_nodes': [60, 62]},
            {'ref_node': 62, 'linked_nodes': [61, 63]},
            {'ref_node': 63, 'linked_nodes': [62, 64]},
            {'ref_node': 64, 'linked_nodes': [63, 65]},
            {'ref_node': 65, 'linked_nodes': [64, 66]},
            {'ref_node': 66, 'linked_nodes': [65, 67]},
            {'ref_node': 67, 'linked_nodes': [60, 66]},
            {'ref_node': 68, 'linked_nodes': []},
            {'ref_node': 69, 'linked_nodes': []}
        ]
    else:
        return None
    return edges_list
