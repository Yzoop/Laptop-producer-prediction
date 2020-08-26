from src.laptop_store_parser import myparser, image_processing
import pandas as pd
import os



def get_laptop_producer_names():
    os.chdir('../')
    print(os.getcwd())
    laptop_full_names = pd.read_csv(myparser.__LAPTOP_TABLE_PATH__)[myparser.__LAPTOP_NAME__]
    producer_names = []
    for full_name in laptop_full_names:
        producer_names.append(myparser.get_producer_name(full_name))
    return list(set(producer_names))


def create_producer_folders(names):
    print(os.getcwd())
    os.chdir('laptop-images')
    for name in names:
        try:
            os.mkdir(name)
        except:
            print(name,'already exists')


if __name__ == '__main__':
    myparser.save_laptop_data_to_csv_table()
    folder_names = get_laptop_producer_names()
    create_producer_folders(folder_names)
    image_processing.start_downloading_images(verbose=True, class_names=folder_names)
    image_processing.preprocess_downloaded_images()
