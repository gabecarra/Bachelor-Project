import os
import sys
import time
from math import ceil
from statistics import mean
from sys import platform
import numpy as np

import cv2
import progress.bar as progress_bar

import src.graph_parser as gp

# Import OpenPose python wrapper
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Windows Import
    if platform == "win32":
        sys.path.append(
            dir_path + '../openpose/build/python/openpose/Release'
        )
        path = os.environ['PATH'] + ';' + \
               dir_path + '/../../x64/Release;' + \
               dir_path + '/../../bin;'
        os.environ['PATH'] = path
        import pyopenpose as op
    else:
        # OSX/Linux
        sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error during openpose import!')
    raise e

# ---FLAG FOR CLI MODE---
__cli = False


# ---HELPER FUNCTIONS---

def __parse_args(args) -> (dict, dict):
    """
    Given a list of arguments, divide it in two sub lists, one
    containing the operations that are done by GraphPipe, and the other
    containing the operations that are done by OpenPose. The two lists
    are then parsed, and returned as dictionaries.
    :param list args: list of arguments
    :return (dict, dict): 2 dictionaries of parsed arguments, one for
    GraphParse and another for OpenPose
    """
    args = [x.split(' ') for x in args]
    gp_dict = dict(display='0',
                   image_dir=None,
                   video=None,
                   write_json=None)
    gp_default = ['--write_json',
                  '--video',
                  '--image_dir',
                  '--display',
                  '--normalize_output']
    op_list = []
    gp_list = []
    for i in range(len(args)):
        if args[i][0] in gp_default:
            [gp_list.append(x) for x in args[i]]
        else:
            [op_list.append(x) for x in args[i]]
    op_dict = __generate_args_dict(op_list)
    temp_dict = __generate_args_dict(gp_list)
    for key in gp_dict.keys():
        if key in temp_dict.keys():
            gp_dict[key] = temp_dict[key]
    return gp_dict, op_dict


def __generate_args_dict(args: list) -> dict:
    """
    Given a list of arguments, parse them and returns a dictionary of
    parsed arguments
    :param list args: list of arguments
    :return dict: dictionary of parsed arguments
    """
    args_dict = dict()
    args_size = len(args)
    for i in range(0, args_size):
        curr_keyword = args[i]
        # if the current keyword is not the last one
        if i != args_size - 1:
            next_keyword = args[i + 1]
        else:
            next_keyword = '1'
        if '--' in curr_keyword:
            keyword = curr_keyword.replace('-', '')
            if keyword not in args_dict:
                if '--' in next_keyword:
                    args_dict[keyword] = '1'
                else:
                    args_dict[keyword] = next_keyword
    return args_dict


def __generate_bar(text: str, size: int):
    """
    Generates a loading bar for tracking OpenPose processing operations
    :param str text: string that will be printed before the progress bar
    :param size: length of the progress bar(n of elements)
    :return:
    """
    return progress_bar.IncrementalBar(
        text,
        max=size,
        suffix='%(index)d/%(max)d'
    )


def get_keypoints(node_type, datum):
    keypts_list = []
    # Pose
    if node_type['pose']:
        keypts_list = [datum.poseKeypoints]
    # Face
    if node_type['face']:
        keypts_list.append(datum.faceKeypoints)
    # Hand
    if node_type['hand']:
        keypts_list.append(datum.handKeypoints[0])
        keypts_list.append(datum.handKeypoints[1])
    return keypts_list


def __display_img(img):
    """
    Given an image represented as a numpy array of rgb values, displays
    the image processed by OpenPose
    :param img: numpy n array of rgb values
    :return None: In order to stop the
    """
    cv2.imshow('image', img)
    key = cv2.waitKey(1000)
    if key == 27:
        cv2.destroyAllWindows()


def __display_fps(fps_count: int, start, output):
    """
    Adds the fps counter to the left top corner of the stream
    :param int fps_count: number of frames processed
    :param start: the time when the stream started
    :param output: the OpenPose output image
    :return: the output image with the fps counter + prints it in
    console
    """
    fps_value = fps_count / (time.time() - start)
    # print('Current FPS: ' + str(fps_value), end='\r')
    return cv2.putText(output,
                       str(round(fps_value, 2)) + ' FPS',
                       (50, 50),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       1,
                       (57, 255, 20),
                       2, cv2.LINE_AA)


def __get_node_types(args: dict):
    """
    Given the parsed arguments, returns a dictionary of flags
    representing the node types to be processed
    :param dict args: dictionary of parsed args
    :return: dictionary of node types
    """
    out = dict(pose=False, hand=False, face=False)
    # check if only face or only hand is required
    if 'body' in args and args['body'] == '0':
        # only hand
        if 'hand' in args and 'face' not in args or args['face'] == '0':
            out['hand'] = True
            return out
        # only face
        elif 'face' in args and 'hand' not in args or args['hand'] == '0':
            out['face'] = True
            return out
        else:
            raise RuntimeError('--hand and --face cannot be used'
                               'simultaneously with --body 0')
    else:
        out['pose'] = True
        if 'hand' in args:
            out['hand'] = True
        if 'face' in args:
            out['face'] = True
    return out


