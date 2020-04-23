import scipy.io

PATH = 'mpii_human_pose/dataset.mat'


def parse_category(cat_name: str):
    """
    Given a category, parses the elements inside a .mat file, in order to retrieve all the image file names that are
    within the given category
    :param str cat_name: category of a given activity
    :return list: list of file names to be retrieved
    """
    file = scipy.io.loadmat(PATH)
    images = file['images'][0]
    file_list = []
    for i in range(0, len(images)):
        if images[i]['cat_name'].size != 0 and images[i]['cat_name'] == cat_name:
            file_list.append(images[i]['name'][0].replace('.jpg', '_keypoints.json'))
    print('Images found: ', len(file_list))
    print(file_list)
    return file_list
