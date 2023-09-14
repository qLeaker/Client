import urllib.request


class ImageUtils:
    @staticmethod
    def imageFromUrl(url: str) -> bytes:
        return urllib.request.urlopen(url).read()

    @staticmethod
    def imageFromHex(hex: str) -> bytes:
        return bytes.fromhex(hex)