def __get_hands_img(img, keypts, blend=False):
    """
    Draw the keypoints generated by OpenPose on the given image, and
    returns it
    :param img: image given as a n array of rgb values
    :param keypts: keypoints of the hand
    :return: image processed as rbg n array
    """
    if blend:
        img = np.zeros(img.shape)
    # node colors in bgr
    colors = [(100, 100, 100),
              (0, 0, 100),
              (0, 0, 150),
              (0, 0, 200),
              (0, 0, 255),
              (0, 100, 100),
              (0, 150, 150),
              (0, 200, 200),
              (0, 255, 255),
              (50, 100, 0),
              (75, 150, 0),
              (100, 200, 0),
              (125, 255, 0),
              (100, 50, 0),
              (150, 75, 0),
              (200, 100, 0),
              (255, 125, 0),
              (100, 0, 100),
              (150, 0, 150),
              (200, 0, 200),
              (255, 0, 255)]
    for i in range(1, 21, 4):
        img = cv2.line(img,
                       (keypts[0][0][0], keypts[0][0][1]),
                       (keypts[0][i][0], keypts[0][i][1]),
                       colors[i],
                       ceil(img.shape[1] * 0.015),
                       lineType=cv2.LINE_AA)
        for j in range(i, i + 3):
            img = cv2.line(img,
                           (keypts[0][j][0], keypts[0][j][1]),
                           (keypts[0][j + 1][0], keypts[0][j + 1][1]),
                           colors[j + 1],
                           ceil(img.shape[1] * 0.015),
                           lineType=cv2.LINE_AA)
    for i in range(len(keypts[0])):
        img = cv2.circle(img,
                         (keypts[0][i][0], keypts[0][i][1]),
                         ceil(img.shape[1] * 0.017),
                         colors[i],
                         -1,
                         lineType=cv2.LINE_AA)
    return img


# ---OPENPOSE PROCESSING---


def __process_images(openpose, args, node_type):
    """
    Process an image or a set of images, in order to get the prediction
    of keypoints for the parts defined by node_type
    :param openpose: OpenPose wrapper
    :param dict args: dictionary of default arguments
    :param dict node_type: dictionary of flags that represents the type
    of nodes to be processed
    :return list: returns a list of Networkx graphs, if __cli=False,
    otherwise None
    """
    paths = op.get_images_on_directory(args['image_dir'])
    bar = __generate_bar('Applying image processing: ', len(paths))
    start = time.time()
    nx_graph_list = []
    bar.start()
    for img_path in paths:
        datum = op.Datum()
        img = cv2.imread(img_path)
        datum.cvInputData = img
        openpose.emplaceAndPop([datum])
        bar.next()
        if args['display'] == '1':
            __display_img(datum.cvOutputData)
        filename = str(os.path.splitext(img_path)[0].split('/')[-1])
        keypts = get_keypoints(node_type, datum)
        nx_graph = gp.parse(keypts,
                            args['write_json'],
                            img.shape,
                            node_type,
                            filename,
                            __cli)
        if not __cli:
            nx_graph_list.append(nx_graph)
    bar.finish()
    end = time.time()
    print("Image processing successfully finished. Total time: {:.2f}s"
          .format(end - start))
    if __cli:
        return None
    return nx_graph_list


def __process_hands(openpose, args, node_type):
    """
    Applies hands processing to an image or a set of images, in order to
    get the prediction of its keypoints
    :param openpose: OpenPose wrapper
    :param dict args: dictionary of default arguments
    :param dict node_type: dictionary of flags that represents the type
    of nodes to be processed
    """
    image_paths = op.get_images_on_directory(args['image_dir'])
    bar = __generate_bar('Applying hands recognition: ', len(image_paths))
    start = time.time()
    idx = 0
    nx_graph_list = []
    for image_path in image_paths:
        datum = op.Datum()
        image_to_process = cv2.imread(image_path)
        datum.cvInputData = image_to_process
        a = image_to_process.shape[0]
        b = image_to_process.shape[1]
        hand_rectangles = [
            [
                op.Rectangle(0., a / 2 - b / 2, a, a),
                op.Rectangle(0., a / 2 - b / 2, a, a),
            ]
        ]
        datum.handRectangles = hand_rectangles
        openpose.emplaceAndPop([datum])
        bar.next()
        left = datum.handKeypoints[0]
        right = datum.handKeypoints[1]
        left_is_best = mean(left[0][:, 2]) >= mean(right[0][:, 2])
        keypts = left if left_is_best else right
        if args['disable_blending'] == '1':
            img = __get_hands_img(image_to_process, keypts, True)
        else:
            img = __get_hands_img(image_to_process, keypts)
        if args['display'] == '1':
            __display_img(img)
        if args['write_images']:
            ext = os.path.splitext(image_path)[1]
            out_path = args['write_images'][: args['write_images'].rfind('/')] + \
                '/' + str(idx) + '_rendered' + ext
            try:
                os.mkdir(args['write_images'])
            except FileExistsError:
                pass
            cv2.imwrite(out_path, img)
            idx += 1
        filename = str(os.path.splitext(image_path)[0].split('/')[-1])
        keypts = get_keypoints(node_type, datum)
        nx_graph = gp.parse(keypts,
                            args['write_json'],
                            img.shape,
                            node_type,
                            filename,
                            __cli)
        if not __cli:
            nx_graph_list.append(nx_graph)
    bar.finish()
    end = time.time()
    print("Hands processing successfully finished. Total time: {:.2f}s"
          .format(end - start))
    if __cli:
        return None
    return nx_graph_list


