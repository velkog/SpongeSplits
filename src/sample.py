from video.webcam import Webcam
from keyboard.trigger_listener import TriggerListener
from pynput.keyboard import KeyCode


def init_keyboard_listener():
    return TriggerListener(KeyCode.from_char('\\'), save_frame_callback)


def init_webcam():
    return Webcam(0)


def save_frame_callback():
    print('Enter Callback')


# Initialize Start and Join: keyboard listener and webcam threads
def initialize_start_and_join():
    thread_keyboard_listener = init_keyboard_listener()
    thread_webcam = init_webcam()

    thread_keyboard_listener.start()
    thread_webcam.start()

    thread_keyboard_listener.join()
    thread_webcam.join()


if __name__ == '__main__':
    initialize_start_and_join()
