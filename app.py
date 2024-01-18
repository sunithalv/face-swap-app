from flask import Flask, render_template, request
import os
import sys

import logging
from face_app.exception import FaceException
from face_app.face_app import FaceApp

logger = logging.getLogger(__name__)

app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'images')
output_path = os.path.join(IMG_FOLDER, 'modified.jpg')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

ROOT = os.getcwd()
source_path = os.path.join(ROOT, 'images', 'src_img.jpg')
dest_path = os.path.join(ROOT, 'images', 'dst_img.jpg')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp', methods = ['GET', 'POST'])
def temp():

    try:
        source_img = request.files['img1']
        destination_img = request.files['img2']

        source_img.save(source_path)
        destination_img.save(dest_path)

        logger.info('Image accepted from user')

        #Call the FaceApp Class 
        face_app = FaceApp(source_path, dest_path, output_path)
        face_app.run()

        display_image = os.path.join(app.config['UPLOAD_FOLDER'], 'modified.jpg')
        return render_template('result.html', user_image=display_image)
    
    except Exception as e:
        raise FaceException(e, sys)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)