import base64
from split import encrypt_string
import time
import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])


with open("images/lenna.png", "rb") as imageFile:
    string = base64.b64encode(imageFile.read())
    secret = string.decode("utf-8")
    lengths = []
    times = []
    for i in range(1, 11):
        sub_sec = secret[0:10*i]
        t1 = time.time()
        encrypt_string(sub_sec,10,2,8)
        t2 = time.time()
        print("Length: " + str(i*10) + ", time is:", t2-t1)
        lengths.append(i*10)
        times.append(t2-t1)

    plt.plot(lengths, times)
    plt.show()
