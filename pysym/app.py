from flask import Flask, render_template, request, send_from_directory
import os
import random
import string
app = Flask(__name__)
app.config['UPLOAD_FOLDER']='uploads'
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/',methods=['POST'])
def POST():
    if 'file' not in request.files:
        return 'No file uploaded.'
    file = request.files['file']
    if file.content_length > 10240:
        return 'file too lager'
    path = ''.join(random.choices(string.hexdigits, k=16))
    directory = os.path.join(app.config['UPLOAD_FOLDER'], path)
    os.makedirs(directory, mode=0o755, exist_ok=True)
    savepath=os.path.join(directory, file.filename)
    file.save(savepath)
    try:
     os.system('tar --absolute-names  -xvf {} -C {}'.format(savepath,directory))
    except:
        return 'something wrong in extracting'

    links = []
    for root, dirs, files in os.walk(directory):
        for name in files:
            extractedfile =os.path.join(root, name)
            if os.path.islink(extractedfile):
                os.remove(extractedfile)
                return 'no symlink'
            if  os.path.isdir(path) :
                return 'no directory'
            links.append(extractedfile)
    return render_template('index.html',links=links)
@app.route("/uploads/<path:path>",methods=['GET'])
def download(path):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], path)
    if not os.path.isfile(filepath):
        return '404', 404
    return send_from_directory(app.config['UPLOAD_FOLDER'], path)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=1337)