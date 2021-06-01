import tensorflow as tf
from tensorflow.keras import backend as K

class FixedDropout(tf.keras.layers.Dropout): # for tpu trained model to work in cpu for deployment
  def _get_noise_shape(self, inputs):
    if self.noise_shape is None:
        return self.noise_shape
    symbolic_shape = K.shape(inputs)
    noise_shape = [symbolic_shape[axis] if shape is None else shape for axis, shape in enumerate(self.noise_shape)]
    return tuple(noise_shape)

model=tf.keras.models.load_model('b6structure.h5',custom_objects={'FixedDropout':FixedDropout},compile=False)

converter=tf.lite.TFLiteConverter.from_keras_model(model)

converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
tflite_quant_model = converter.convert()

with open('model.tflite', 'wb') as f:
  f.write(tflite_quant_model)
