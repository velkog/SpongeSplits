from functools import lru_cache
import yaml

SPECIFICATIONS_PATH = 'src/learner/specs.yaml'


# return the specifications yaml
@lru_cache(maxsize=1)
def get_specs():
    with open(SPECIFICATIONS_PATH, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exec:
            return None


# number of epochs
def get_attr_epochs():
    return get_specs()['model']['attributes']['EPOCHS']


# learning rate
def get_attr_lr():
    return get_specs()['model']['attributes']['INIT_LR']


# model batch size
def get_attr_batch_size():
    return get_specs()['model']['attributes']['BATCH_SIZE']


# number of column pixels in images
def get_num_cols():
    return get_specs()['model']['dimensions']['COLS']


# number of row pixels in images
def get_num_rows():
    return get_specs()['model']['dimensions']['ROWS']


# color dimenion: 0 = grayscale, 3 = color
def get_color_dim():
    return get_specs()['model']['dimensions']['COLOR']


# get test train split percentage
def get_train_split():
    return get_specs()['model']['training']['TEST_SIZE']
