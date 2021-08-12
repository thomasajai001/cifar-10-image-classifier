import os
from flask import Flask, request, redirect, render_template
from werkzeug.utils import secure_filename
from keras.models import load_model
from skimage.transform import resize
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
model = load_model("model/cnn.h5", compile=False)

UPLOAD_FOLDER = "static"
ALLOWED_EXTENSIONS = set(["txt", "pdf", "png", "jpg", "jpeg", "gif"])

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
dict = {
    8: "ship",
    9: "truck",
}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if request.method == "POST":
        if request.files["image"] == " ":
            return redirect("/")
        file = request.files["image"]
        if file.filename == "":
            return redirect("/")
        try:
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                image = plt.imread("static/" + filename)
                resized_image = resize(image, (32, 32, 3))
                x_t = np.array(resized_image)
                x_t = x_t.reshape(-1, 32, 32, 3)
                name = model.predict(x_t)
                index = np.argmax(name)
                print(dict[index])
                if index >7:
                    result = {"image": filename, "result": dict[index]}
                else:
                    index = 8 + index % 2
                    result = {"image": filename, "result": dict[index]}
        except (IOError, SyntaxError) as e:
            result = {"error": "Corrupt Image"}

    return render_template("result.html", result=result)


@app.route("/result")
def result():
    return render_template("result.html")


if __name__ == "__main__":
    app.run(debug=True)
