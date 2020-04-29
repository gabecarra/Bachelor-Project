
def get_labels(node_type: str):
    # TODO: add labels for head and hands
    if node_type == 'pose':
        label_list = [
            {'id': 0, 'label': 'head'},
            {'id': 1, 'label': 'upper_spine'},
            {'id': 2, 'label': 'right_shoulder'},
            {'id': 3, 'label': 'right_elbow'},
            {'id': 4, 'label': 'right_wrist'},
            {'id': 5, 'label': 'left_shoulder'},
            {'id': 6, 'label': 'left_elbow'},
            {'id': 7, 'label': 'left_wrist'},
            {'id': 8, 'label': 'lower_spine'},
            {'id': 9, 'label': 'right_hip'},
            {'id': 10, 'label': 'right_knee'},
            {'id': 11, 'label': 'right_ankle'},
            {'id': 12, 'label': 'left_hip'},
            {'id': 13, 'label': 'left_knee'},
            {'id': 14, 'label': 'left_ankle'},
            {'id': 15, 'label': 'right_eye'},
            {'id': 16, 'label': 'left_eye'},
            {'id': 17, 'label': 'right_ear'},
            {'id': 18, 'label': 'left_ear'},
            {'id': 19, 'label': 'left_big_toe'},
            {'id': 20, 'label': 'left_little_toe'},
            {'id': 21, 'label': 'left_heel'},
            {'id': 22, 'label': 'right_big_toe'},
            {'id': 23, 'label': 'right_little_toe'},
            {'id': 24, 'label': 'right_heel'}]
    else:
        raise ValueError(node_type + ' is not supported!...')
    return label_list
