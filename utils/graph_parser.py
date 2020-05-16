"""
@author Carraretto Gabriel H.
@license MIT
Parses a given set of JSON OpenPose structured data in a cleaner and
more easy-to-use JSON structured data. Can be used as it its, or by
passing the path to the JSON files in command line. If a path is not
given,it will assume that the data folder is in the same path as the
script.
"""

import glob
import ujson
import os
import sys
from statistics import mean

import progress.bar as progress_bar

from utils import image_info, edges_ref

__DEFAULT_PATH = './data/'


def __parse_edges(graph: dict, del_nodes: list, index: int, node_type: str):
    """
    Given a graph, a list of nodes to be deleted and the type of
    nodes(pose, hand or face), takes the edge set specified by
    node_type, removes the edges specified in del_nodes list, and return
    the resulting set of edges.
    :param graph: Graph represented as a dict, containing only nodes
    :param list del_nodes: Nodes to be deleted
    :param int index: Index of the current person
    :param str node_type: Type of nodes needed
    ('pose', 'hand' or 'face'). Default: 'pose'
    """
    if node_type not in ['pose', 'handl', 'handr', 'face']:
        raise ValueError('Given type of keypoints is unsupported!...')
    edges_list = edges_ref.get_edges(node_type)
    for del_node in del_nodes:
        curr_node = __find_node(edges_list, del_node)
        if curr_node is not None:
            for linked_node_id in curr_node['linked_nodes']:
                node_i = __find_index(edges_list, linked_node_id)
                if node_i is not None:
                    edges_list[node_i]['linked_nodes'].remove(del_node)
            edges_list.remove(curr_node)
    orientation = 'right' if node_type == 'handr' else 'left'
    if node_type in ['handr', 'handl']:
        graph['people'][index]['edges']['hands'][orientation] = edges_list
    else:
        graph['people'][index]['edges'][node_type] = edges_list


def __parse_nodes(graph: dict, keypoints: list, index: int, k_type: str) -> list:
    """
    Given a graph represented as a dictionary, keypoints taken from a
    JSON, the index of the given graph, the type of keypoints
    (pose,handl, handr, face), parse the keypoints by creating nodes
    with the following attributes: {x, y, confidence}. Appends each node
    to the given graph.
    :param dict graph: Graph represented as a dictionary
    :param list keypoints: List of keypoints taken from OpenPose JSON
    :param int index: Counter that represents the id of the current
    person keypoints being parsed
    :param str k_type: Type of the given keypoints. Can be one of:
    'pose', 'handl', 'handr' or 'face'
    :return list: List of indexes of nodes for which no information was
    obtained by OpenPose
    """
    index_list = []
    orientation = 'right' if k_type == 'handr' else 'left'
    if k_type == 'pose':
        n_keypoints = 75
    elif k_type in ['handr', 'handl']:
        n_keypoints = 63
    elif k_type == 'face':
        n_keypoints = 210
    else:
        print(k_type)
        raise ValueError('Given type of nodes is unsupported!...')
    for i in range(0, n_keypoints, 3):
        x = keypoints[i]
        y = keypoints[i + 1]
        confidence = keypoints[i + 2]
        node_id = int(i / 3)
        if k_type in ['handl', 'handr']:
            graph['people'][index]['nodes']['hands'][orientation].append(
                dict(
                    id=node_id,
                    x=x,
                    y=y,
                    confidence=confidence
                )
            )
        else:
            graph['people'][index]['nodes'][k_type].append(
                dict(
                    id=node_id,
                    x=x,
                    y=y,
                    confidence=confidence
                )
            )
        if x == 0 and y == 0:
            index_list.append(node_id)
    return index_list


def __find_node(node_list: list, node_id: int) -> dict or None:
    """
    Given a list of nodes and the id of a node, returns the given node
    if it exists, otherwise None
    :param list node_list: List of nodes
    :param int node_id: The id of a node
    :return dict or None: The node with the given id, if it is found,
    otherwise None
    """
    for node in node_list:
        if node['ref_node'] == node_id:
            return node
    return None


def __find_index(node_list: list, node_id: int) -> int or None:
    """
    Given a list of nodes, and the id of a node, returns the position of
    the given node inside the list if it exists, otherwise None
    :param list node_list: List of nodes
    :param int node_id: The id of a node
    :return int: Position of the node with the given id in the list,
    otherwise None
    """
    for i in range(0, len(node_list)):
        if node_list[i]['ref_node'] == node_id:
            return i
    return None


