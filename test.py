import json
import sys
import os
import matplotlib.pyplot as plt
import networkx as nx

root_path = sys.argv[1] + '/'
out_path = root_path + '/out/'
G = nx.Graph()
POSE_EDGES = [(0, 1), (0, 15), (0, 16), (1, 2), (1, 5), (1, 8), (2, 3), (3, 4), (5, 6), (6, 7), (8, 9), (8, 12),
              (9, 10), (10, 11), (10, 11), (11, 22), (11, 24), (12, 13), (13, 14), (14, 19), (14, 21), (15, 17),
              (16, 18), (19, 20), (22, 23)]


# Given a dictionary(graph), keypoints taken from a JSON, the id of the given graph, the type of keypoints(pose,
# hand, face), and a flag for right an left hand, parse the keypoints by creating nodes with the following
# attributes: x, y and confidence. returns a list of keypoints parsed.
def parse_keypoints(keypoints, keypoint_type='pose') -> (nx.Graph, list):
    graph = nx.Graph()
    out = []
    n_keypoints = 75
    if keypoint_type == 'hand':
        n_keypoints = 63
    elif keypoint_type == 'face':
        n_keypoints = 210
    for i in range(0, n_keypoints, 3):
        x = keypoints[i]
        y = keypoints[i + 1]
        confidence = keypoints[i + 2]
        index = int(i / 3)
        if x != 0 or y != 0:
            graph.add_node(index, x=x, y=y, confidence=confidence)
        else:
            out.append(index)
    return graph, out


def parse_graph(graph_data):
    for person in graph_data['people']:
        # Get keypoints
        pose_keypoints = person['pose_keypoints_2d']
        handl_keypoints = person['hand_left_keypoints_2d']
        handr_keypoints = person['hand_right_keypoints_2d']
        face_keypoints = person['face_keypoints_2d']
        pose_graph, pose_null_nodes  = parse_keypoints(pose_keypoints)
        handl_graph, handl_null_nodes  = parse_keypoints(handl_keypoints, 'hand')
        handr_graph, handr_null_nodes = parse_keypoints(handr_keypoints, 'hand')
        face_graph, face_null_nodes = parse_keypoints(face_keypoints, 'face')



try:
    os.mkdir(out_path)
except FileExistsError:
    print(out_path + " already exists...")
    pass

# for root, dirs, files in os.walk(root_path):
#     for file in files:
#         if file.endswith('.json'):
#             print(file)
#             with open(root_path + file) as json_file:
#                 data = json.load(json_file)
#                 person_index = 0
#                 out_string = {'people': []}
#
#                     G.add_edges_from(EDGES)
#                     for node in null_nodes:
#                         for edge in G.edges:
#                             if node in edge:
#                                 G.remove_edge(edge[0], edge[1])
#                     out_string['people'].append({'id': person_index, 'value': nx.adjacency_data(G)})
#                     person_index += 1
#             with open(out_path + file, 'w') as out_file:
#                 json.dump(out_string, out_file, indent=2)
#             G.clear()
#     break
# nx.draw(G, with_labels='true', font_color='white', font_weight='bold')
#           plt.show()
