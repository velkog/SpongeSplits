from keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from learner.image_processor import ImageSet
from learner.specifications import get_attr_batch_size, get_attr_epochs, get_attr_lr, get_color_dim, get_num_cols, get_num_rows


class CnnModel():

    def __init__(self, num_classes):
        model = Sequential()
        input_shape = self.__get_input_shape()
        self.compile = False

        # Input layer
        model.add(Conv2D(32, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Convolutional layer
        model.add(Conv2D(32, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Flatten
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # Reduce to number of classes
        model.add(Dense(num_classes))
        model.add(Activation("softmax"))

        self.model = model

    def __get_input_shape(self):
        return get_num_rows(), get_num_cols(), get_color_dim()

    def __get_optimizer(self):
        return Adam(lr=get_attr_lr(), decay=get_attr_lr() / get_attr_epochs())

    def compile_model(self, loss='binary_crossentropy'):
        self.compile = True
        self.model.compile(loss='binary_crossentropy',
                           optimizer=self.__get_optimizer(),
                           metrics=['accuracy'])

    def fit_model(self, image_set):
        if self.compile == False:
            self.compile_model()
        train_x, train_y, val_x, val_y = image_set.get_dataset()
        self.model.fit_generator(
            ImageDataGenerator().flow(train_x,
                                      train_y,
                                      batch_size=get_attr_batch_size()),
            validation_data=(val_x, val_y),
            steps_per_epoch=len(train_x) // get_attr_batch_size(),
            epochs=get_attr_epochs(),
            verbose=1)
