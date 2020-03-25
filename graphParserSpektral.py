import json
import sys
import os

root_path = sys.argv[1] + '/'
out_path = root_path + '/out/'


# Given a list of nodes to be deleted, return a list of edges without the given nodes and their respective edges.
# Depending on the given type of the nodes, a different set of edges will be used(pose, hand and face)
def get_pose_edges(del_nodes, node_type='pose') -> list or None:
    edges_list = []
    if node_type == 'pose':
        edges_list = [{"ref_node": 0, 'linked_nodes': [1, 15, 16]},
                      {"ref_node": 1, 'linked_nodes': [0, 2, 5, 8]},
                      {"ref_node": 2, 'linked_nodes': [1, 3]},
                      {"ref_node": 3, 'linked_nodes': [2, 4]},
                      {"ref_node": 4, 'linked_nodes': [3]},
                      {"ref_node": 5, 'linked_nodes': [1, 6]},
                      {"ref_node": 6, 'linked_nodes': [5, 7]},
                      {"ref_node": 7, 'linked_nodes': [6]},
                      {"ref_node": 8, 'linked_nodes': [1, 9, 12]},
                      {"ref_node": 9, 'linked_nodes': [8, 10]},
                      {"ref_node": 10, 'linked_nodes': [9, 11]},
                      {"ref_node": 11, 'linked_nodes': [10, 22, 24]},
                      {"ref_node": 12, 'linked_nodes': [8, 13]},
                      {"ref_node": 13, 'linked_nodes': [12, 14]},
                      {"ref_node": 14, 'linked_nodes': [13, 19, 21]},
                      {"ref_node": 15, 'linked_nodes': [0, 17]},
                      {"ref_node": 16, 'linked_nodes': [0, 18]},
                      {"ref_node": 17, 'linked_nodes': [15]},
                      {"ref_node": 18, 'linked_nodes': [16]},
                      {"ref_node": 19, 'linked_nodes': [14, 20]},
                      {"ref_node": 20, 'linked_nodes': [19]},
                      {"ref_node": 21, 'linked_nodes': [14]},
                      {"ref_node": 22, 'linked_nodes': [23, 11]},
                      {"ref_node": 23, 'linked_nodes': [22]},
                      {"ref_node": 24, 'linked_nodes': [11]}]
    elif node_type == 'hand':
        edges_list = [{"ref_node": 0, 'linked_nodes': [1, 5, 9, 13, 17]},
                      {"ref_node": 1, 'linked_nodes': [0, 2]},
                      {"ref_node": 2, 'linked_nodes': [1, 3]},
                      {"ref_node": 3, 'linked_nodes': [2, 4]},
                      {"ref_node": 4, 'linked_nodes': [3]},
                      {"ref_node": 5, 'linked_nodes': [0, 6]},
                      {"ref_node": 6, 'linked_nodes': [5, 7]},
                      {"ref_node": 7, 'linked_nodes': [6, 8]},
                      {"ref_node": 8, 'linked_nodes': [7]},
                      {"ref_node": 9, 'linked_nodes': [0, 10]},
                      {"ref_node": 10, 'linked_nodes': [9, 11]},
                      {"ref_node": 11, 'linked_nodes': [10, 12]},
                      {"ref_node": 12, 'linked_nodes': [11]},
                      {"ref_node": 13, 'linked_nodes': [0, 14]},
                      {"ref_node": 14, 'linked_nodes': [13, 15]},
                      {"ref_node": 15, 'linked_nodes': [14, 16]},
                      {"ref_node": 16, 'linked_nodes': [15]},
                      {"ref_node": 17, 'linked_nodes': [0, 18]},
                      {"ref_node": 18, 'linked_nodes': [17, 19]},
                      {"ref_node": 19, 'linked_nodes': [18, 20]},
                      {"ref_node": 20, 'linked_nodes': [19]}]
    elif node_type == 'face':
        edges_list = [{"ref_node": 0, 'linked_nodes': [1]},
                      {"ref_node": 1, 'linked_nodes': [0, 2]},
                      {"ref_node": 2, 'linked_nodes': [1, 3]},
                      {"ref_node": 3, 'linked_nodes': [2, 4]},
                      {"ref_node": 4, 'linked_nodes': [3, 5]},
                      {"ref_node": 5, 'linked_nodes': [4, 6]},
                      {"ref_node": 6, 'linked_nodes': [5, 7]},
                      {"ref_node": 7, 'linked_nodes': [6, 8]},
                      {"ref_node": 8, 'linked_nodes': [7, 9]},
                      {"ref_node": 9, 'linked_nodes': [8, 10]},
                      {"ref_node": 10, 'linked_nodes': [9, 11]},
                      {"ref_node": 11, 'linked_nodes': [10, 12]},
                      {"ref_node": 12, 'linked_nodes': [11, 13]},
                      {"ref_node": 13, 'linked_nodes': [12, 14]},
                      {"ref_node": 14, 'linked_nodes': [13, 15]},
                      {"ref_node": 15, 'linked_nodes': [14, 16]},
                      {"ref_node": 16, 'linked_nodes': [15]},
                      {"ref_node": 17, 'linked_nodes': [18]},
                      {"ref_node": 18, 'linked_nodes': [17, 19]},
                      {"ref_node": 19, 'linked_nodes': [18, 20]},
                      {"ref_node": 20, 'linked_nodes': [19, 21]},
                      {"ref_node": 21, 'linked_nodes': [20]},
                      {"ref_node": 22, 'linked_nodes': [23]},
                      {"ref_node": 23, 'linked_nodes': [22, 24]},
                      {"ref_node": 24, 'linked_nodes': [23, 25]},
                      {"ref_node": 25, 'linked_nodes': [24, 26]},
                      {"ref_node": 26, 'linked_nodes': [25]},
                      {"ref_node": 27, 'linked_nodes': [28]},
                      {"ref_node": 28, 'linked_nodes': [27, 29]},
                      {"ref_node": 29, 'linked_nodes': [28, 30]},
                      {"ref_node": 30, 'linked_nodes': [29]},
                      {"ref_node": 31, 'linked_nodes': [32]},
                      {"ref_node": 32, 'linked_nodes': [31, 33]},
                      {"ref_node": 33, 'linked_nodes': [32, 34]},
                      {"ref_node": 34, 'linked_nodes': [33, 35]},
                      {"ref_node": 35, 'linked_nodes': [34]},
                      {"ref_node": 36, 'linked_nodes': [37, 41]},
                      {"ref_node": 37, 'linked_nodes': [36, 38]},
                      {"ref_node": 38, 'linked_nodes': [37, 39]},
                      {"ref_node": 39, 'linked_nodes': [38, 40]},
                      {"ref_node": 40, 'linked_nodes': [39, 41]},
                      {"ref_node": 41, 'linked_nodes': [36, 40]},
                      {"ref_node": 42, 'linked_nodes': [43, 47]},
                      {"ref_node": 43, 'linked_nodes': [42, 44]},
                      {"ref_node": 44, 'linked_nodes': [43, 45]},
                      {"ref_node": 45, 'linked_nodes': [44, 46]},
                      {"ref_node": 46, 'linked_nodes': [45, 47]},
                      {"ref_node": 47, 'linked_nodes': [42, 46]},
                      {"ref_node": 48, 'linked_nodes': [49, 59]},
                      {"ref_node": 49, 'linked_nodes': [48, 50]},
                      {"ref_node": 50, 'linked_nodes': [49, 51]},
                      {"ref_node": 51, 'linked_nodes': [50, 52]},
                      {"ref_node": 52, 'linked_nodes': [51, 53]},
                      {"ref_node": 53, 'linked_nodes': [52, 54]},
                      {"ref_node": 54, 'linked_nodes': [53, 55]},
                      {"ref_node": 55, 'linked_nodes': [54, 56]},
                      {"ref_node": 56, 'linked_nodes': [55, 57]},
                      {"ref_node": 57, 'linked_nodes': [56, 58]},
                      {"ref_node": 58, 'linked_nodes': [57, 59]},
                      {"ref_node": 59, 'linked_nodes': [48, 58]},
                      {"ref_node": 60, 'linked_nodes': [61, 67]},
                      {"ref_node": 61, 'linked_nodes': [60, 62]},
                      {"ref_node": 62, 'linked_nodes': [61, 63]},
                      {"ref_node": 63, 'linked_nodes': [62, 64]},
                      {"ref_node": 64, 'linked_nodes': [63, 65]},
                      {"ref_node": 65, 'linked_nodes': [64, 66]},
                      {"ref_node": 66, 'linked_nodes': [65, 67]},
                      {"ref_node": 67, 'linked_nodes': [60, 66]},
                      {"ref_node": 68, 'linked_nodes': []},
                      {"ref_node": 69, 'linked_nodes': []}]
    else:
        return None
    return remove_nodes(edges_list, del_nodes)


