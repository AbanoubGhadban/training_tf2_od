import tensorflow as tf
import argparse
# Define model and output directory arguments
parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Folder that the saved model is located in',
                    default='exported-models/my_tflite_model/saved_model')
parser.add_argument('--output', help='Folder that the tflite model will be written to',
                    default='exported-models/my_tflite_model')
args = parser.parse_args()

rep_ds = tf.data.Dataset.list_files("H:\datasets\export\*.jpg")
HEIGHT, WIDTH = 320, 320


def representative_dataset_gen():
    i = 0
    for image_path in rep_ds:
        img = tf.io.read_file(image_path)
        img = tf.io.decode_image(img, channels=3)
        img = tf.image.convert_image_dtype(img, tf.float32)
        resized_img = tf.image.resize(img, (HEIGHT, WIDTH))
        resized_img = resized_img[tf.newaxis, :]
        yield [resized_img]
        i += 1
        if i == 100:
            break


converter = tf.lite.TFLiteConverter.from_saved_model(args.model)
#converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model('exported-models/my_tflite_model/saved_model')
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.allow_custom_ops = True
converter.representative_dataset = representative_dataset_gen
# converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8  # or tf.int8
converter.inference_output_type = tf.uint8  # or tf.int8
tflite_model = converter.convert()

output = args.output + '/model.tflite'
with tf.io.gfile.GFile(output, 'wb') as f:
    f.write(tflite_model)
