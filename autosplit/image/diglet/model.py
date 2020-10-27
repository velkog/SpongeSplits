from keras.layers import Activation, Conv2D, Dense, Flatten, MaxPooling2D
from keras.models import Sequential
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from numpy import ndarray
from typing import NamedTuple, List

from image.frame import SpongeFrame
from image.diglet.specifications import (
    get_attr_batch_size,
    get_attr_epochs,
    get_attr_lr,
    get_color_dim,
    get_num_cols,
    get_num_rows,
)


class Prediction(NamedTuple):
    label: int
    probability: float

    @classmethod
    def build(cls, prediction: ndarray):
        label = prediction.argmax(axis=-1).flat[0]
        probability = prediction.flat[label]
        # TODO: clean up this logic
        label = None if label == 83 else label
        return cls(label, probability * 100)


class CnnModel:
    def __init__(self, num_classes: int):
        model = Sequential()
        input_shape = self.__get_input_shape()
        self.compile = False  # TODO: fix this and actually save and load the model

        # Input layer
        num_filters = get_num_cols() * get_num_rows() * 3
        model.add(Conv2D(64, (3, 3), padding="same", input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Convolutional layer
        model.add(Conv2D(8, (3, 3)))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2)))

        # Flatten
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # Reduce to number of classes
        model.add(Dense(num_classes))
        model.add(Activation("softmax"))

        print(model.summary())
        self.model = model

    def __get_input_shape(self):
        return get_num_rows(), get_num_cols(), get_color_dim()

    def __get_optimizer(self):
        return Adam(lr=get_attr_lr(), decay=get_attr_lr() / get_attr_epochs())

    def __save_model(self):
        # TODO: save model to be loaded later
        return

    def compile_model(self, loss="binary_crossentropy"):
        self.compile = True
        self.model.compile(
            loss="binary_crossentropy",
            optimizer=self.__get_optimizer(),
            metrics=["accuracy"],
        )

    def fit_model(self, image_set):
        if self.compile == False:
            self.compile_model()
        train_x, train_y, val_x, val_y = image_set.get_dataset()
        self.model.fit_generator(
            ImageDataGenerator().flow(
                train_x,
                train_y,
                batch_size=get_attr_batch_size()
            ),
            validation_data=(val_x, val_y),
            steps_per_epoch=len(train_x) // get_attr_batch_size(),
            epochs=get_attr_epochs(),
            verbose=1,
        )

    # TODO: returning a list here is dumb
    def predict(self, frame: SpongeFrame) -> Prediction:
        spatula = frame.spatula_array
        spatula_prediction = self.model.predict(
            spatula, batch_size=get_attr_batch_size(),
        )
        # sock = frame.sock_array(375, 525)
        # sock_prediction = self.model.predict(
        #     sock,
        #     batch_size=get_attr_batch_size(),
        # )
        return Prediction.build(spatula_prediction)

    @staticmethod
    def gen_model():
        # TODO: load saved cnn model
        return None