# Given a list of edges and a list of nodes to remove, remove all the edges pointing to the nodes to be removed,
# and the nodes from the list
def remove_nodes(edges_list, del_nodes) -> list:
    for del_node in del_nodes:
        curr_node = find_node(edges_list, del_node)
        if curr_node is not None:
            for linked_node_id in curr_node['linked_nodes']:
                linked_node_index = find_index(edges_list, linked_node_id)
                if linked_node_index is not None:
                    edges_list[linked_node_index]['linked_nodes'].remove(del_node)
            edges_list.remove(curr_node)
    return edges_list


# Given a dictionary(graph), keypoints taken from a JSON, the id of the given graph, the type of keypoints(pose,
# hand, face), and a flag for right an left hand, parse the keypoints by creating nodes with the following
# attributes: x, y and confidence. returns a list of keypoints parsed.
def parse_keypoints(key_graph, keypoints, id_count, keypoint_type='pose', right=True) -> list:
    out = []
    orientation = 'right' if right else 'left'
    n_keypoints = 75
    if keypoint_type == 'hand':
        n_keypoints = 63
    elif keypoint_type == 'face':
        n_keypoints = 210
    for i in range(0, n_keypoints, 3):
        x = keypoints[i]
        y = keypoints[i + 1]
        confidence = keypoints[i + 2]
        node_id = int(i / 3)
        if x != 0 or y != 0:
            if keypoint_type == 'hand':
                key_graph['people'][id_count]['nodes']['hands'][orientation].append(
                    dict(id=node_id, x=x, y=y, confidence=confidence))
            else:
                key_graph['people'][id_count]['nodes'][keypoint_type].append(
                    dict(id=node_id, x=x, y=y, confidence=confidence))
        else:
            out.append(node_id)
    return out


