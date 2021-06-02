#imports
import os
import numpy as np
# tf Keras
import tensorflow as tf
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from tensorflow.python.keras.backend import dtype
from werkzeug.utils import secure_filename
# from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

model=None

def model_predict(img_path, interpreter):
    img = image.load_img(img_path, target_size=(500,500))

    # Preprocessing the image
    inp_tensor = image.img_to_array(img,dtype=np.float32)
    inp_tensor = inp_tensor / 255.0 #normailizing the image between [0-255]
    inp_tensor = np.expand_dims(inp_tensor,0) #adding batch size of 1 to get shape (1,img_height,img_width,channels=3)
    # print(x.shape)

    input_index = interpreter.get_input_details()[0]["index"]
    interpreter.set_tensor(input_index, inp_tensor)
    interpreter.invoke()
    output_details = interpreter.get_output_details()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    # print(results)
    return results


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
        preds = model_predict(file_path, interpreter)

        os.remove(file_path)
        if preds>=0.5:
            return "Melanoma Lesion"#+"\nconfidence :"+format(preds[0][0]*100,'.2f')+"%"
        else:
            return "Non-Melanoma Lesion"#+"\nconfidence :"+format(preds[0][0]*100,'.2f')+"%"
    return None


if __name__ == '__main__':
    interpreter=tf.lite.Interpreter('model.tflite')
    interpreter.allocate_tensors()
    inputs=interpreter.get_input_details()
    outputs = interpreter.get_output_details()
    #just need to change the model if it is efficientnet trained on tpu add custom objects code 
    app.run(host="0.0.0.0", port=5000, debug=True)
    # http_server=WSGIServer(('0.0.0.0',5000),app)
    # http_server.serve_forever()

