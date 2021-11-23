
class ErrorHandling:

    def __init__(self, err, message, data=None):
        super(ErrorHandling, self).__init__()
        self.err = err
        self.message = message
        self.data = data