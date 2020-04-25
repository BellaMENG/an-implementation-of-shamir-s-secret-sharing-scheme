import base64
from split import encrypt_string
import time
import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])

def open_img(file_name):
    with open("images/"+file_name, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
        secret = string.decode("utf-8")
        print(len(secret))


def open_aud(file_name):
    with open("audios/"+file_name,"rb") as audfile:
        string = base64.b64encode(audfile.read())
        secret = string.decode("utf-8")
        print(len(secret))


if __name__ == "__main__":
    open_aud("178.mp3")

