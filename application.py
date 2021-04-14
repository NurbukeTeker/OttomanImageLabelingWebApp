import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from keras.models import Sequential, load_model
from werkzeug.utils import secure_filename
import numpy as np

from PIL import Image
import pytesseract
import argparse
import cv2
import os

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])
IMAGE_SIZE = (224, 224)
UPLOAD_FOLDER = 'uploads'


from ImageClass import Imageclass
global current_image
current_image = Imageclass("")
counter = current_image.counter

def resetImage():
    write_to_file()
    current_image = Imageclass("")
    counter = current_image.counter
    current_image.counter = counter+1
    return 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def write_to_file():
    f = open("1.txt","a" ,encoding='utf-8')

    # f = open("static/1.txt".format(current_image.id),"w" ,encoding='utf-8')
    # output = ["ImagePath:", current_image.name,"ImageLabel:", current_image.newlabel]
    output = str( current_image.newlabel)
    f.write(str(output))
    f.write("\n")
    f.close()
    return 

def check_text(line):
    characters = ["x","w","0","1","2","3","4","5","6","7","8","9","\\","\/"]
    for char in characters:
        if char  in  line:
            # print(char)
            return False     
    return True


def predictionImageOttoman(image):
    image = cv2.resize(image, None, fx=0.3, fy=0.3)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
#    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#    gray = cv2.medianBlur(gray, 3)
    config = "--psm 3"

    filename = "static/{}.tif".format(current_image.id)
    cv2.imwrite(filename, adaptive_threshold)
    
    pytesseract.pytesseract.tesseract_cmd = 'tesseract'
    text = pytesseract.image_to_string(Image.open(filename),lang='ara',config=config)
    text = text.split("\n")
    # print("text:  ",text)

    output = []
    for  i in text:
        if (i != '') and (i != '\x0c')  :
            i = str(i)
            # print(i)


            output.append(i)
            
#    text = ''.join(output)
#    print(text)
#    return str(text)
    
    return output


def predict(file):
    image = cv2.imread(file)
    # print(image)    
    prediction = predictionImageOttoman(image)
    output =  prediction

    return output

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/handle_data', methods=['POST'])
def handle_data():
    paragraph_text = request.form['paragraph_text']
    print("paragraph_text",paragraph_text)
    current_image.newLabel(paragraph_text)
    resetImage()
    return redirect(url_for('template_test'))

#    return render_template("home.html", label=current_image.prediction, imagesource=current_image.name)



@app.route('/approve', methods=['POST'])
def approve():
    if "approve" in request.form:
          current_image.approved = True
          current_image.newlabel = current_image.prediction
          print("Onay verildi")
          print(current_image.name,current_image.approved )
    resetImage()
    return redirect(url_for('template_test'))
#    return render_template("home.html",  label=current_image.prediction, imagesource=current_image.name)


    
@app.route("/")
def template_test():
    resetImage()
    return render_template('home.html', label='', imagesource='file://null')


@app.route('/', methods=['POST'])
def upload_file():
    # print("HERREEE")
    if request.method == 'POST':
        file = request.files['file']
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            current_image.nameImage(file_path,counter)
            output = predict(file_path)
            current_image.labelImage(output)
            print(current_image.name,current_image.prediction )
            
            if  ' ' in output :
                output.remove(' ')
                if output == []:
                    output.append("Bulunamadı")
            if output == []:
                    output.append("Bulunamadı")
            print("OUTPUT:",output)
    return render_template("home.html", label=output, imagesource=file_path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port= '5009',debug=True, threaded=False)
#    app.run(host = '192.168.1.38', port= '5000')