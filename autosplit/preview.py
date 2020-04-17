"""
compare_ssim
compare_mse
compare_nrmse
"""
from cv2 import imread, resize, INTER_AREA
from skimage.metrics import structural_similarity, mean_squared_error, normalized_root_mse
from time import sleep

from common.video.webcam import Webcam
from common.keyboard.trigger_listener import TriggerListener
from config import Identity

EXIT = False
EXIT_LAMBDA = (lambda: EXIT, )
WEBCAM = Webcam(args=EXIT_LAMBDA, debug=True, input=0, states=[Identity.ALL])
WEBCAM.start()

input("Hit enter to exit. ")
EXIT = True
