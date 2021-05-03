import os
import numpy as np

# tf Keras
import tensorflow as tf
from tensorflow.keras.applications.imagenet_utils import preprocess_input, decode_predictions
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class FixedDropout(tf.keras.layers.Dropout):
  def _get_noise_shape(self, inputs):
    if self.noise_shape is None:
        return self.noise_shape
    symbolic_shape = K.shape(inputs)
    noise_shape = [symbolic_shape[axis] if shape is None else shape for axis, shape in enumerate(self.noise_shape)]
    return tuple(noise_shape)

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from tensorflow.python.keras.backend import dtype
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

model=None

def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(512,512))

    # Preprocessing the image
    x = image.img_to_array(img)
    x = x.astype("float") / 255.0
    x = np.expand_dims(x,0)
    # print(x.shape)

    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)

        os.remove(file_path)

        # Process your result for human
        pred_class = preds.argmax(axis=-1)
        if preds[0][0]>=0.5:
            return "Melanoma Lesion"
        else:
            return "Non-Melanoma Lesion"
    return None


if __name__ == '__main__':
    model=load_model('new.h5',custom_objects={'FixedDropout':FixedDropout},compile=False)
    #just need to change the model if it is efficientnet trained on tpu add custom objects code 
    # app.run(host="0.0.0.0", port=5000, debug=True)
    http_server=WSGIServer(('0.0.0.0',5000),app)
    http_server.serve_forever()

