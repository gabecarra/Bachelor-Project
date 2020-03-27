import os
import glob
from PIL import Image


def get_resolution(path_name) -> str:
    with open(path_name, 'r') as img_file:
        return img_file.read()


def generate_image_info(path):
    try:
        os.mkdir(path + '/out/')
    except FileExistsError:
        print(path + " already exists...")
        pass
    for img_path in glob.glob(path + '.png'):
        img = Image.open(img_path)
        img_name = img_path.split('/')[-1].split('.')[0].split('_')[0]
        with open(path + '/out/' + img_name + '.txt', 'w') as file:
            file.write(str(img.size[0]) + 'x' + str(img.size[1]))
