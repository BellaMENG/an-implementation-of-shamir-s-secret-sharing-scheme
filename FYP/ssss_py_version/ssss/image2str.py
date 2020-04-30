import base64
from split import encrypt_string
import time
# plt.plot([1, 2, 3, 4])

def open_img(file_name):
    with open(file_name, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
        secret = string.decode("utf-8")
        print(len(secret))
        return secret


def open_aud(file_name):
    with open(file_name,"rb") as audfile:
        string = base64.b64encode(audfile.read())
        secret = string.decode("utf-8")
        print(len(secret))
        return secret


def str2aud(string):
    fh = open("/Users/zmeng/Documents/FYP/ssss_py_version/ssss/static/combine" + "/aud.mp3", "wb")
    fh.write(base64.b64decode(string))
    fh.close()
    return fh


if __name__ == "__main__":
    string = open_aud("/Users/zmeng/Documents/FYP/ssss_py_version/ssss/static/secrets/2514.mp3")
    str2aud(string)

