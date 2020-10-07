from functools import lru_cache
from yaml import safe_load, YAMLError

SPECIFICATIONS_PATH = "autosplit/image/diglet/specs.yaml"

# TODO: I have no idea why I thought using an LRU cache was a
# better idea than just storing the specs. Probably should change this


# return the specifications yaml
@lru_cache(maxsize=1)
def get_specs():
    with open(SPECIFICATIONS_PATH, 'r') as stream:
        try:
            return safe_load(stream)
        except YAMLError as exec:
            # TODO: this will cause a thread/process to crash, do something smarter
            # or maybe just reraise?
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


def get_datapath():
    return get_specs()['datapath']


# TODO: rename these functions to be more specific
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
