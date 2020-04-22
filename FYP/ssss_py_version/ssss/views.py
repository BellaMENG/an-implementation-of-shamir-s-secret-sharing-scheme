# print("You reached the test file.")

from flask import Flask, render_template, request
from werkzeug.datastructures import ImmutableMultiDict
from split import encrypt_string_str


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


@app.route('/split', methods=['GET','POST'])
def text_split():
    if request.method == 'POST':
        secret = request.form.getlist('secret')[0]
        intercept = int(request.form.getlist('intercept')[0])
        degree = int(request.form.getlist('degree')[0]) - 1
        field_base = int(request.form.getlist('field_base')[0])

        shares = encrypt_string_str(secret, intercept, degree, field_base)
        return shares
    if request.method == 'GET':
        return render_template('text_split.html')
    # return render_template('text_split.html')


if __name__ == "__main__":
    app.run()

