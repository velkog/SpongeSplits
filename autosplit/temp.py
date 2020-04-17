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

EXIT = False
EXIT_LAMBDA = (lambda: EXIT, )
WEBCAM = Webcam(args=EXIT_LAMBDA, input=0, debug=True)
WEBCAM.start()

imageA = imread("autosplit/res/original/key_frames/reset_frame.jpg")
imageB = imread("autosplit/res/original/key_frames/start_frame.jpg")

scale_percent = 20  # percent of original size
width = int(imageA.shape[1] * scale_percent / 100)
height = int(imageA.shape[0] * scale_percent / 100)

imageA = resize(imageA, (height, width), interpolation=INTER_AREA)
imageB = resize(imageB, (height, width), interpolation=INTER_AREA)

while True:
    try:
        frame = WEBCAM.get_frame()
        frame = resize(frame, (height, width), interpolation=INTER_AREA)
        if frame is None:
            continue
        scoreA = structural_similarity(imageA, frame, multichannel=True)
        scoreB = mean_squared_error(imageA, frame)
        scoreC = normalized_root_mse(imageA, frame)
        if scoreC < 0.075:
            print("\n-----Comparing RESET frame-----")
            print("SSIM Score='%s'" % (str(scoreA)))
            print("MSE Score='%s'" % (str(scoreB)))
            print("NRMSE Score='%s'" % (str(scoreC)))

        scoreA = structural_similarity(imageB, frame, multichannel=True)
        scoreB = mean_squared_error(imageB, frame)
        scoreC = normalized_root_mse(imageB, frame)
        if scoreC < 0.075:
            print("\n-----Comparing START frame-----")
            print("SSIM Score='%s'" % (str(scoreA)))
            print("MSE Score='%s'" % (str(scoreB)))
            print("NRMSE Score='%s'" % (str(scoreC)))
        sleep(0.005)
    except:
        EXIT = False

EXIT = False