def __process_video(openpose, args, node_type: dict):
    """
    Process an video in order to get the prediction of keypoints for
    face, hands and body, as indicated by node_types
    :param openpose: OpenPose wrapper
    :param dict args: dictionary of default arguments
    :param dict node_type: dictionary of flags that represents the type
    of nodes to be processed
    """
    video = cv2.VideoCapture(args['video'])
    n_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    if n_frames == 0:
        raise FileNotFoundError(args['video'] + ' not found!')
    bar = progress_bar.IncrementalBar(
        'Applying OpenPose recognition: ',
        max=n_frames,
        suffix='%(index)d/%(max)d'
    )
    start = time.time()
    frame_idx = 0
    nx_graph_list = []
    while video.isOpened():
        datum = op.Datum()
        ret, video_frame = video.read()
        if ret:
            datum.cvInputData = video_frame
            openpose.emplaceAndPop([datum])
            bar.next()
            if args['display'] == '1':
                __display_img(datum.cvOutputData)
            filename = str(os.path.splitext(args['video'])[0].split('/')[-1])
            filename = filename + str(frame_idx)
            keypts = get_keypoints(node_type, datum)
            nx_graph = gp.parse(keypts,
                                args['write_json'],
                                video_frame.shape,
                                node_type,
                                filename,
                                __cli)
            frame_idx += 1
            if not __cli:
                nx_graph_list.append(nx_graph)
    bar.finish()
    end = time.time()
    print("Video processing successfully finished. Total time: {:.2f}s"
          .format(end - start))
    if __cli:
        return None
    return nx_graph_list


def __process_stream(openpose, args, node_type: dict):
    """
    Applies OpenPose prediction to a stream such as a camera, in order
    to get the prediction of keypoints for face, hands and body, as
    indicated by node_types
    :param openpose: OpenPose wrapper
    :param dict args: dictionary of default arguments
    :param dict node_type: dictionary of flags that represents the type
    of nodes to be processed
    """
    cap = cv2.VideoCapture(0)
    cap.open(0)
    start = time.time()
    fps = 1
    frame_idx = 0
    while True:
        datum = op.Datum()
        ret, frame = cap.read()
        if ret:
            datum.cvInputData = frame
            openpose.emplaceAndPop([datum])
            cv2.imshow('frame', __display_fps(fps, start, datum.cvOutputData))
            fps += 1
            filename = 'capture' + str(frame_idx)
            keypts = get_keypoints(node_type, datum)
            gp.parse(keypts,
                     args['write_json'],
                     frame.shape,
                     node_type,
                     filename,
                     __cli)
            frame_idx += 1
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


def run(args):
    """
    Parses the given arguments, and applies run the pipeline on the
    given input. If __cli = False, returns a list of Networkx graphs
    :param list args: list of strings representing the arguments/flags
    passed to the pipeline
    :return: list of NetworkX graphs, if __cli = False, otherwise None
    """

    gp_args, op_args = __parse_args(args)

    # path to openpose models
    if 'model_folder' not in op_args:
        op_args['model_folder'] = '../openpose/models/'
    node_type = __get_node_types(op_args)
    only_hands = node_type['hand'] \
        and not node_type['pose'] \
        and not node_type['face']
    if only_hands:
        gp_args['write_images'] = op_args.pop('write_images', None)
        gp_args['disable_blending'] = op_args.pop('disable_blending', None)

    # Starting OpenPose
    op_wrapper = op.WrapperPython()
    op_wrapper.configure(op_args)
    op_wrapper.start()

    usage_err = 'Usage: ' + os.path.basename(__file__) + \
                ' --image_dir [path] or --video [path]'

    # video processing
    if gp_args['video']:
        if gp_args['image_dir']:
            raise IndexError(usage_err)
        return __process_video(op_wrapper, gp_args, node_type)

    # image processing
    elif gp_args['image_dir']:
        if gp_args['video']:
            raise IndexError(usage_err)
        if only_hands:
            return __process_hands(op_wrapper, gp_args, node_type)
        else:
            return __process_images(op_wrapper, gp_args, node_type)

    # stream processing
    else:
        try:
            __process_stream(op_wrapper, gp_args, node_type)
            return None
        except IndexError:
            print(usage_err)


if __name__ == '__main__':
    sys_args = sys.argv[1:]
    parsed_args = []
    for i in range(len(sys_args)):
        if '--' in sys_args[i]:
            if i < len(sys_args) - 1 and '--' not in sys_args[i + 1]:
                parsed_args.append(sys_args[i] + ' ' + sys_args[i + 1])
            else:
                parsed_args.append(sys_args[i])
    __cli = True
    run(parsed_args)
