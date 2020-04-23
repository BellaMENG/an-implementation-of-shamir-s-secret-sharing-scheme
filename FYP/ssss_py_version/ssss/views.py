# print("You reached the test file.")

from flask import Flask, render_template, request, jsonify
from werkzeug.datastructures import ImmutableMultiDict
from split import encrypt_string_str
from interpolation import reconstruct_secret


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
    shares = encrypt_string_str(secret, intercept, degree, field_base)
    return jsonify(shares)


@app.route('/combine', methods=['POST'])
def text_combine():
    degree = int(request.form.getlist('degree')[0]) - 1
    field_base = int(request.form.getlist('field_base')[0])
    shares = request.form.getlist('shares')[0].split('\n')
    secret = reconstruct_secret(shares, degree, field_base)
    print(secret)
    return jsonify(secret)


if __name__ == "__main__":
    app.run()

