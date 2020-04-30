from flask import Flask, render_template, request, jsonify
from utilitybelt import secure_randint as randint
import os
import base64
from werkzeug.utils import secure_filename
import sys
sys.path.insert(1,"/Users/zmeng/Documents/FYP/ssss_py_version/ssss/cpp_code/build/lib.macosx-10.9-x86_64-3.8/")
from fetch_data import fetch_shares, fetch_secret, fetch_shares_arr
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# import matplotlib.pyplot as plt
# import io
# from flask import send_file, send_from_directory, safe_join, abort

#TODO:
'''
1. check validity of inputs
 1.1 field_base/k/n should be integers
 1.2 secret should be a string
 1.3 number of shares while combining
 1.4 whether the shares format is legal
'''

# UPLOAD_FOLDER = '/Users/zmeng/Documents/FYP/ssss_py_version/ssss/images/'
UPLOAD_FOLDER = os.path.join('static', 'secrets')
SHARE_FOLDER = os.path.join('static', 'shares')
COMBINE_FOLDER = os.path.join('static', 'combine')
UPPER_BOUND = 2**16
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SHARE_FOLDER'] = SHARE_FOLDER
app.config['COMBINE_FOLDER'] = COMBINE_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text_secrets')
def text_secrets():
    # print("in views.py text_secrets()")
    return render_template('text_secrets.html')

@app.route('/image_secrets')
def image_secrets():
    return render_template('image_secrets.html')


@app.route('/img_split', methods=['POST'])
def img_split():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    secret = image2str(filename)
    shares = fetch_shares_arr(secret, 10, 2)
    print(len(shares))
    img_shares = []
    for i in range(len(shares)):
        img_share = save_str2file(shares[i],i)
        img_shares.append(img_share)

    return jsonify(file_path)


@app.route('/img_combine')
def img_combine():
    path = os.path.join(SHARE_FOLDER)
    fp0 = path+'/'+str(0)+".txt"
    fp1 = path + '/' + str(1) + ".txt"
    fp2 = path + '/' + str(2) + ".txt"
    fp3 = path + '/' + str(3) + ".txt"
    fp4 = path + '/' + str(4) + ".txt"
    fp5 = path + '/' + str(5) + ".txt"
    fp6 = path + '/' + str(6) + ".txt"
    fp7 = path + '/' + str(7) + ".txt"
    fp8 = path + '/' + str(8) + ".txt"
    fp9 = path + '/' + str(9) + ".txt"
    return render_template('img_combine.html', fp0=fp0, fp1=fp1, fp2=fp2, fp3=fp3, fp4=fp4, fp5=fp5, fp6=fp6, fp7=fp7, fp8=fp8, fp9=fp9)


@app.route('/img_combine_c', methods=['POST'])
def combine_action():
    file = request.files['file0']
    filename = secure_filename(file.filename)
    fp0 = os.path.join(app.config['COMBINE_FOLDER'], filename)
    file.save(fp0)
    file = request.files['file1']
    filename = secure_filename(file.filename)
    fp1 = os.path.join(app.config['COMBINE_FOLDER'], filename)
    file.save(fp1)
    file = request.files['file2']
    filename = secure_filename(file.filename)
    fp2 = os.path.join(app.config['COMBINE_FOLDER'], filename)
    file.save(fp2)
    print(filename)
    shares = []
    shares.append(read_file(fp0))
    shares.append(read_file(fp1))
    shares.append(read_file(fp2))

    secret = fetch_secret(shares, 2)
    random_int = randint(1, UPPER_BOUND)
    fp = os.path.join(app.config['COMBINE_FOLDER'], str(random_int) + ".jpg")
    if os.path.exists(fp):
        os.remove(fp)
        random_int = randint(1, UPPER_BOUND)
        fp = os.path.join(app.config['COMBINE_FOLDER'], str(random_int) + ".jpg")
    fh = open(fp, "wb")
    fh.write(base64.b64decode(secret))
    fh.close()
    print(fp)
    return jsonify(fp)


@app.route('/split', methods=['POST'])
def text_split():
    secret = request.form.getlist('secret')[0]
    intercept = int(request.form.getlist('intercept')[0])
    degree = int(request.form.getlist('degree')[0]) - 1
    field_base = int(request.form.getlist('field_base')[0])
    shares = fetch_shares(secret, intercept, degree)
    return jsonify(shares)


@app.route('/combine', methods=['POST'])
def text_combine():
    degree = int(request.form.getlist('degree')[0]) - 1
    field_base = int(request.form.getlist('field_base')[0])
    shares = request.form.getlist('shares')[0].split('\n')
    secret = fetch_secret(shares, degree)
    print(secret)
    return jsonify(secret)


@app.route('/aud_secrets')
def aud_secrets():
    return render_template('aud_secrets.html')


def image2str(filename):
    path = os.path.join(UPLOAD_FOLDER)
    with open(path+'/'+filename, "rb") as imageFile:
        string = base64.b64encode(imageFile.read())
        secret = string.decode("utf-8")
        print(len(secret))
        return secret


def str2img(string,x):
    path = os.path.join(SHARE_FOLDER)
    fh = open(path+'/'+str(x)+".jpg", "wb")
    fh.write(base64.b64decode(string))
    fh.close()
    return path+str(x)+".jpg"


def save_str2file(string, x):
    path = os.path.join(SHARE_FOLDER)
    fp = path + '/' + str(x) + ".txt"
    fh = open(fp, "w")
    fh.write(string)
    fh.close()
    return fp


def read_file(fp):
    with open(fp, "r") as file:
        return file.readline()


def test_img():
    str2img(image2str("qrls.jpg"))


def get_share(share):
    return share.split("-")[1]


if __name__ == "__main__":
    app.run()