# Given a list of nodes and the id of a node, returns the given node if it exists, otherwise None
def find_node(node_list, node_id) -> dict or None:
    for node in node_list:
        if node['ref_node'] == node_id:
            return node
    return None


# Given a list of nodes, and the id of a node, returns the index of the given node if it exists, otherwise None
def find_index(node_list, node_id) -> int or None:
    for i in range(0, len(node_list)):
        if node_list[i]['ref_node'] == node_id:
            return i
    return None


def parse_graph(graph_data) -> dict:
    id_count = 0
    graph = {'people': []}
    for person in graph_data['people']:
        # Get keypoints
        pose_keypoints = person['pose_keypoints_2d']
        handl_keypoints = person['hand_left_keypoints_2d']
        handr_keypoints = person['hand_right_keypoints_2d']
        face_keypoints = person['face_keypoints_2d']
        # Create a new structure
        graph['people'].append(
            dict(id=id_count, nodes=dict(pose=[], hands=dict(left=[], right=[]), face=[]),
                 edges=dict(pose=[], hands=dict(left=[], right=[]), face=[])))
        # body pose parsing
        null_pose_nodes = parse_keypoints(graph, pose_keypoints, id_count)
        # hands pose parsing
        null_handl_nodes = parse_keypoints(graph, handl_keypoints, id_count, 'hand', False)
        null_handr_nodes = parse_keypoints(graph, handr_keypoints, id_count, 'hand')
        # face pose parsing
        null_face_nodes = parse_keypoints(graph, face_keypoints, id_count, 'face')
        # set edges and remove null nodes and edges from the nodes
        graph['people'][id_count]['edges']['pose'] = get_pose_edges(null_pose_nodes)
        graph['people'][id_count]['edges']['hands']['left'] = get_pose_edges(null_handl_nodes, 'hand')
        graph['people'][id_count]['edges']['hands']['right'] = get_pose_edges(null_handr_nodes, 'hand')
        graph['people'][id_count]['edges']['face'] = get_pose_edges(null_face_nodes, 'face')
        id_count += 1
    return graph


# Create an output directory, if it doesn't exists
try:
    os.mkdir(out_path)
except FileExistsError:
    print(out_path + " already exists...")
    pass

for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith('.json'):
            print(file)
            with open(root_path + file) as json_file:
                data = json.load(json_file)
            graph = parse_graph(data)
            with open(out_path + file, 'w') as out_file:
                json.dump(graph, out_file, indent=2)
    break
