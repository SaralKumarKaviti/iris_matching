from flask import Flask, flash, request, redirect, url_for, render_template
import urllib.request
import os
from werkzeug.utils import secure_filename
import cv2
import numpy as np

app = Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image1():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file1 = request.files['file']
    file2 = request.files['file2']
    if file1.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)

    def orb_sim(img1, img2):
        # SIFT is no longer available in cv2 so using ORB
        orb = cv2.ORB_create()

        # 714 x 901 pixels

        # detect keypoints and descriptors
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)

        # define the bruteforce matcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # perform matches.
        matches = bf.match(desc_a, desc_b)
        # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
        similar_regions = [i for i in matches if i.distance < 50]
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    # Needs images to be same dimensions
    npimg = np.fromfile(file1, np.uint8)
    file3 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    npimg = np.fromfile(file2, np.uint8)
    file4 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

@app.route('/upload', methods=['POST'])
def upload_image():
    data_status={"responseStatus":400,"result":""}
    if 'file' not in request.files:
        #flash('No file part')
        data_status["responseStatus"]=400
        data_status["result"]="No file part"
        return data_status

    file1 = request.files['file']
    file2 = request.files['file2']
    if file1.filename == '':
        # flash('')
        data_status["responseStatus"]=400
        data_status["result"]="No image selected for uploading"
        return data_status

    def orb_sim(img1, img2):
        # SIFT is no longer available in cv2 so using ORB
        orb = cv2.ORB_create()

        # 714 x 901 pixels

        # detect keypoints and descriptors
        kp_a, desc_a = orb.detectAndCompute(img1, None)
        kp_b, desc_b = orb.detectAndCompute(img2, None)

        # define the bruteforce matcher object
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        # perform matches.
        matches = bf.match(desc_a, desc_b)
        # Look for similar regions with distance < 50. Goes from 0 to 100 so pick a number between.
        similar_regions = [i for i in matches if i.distance < 50]
        if len(matches) == 0:
            return 0
        return len(similar_regions) / len(matches)

    # Needs images to be same dimensions
    npimg = np.fromfile(file1, np.uint8)
    file3 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    npimg = np.fromfile(file2, np.uint8)
    file4 = cv2.imdecode(npimg, cv2.IMREAD_COLOR)






    orb_similarity = orb_sim(file3, file4)
    if orb_similarity > 0.80:
        data_status["responseStatus"]=200
        data_status["result"]="image is matching"
        data_status["orbSimilarity"]=orb_similarity
        return data_status
        #flash("image is matching")
    else:
        data_status["responseStatus"]=400
        data_status["result"]="image is not matching"
        # data_status["orbSimilarity"]=orb_similarity
        return data_status
        






    return render_template('index.html')





if __name__ == "__main__":
    app.run(debug=True)