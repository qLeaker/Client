import json
import sys
from rich.console import Console
from classes.imageUtils import ImageUtils
from classes.gmodObject import Gmod
import pyperclip

console = Console()

if __name__ == "__main__":
    console.clear()
    name = console.input("File: ")
    in_file = open(name, "rb")
    fileBytes = in_file.read()
    pyperclip.copy(fileBytes.hex())
    del name
    sys.exit(0)