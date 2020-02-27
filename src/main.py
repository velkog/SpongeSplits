from video.webcam import Webcam
from keyboard.trigger_listener import TriggerListener
from pynput.keyboard import KeyCode
import cv2
import atexit

from learner.specifications import get_specs

global_counter = -1
spatula_count = 72
thread_webcam = None


def init_keyboard_listener():
    return TriggerListener(KeyCode.from_char('\\'), save_frame_callback,
                           exit_callback)


def init_webcam():
    return Webcam(0)


def save_frame_callback():
    global global_counter
    global_counter += 1
    saved_frame = thread_webcam.get_frame()
    saved_file = "%d-%d.jpg" % (spatula_count, global_counter)
    cv2.imwrite(saved_file, saved_frame)
    print('Frame saved to file %s.' % (saved_file))


def exit_callback():
    print('Exit Callback')
    thread_webcam.exit()


def initialize():
    global_counter = 0
    return init_keyboard_listener(), init_webcam()


if __name__ == '__main__':
    thread_keyboard_listener, thread_webcam = initialize()
    thread_keyboard_listener.start()
    thread_webcam.start()

    thread_keyboard_listener.join()
    thread_webcam.join()
