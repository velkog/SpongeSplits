from pynput import keyboard


class TriggerListener(keyboard.Listener):
    """
    This class overrides the keyboard.Listener class from the pynput library in 
    order to allow callback triggers from a specified key input.

    :param keyboard.Key trigger_key: Specify which key will trigger event 
    trigger_callback.

    :param function trigger_callback: Specify the callback when the specified
    trigger key is pressed.
    """
    def __init__(self, trigger_key, trigger_callback=None, exit_callback=None):
        self.trigger_key = trigger_key
        self.trigger_callback = trigger_callback
        self.exit_callback = exit_callback
        super(TriggerListener, self).__init__(on_press=self.on_press)

    def on_press(self, key):
        if key == self.trigger_key:
            if self.trigger_callback is not None:
                self.trigger_callback()
        # Close keyboard listener thread on escape
        if key == keyboard.Key.esc:
            if self.exit_callback is not None:
                self.exit_callback()
            return False
