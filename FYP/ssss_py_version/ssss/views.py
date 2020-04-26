# print("You reached the test file.")
from flask import Flask, render_template, request, jsonify
from split import encrypt_string_str
from interpolation import reconstruct_secret
import sys
sys.path.insert(1,"/Users/zmeng/Documents/FYP/ssss_py_version/ssss/cpp_code/build/lib.macosx-10.9-x86_64-3.8/")
from fetch_data import fetch_shares, fetch_secret

#TODO:
'''
1. check validity of inputs
 1.1 field_base/k/n should be integers
 1.2 secret should be a string
 1.3 number of shares while combining
 1.4 whether the shares format is legal
'''

app = Flask(__name__)


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
    secret = reconstruct_secret(shares, degree, field_base)
    # secret = fetch_secret(shares, degree)
    print(secret)
    return jsonify(secret)




if __name__ == "__main__":
    app.run()

