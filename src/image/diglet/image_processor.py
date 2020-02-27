import cv2
import numpy as np
import os
from keras.utils import to_categorical
from keras.preprocessing.image import img_to_array
from sklearn.model_selection import train_test_split

from image.diglet.specifications import get_train_split, get_color_dim, get_num_cols, get_num_rows


class ImageSet():

    def __init__(self):
        self.class_labels = set()
        self.__generate_dataset()

    def __generate_dataset(self):
        data_x, data_y = self.__process_images()
        self.train_x, self.val_x, self.train_y, self.val_y = train_test_split(
            data_x, data_y, test_size=get_train_split())

        self.train_y = to_categorical(self.train_y,
                                      num_classes=len(self.class_labels))
        self.val_y = to_categorical(self.val_y,
                                    num_classes=len(self.class_labels))

    def __process_images(self):
        data_x, data_y = [], []
        list_of_images = self.__retrieve_dataset()

        for image_file in list_of_images:
            image = cv2.imread(image_file, get_color_dim())[45:85, 325:380]
            image = cv2.resize(image, (get_num_cols(), get_num_rows()),
                               interpolation=cv2.INTER_CUBIC)
            image = img_to_array(image)

            data_x.append(image)
            label = int(image_file.split('-')[0][-1])
            self.class_labels.add(label)
            data_y.append(int(image_file.split('-')[0][-1]))

        data_x = np.array(data_x, dtype='float') / 255.0
        data_y = np.array(data_y)

        return data_x, data_y

    def __retrieve_dataset(self):
        list_of_images = []
        for filename in os.listdir('dataset/'):
            if filename.endswith('.jpg'):
                list_of_images.append('dataset/%s' % (filename))
        return list_of_images

    def get_dataset(self):
        return self.train_x, self.train_y, self.val_x, self.val_y

    def get_num_classes(self):
        return len(self.class_labels)
