class SpongeFrame():

    def __init__(self, frame):
        self.spatula = frame[45:85, 325:380]
        self.sock = frame[380:420, 530:585]

    def get_spatula_img(self):
        return self.spatula
