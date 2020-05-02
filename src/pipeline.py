import sys
import cv2
import os
from sys import platform
import argparse
import time
import progress.bar as progress_bar

# Import OpenPose python wrapper
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    # Windows Import
    if platform == "win32":
        sys.path.append(
            dir_path + '../openpose/build/python/openpose/Release'
        )
        path = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' + dir_path + '/../../bin;'
        os.environ['PATH'] = path
        import pyopenpose as op
    else:
        # OSX/Linux
        sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError as e:
    print('Error during openpose import!')
    raise e


def parse_config_params(arg_size):
    params = dict()
    for i in range(0, arg_size):
        curr_keyword = args[1][i]
        # if the current keyword is not the last one
        if i != arg_size - 1:
            next_keyword = args[1][i + 1]
        else:
            next_keyword = '1'
        if '--' in curr_keyword:
            keyword = curr_keyword.replace('-', '')
            if keyword not in params:
                if '--' in next_keyword:
                    params[keyword] = '1'
                else:
                    params[keyword] = next_keyword
    return params


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    try:
        # default params
        parser.add_argument('--image_dir')
        parser.add_argument('--video')
        parser.add_argument('--display', default='0')
        args = parser.parse_known_args()

        # Custom params
        params = parse_config_params(len(args[1]))
        params["model_folder"] = "../openpose/models/"

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Read frames on directory
        if args[0].image_dir is not None:
            imagePaths = op.get_images_on_directory(args[0].image_dir)
        elif args[0].video is not None:
            # TODO: implement video recognition
            pass
        start = time.time()

        bar = progress_bar.IncrementalBar(
            'Applying pose recognition: ',
            max=len(imagePaths),
            suffix='%(index)d/%(max)d'
        )

        # Process and display images
        for imagePath in imagePaths:
            datum = op.Datum()
            imageToProcess = cv2.imread(imagePath)
            datum.cvInputData = imageToProcess
            opWrapper.emplaceAndPop([datum])
            bar.next()

            # print("Body keypoints: \n" + str(datum.poseKeypoints))

            if args[0].display == '1':
                cv2.imshow("OpenPose Image", datum.cvOutputData)
                key = cv2.waitKey(15)
                if key == 27:
                    break
        bar.finish()
        end = time.time()
        print("Pose recognition successfully finished. Total time: "
              + str(end - start) + " seconds")
    except Exception as e:
        print(e)
        sys.exit(-1)

