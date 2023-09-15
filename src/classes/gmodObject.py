class Gmod(object):
    def __init__(self, name: str, version: str, image, file: str, store: str, content: str):
        self.name = name
        self.version = version
        self.image = image
        self.file = file
        self.store = store
        self.content = content