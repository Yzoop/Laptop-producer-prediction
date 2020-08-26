import src.laptop_store_parser.myparser as myparser
import pandas as pd
import requests
import os
import cv2

__SAVE_DIR__ = 'laptop-images/'


def get_average_shape(full_image_pathes) -> tuple:
    average_shape = [0, 0, 0]
    for img_path in full_image_pathes:
        cur_shape = list(cv2.imread(img_path).shape)
        for i in range(len(average_shape)):
            average_shape[i] += (cur_shape[i] / len(full_image_pathes))
    average_shape = tuple([round(val) for val in average_shape])
    return average_shape


def resize_images(full_image_pathes, new_size):
    new_size = new_size[:2][::-1]
    for img_path in full_image_pathes:
        img = cv2.imread(img_path)
        img = cv2.resize(img, new_size)
        cv2.imwrite(img_path, img)


def preprocess_downloaded_images():
    print(os.getcwd())
    full_image_pathes = []
    for class_folder in os.listdir(__SAVE_DIR__):
        for image_path in os.listdir(__SAVE_DIR__ + class_folder):
            full_image_pathes.append(__SAVE_DIR__ + class_folder + '/' + image_path)
    average_shape = get_average_shape(full_image_pathes)
    resize_images(full_image_pathes, average_shape)


def start_downloading_images(class_names,
                             csv_path=myparser.__LAPTOP_TABLE_PATH__,
                             verbose=False,
                             folder_directory=__SAVE_DIR__):
    os.chdir('../')
    # laptop_csv = pd.read_csv(csv_path)
    # for img_link, producer in zip(laptop_csv[myparser.__IMAGE_LINK__], laptop_csv[myparser.__LAPTOP_NAME__]):
    #     response = requests.get(img_link)
    #     name = img_link.split('/')[-1]
    #     file = open(folder_directory + '/' + producer + '/' + name, 'wb')
    #     file.write(response.content)
    #     file.close()
    #     if verbose:
    #         print('image', name, 'has successfully been saved')
