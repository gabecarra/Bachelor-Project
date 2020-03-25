import json
import sys
import os
import matplotlib.pyplot as plt

root_path = sys.argv[1] + '/'
out_path = root_path + '/out/'


def get_edges() -> object:
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
                  {"ref_node": 24, 'linked_nodes': [11]},
                  ]
    return edges_list


def parse_pose(pose_graph, keypoints):
    out = []
    for i in range(0, 75, 3):
        x = keypoints[i]
        y = keypoints[i + 1]
        confidence = keypoints[i + 2]
        index = int(i / 3)
        if x != 0 or y != 0:
            pose_graph['people'][id_count]['nodes']['pose'].append(
                dict(id=index, x=x, y=y, confidence=confidence))
        else:
            out.append(index)
    return out


try:
    os.mkdir(out_path)
except FileExistsError:
    print(out_path + " already exists...")
    pass

for root, dirs, files in os.walk(root_path):
    for file in files:
        print(file)
        if file.endswith('.json'):
            with open(root_path + file) as json_file:
                data = json.load(json_file)
                graph = {'people': []}
                id_count = 0
                for person in data['people']:
                    pose_keypoints = person['pose_keypoints_2d']
                    graph['people'].append(
                        dict(id=id_count, nodes=dict(pose=[], hands=dict(left=[], right=[]), face=[]), edges=[]))

                    # body pose parsing
                    null_nodes = parse_pose(graph, pose_keypoints)
                    print(null_nodes)

                    # set edges and remove null nodes and edges from the nodes
                    graph['people'][id_count]['edges'] = get_edges()
                    for node in null_nodes:
                        print(node)
                        temp = graph['people'][id_count]['edges'][node]
                        temp = next((item for item in graph['people'][id_count]['edges'] if item["ref_node"] == node), None)
                        print(temp)
                        for n in temp['linked_nodes']:
                            print(n)
                            try:
                                graph['people'][id_count]['edges'][n]['linked_nodes'].remove(node)
                            except ValueError:
                                pass
                        try:
                            graph['people'][id_count]['edges'].remove(temp)
                        except ValueError:
                            pass

                    id_count += 1
            with open(out_path + file, 'w') as out_file:
                json.dump(graph, out_file, indent=2)
    break
