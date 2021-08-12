import os
from tensorflow import keras
import skimage
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from keras.models import load_model
from keras.preprocessing import image
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt
app = Flask(__name__)
model = load_model('model/cnn.h5',compile=False)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
dict={0:'airplane',1:'automobile',2:'bird',3:'cat',4:'deer',5:'dog',6:'frog',7:'horse',8:'ship',9:'truck'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    if(request.method=='POST'):
        if  request.files['image']==" ":
    
            return redirect('/')
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect("/")
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # i = image.load_img("static/images/"+filename)
            image=plt.imread("static/images/"+filename)
            resized_image=resize(image,(32,32,3))
            x_t=np.array(resized_image)
            x_t=x_t.reshape(-1,32,32,3)


            # i = image.img_to_array(i)/255.0
            # i = i.reshape(1, 32,32,3)
            name=model.predict(x_t)
            index=np.argmax(name)
            print(dict[index])
            result={'result' :dict[index],
            'image':filename}


        
    return render_template("result.html",result = result)

@app.route("/result")
def result():
    return render_template('result.html')





if __name__ == "__main__":
    app.run(debug=True)