def __parse_graph(open_pose_data: dict, filename: str, path=None, res=None) -> dict:
    """
    Given an OpenPose dataset_info, the codename of the file, and the
    path to the dataset_info returns the dataset_info parsed as a
    graph(JSON)
    :param dict open_pose_data: Dictionary containing all the data
    generated by OpenPose
    :param str filename: name of a file (es. 099945052)
    :param str path: Path where the data is located
    :return dict: Graph represented as a dictionary
    """
    index = 0
    if res is None:
        image_info_path = path + '/out_res/' + filename + '.txt'
        res = image_info.get_resolution(image_info_path)
    graph = dict(filename=filename,
                 resolution=res,
                 people=[])
    for person in open_pose_data['people']:
        # Get keypoints
        pose_keypts = person['pose_keypoints_2d']
        handl_keypts = person['hand_left_keypoints_2d']
        handr_keypts = person['hand_right_keypoints_2d']
        face_keypts = person['face_keypoints_2d']
        graph['people'].append(
            dict(
                id=index,
                nodes=dict(
                    pose=[],
                    hands=dict(
                        left=[],
                        right=[]
                    ),
                    face=[]
                ),
                edges=dict(
                    pose=[],
                    hands=dict(
                        left=[],
                        right=[]
                    ),
                    face=[]
                )
            )
        )
        # nodes and edges parsing
        if len(pose_keypts) > 0:
            null_pose_nodes = __parse_nodes(graph, pose_keypts, index, 'pose')
            __parse_edges(graph, null_pose_nodes, index, 'pose')
        if len(handl_keypts) > 0:
            null_handl_nodes = __parse_nodes(graph, handl_keypts, index, 'handl')
            __parse_edges(graph, null_handl_nodes, index, 'handl')
        if len(handr_keypts) > 0:
            null_handr_nodes = __parse_nodes(graph, handr_keypts, index, 'handr')
            __parse_edges(graph, null_handr_nodes, index, 'handr')
        if len(face_keypts) > 0:
            null_face_nodes = __parse_nodes(graph, face_keypts, index, 'face')
            __parse_edges(graph, null_face_nodes, index, 'face')
        index += 1
    return graph


def openpose_to_json(path: str):
    """
    Given a path to a folder containing JSON files generated by
    OpenPose, parse the files and generate a set of graphs based on the
    data set given, and save them as JSON in '../out/'
    :param str path: path containing data generated by OpenPose
    """
    # Create an output directory, if it doesn't exists
    try:
        print('Creating output folder...', end='')
        os.mkdir(path + '/out/')
    except FileExistsError:
        print('folder already exists!')
    else:
        print('done')
    files = glob.glob(path + '*.json')
    if len(files) == 0:
        raise ValueError('No JSON files found in' + path)
    bar = progress_bar.IncrementalBar(
        'Parsing files: ',
        max=len(files),
        suffix='%(index)d/%(max)d, Elapsed: %(elapsed)ds'
    )
    bar.start()
    for file in files:
        filename = file.split('/')[-1]
        with open(file) as json_file:
            data = ujson.load(json_file)
            graph = __parse_graph(
                data,
                filename.split('.')[0].split('_')[0],
                path
            )
            with open(path + '/out/' + filename, 'w') as out_file:
                ujson.dump(graph, out_file)
        bar.next()
    bar.finish()


def __generate_openpose_dict(keypoints, node_type: dict) -> dict:
    """
    Given a set of keypoints as numpy array, and a set of node types,
    generates a dictionary structured as the JSON generated by Openpose
    :param keypoints: numpy array of keypoints
    :param list node_type: list of node types. Can be one of 'pose',
    'hand' or 'face'
    :return dict: dictionary of keypoints
    """
    keypts_dict = dict(people=[])
    n_person = keypoints[0].shape[0]
    for i in range(n_person):
        person = dict(
            pose_keypoints_2d=[],
            face_keypoints_2d=[],
            hand_left_keypoints_2d=[],
            hand_right_keypoints_2d=[]
        )
        n = 0
        if node_type['pose']:
            pose = keypoints[0][i].flatten().tolist()
            person['pose_keypoints_2d'] = pose
            n += 1
        if node_type['face']:
            face = keypoints[0 + n][i].flatten().tolist()
            person['face_keypoints_2d'] = face
            n += 1
        if node_type['hand']:
            left = keypoints[0][i].flatten().tolist()
            right = keypoints[1][i].flatten().tolist()
            only_hand = not node_type['pose'] and not node_type['face']
            left_is_best = mean(left) >= mean(right)
            person['hand_left_keypoints_2d'] = left
            person['hand_right_keypoints_2d'] = right
            if only_hand and left_is_best:
                person['hand_right_keypoints_2d'] = []
            elif only_hand and not left_is_best:
                person['hand_left_keypoints_2d'] = []
        keypts_dict['people'].append(person)
    return keypts_dict


def points_to_json(keypoints, path: str, img_res: list, node_type: dict,
                   filename: str):
    """
    Given a set of points as numpy array generated by OpenPose, parses
    them and generate a JSON file in the given path
    :param keypoints: set of keypoints generated by OpenPose.
    :param str path: path where the output file should be saved
    :param str img_res: resolution of the given frame/images separated
    by an x. Ex: '1920x1080'
    :param dict node_type: dictionary of flags that represents the type
    of nodes for each keypoint
    :param str filename: name of the given file processed by OpenPose
    """
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    openpose_dict = __generate_openpose_dict(keypoints, node_type)
    graph = __parse_graph(openpose_dict,
                          filename,
                          res=str(img_res[1]) + 'x' + str(img_res[0]))
    json_file = path + filename + '_keypoints.json'
    with open(json_file, 'w') as out_file:
        ujson.dump(graph, out_file)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        openpose_to_json(__DEFAULT_PATH)
    else:
        openpose_to_json(sys.argv[1])
