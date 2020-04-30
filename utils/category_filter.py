"""
Carraretto Gabriel H.
category_filter
Retrieves a set of filenames associated to a given category
"""

import scipy.io

PATH = 'dataset_info/dataset_info.mat'


def parse_category(cat_name: str, path=PATH):
    """
    Given a category and a path, parses the elements inside a .mat file,
    in order to retrieve all the image file names that are within the
    given category
    :param str cat_name: category of a given activity
    :param str path: path to the .mat file
    :return list: list of file names to be retrieved
    """
    file = scipy.io.loadmat(path)
    images = file['images'][0]
    file_list = []
    for i in range(0, len(images)):
        if images[i]['cat_name'].size != 0 and \
                images[i]['cat_name'] == cat_name:
            file_list.append(
                images[i]['name'][0].replace('.jpg', '_keypoints.json')
            )
    return file_list
