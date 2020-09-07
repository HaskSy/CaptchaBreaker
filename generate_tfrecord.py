import os
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple

flags = tf.compat.v1.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('image_dir', '', 'Path to the image directory')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


def class_text_to_int(row_label):
    symbols = "bdfghkmnpqstwxyzABDEFHKLMNPSTWXYZ23456789"
    if row_label in symbols:
        return symbols.index(row_label) + 1


def split(df):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby('filename')
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    path = os.path.join(path, group.filename)
    with tf.io.gfile.GFile(path, 'rb') as bin_img:
        encoded_jpg = bin_img.read()
    image = Image.open(path)
    width, height = image.size
    image.close()

    filename = group.filename.encode('utf8')
    image_format = b'jpeg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'height': dataset_util.int64_feature(height),
        'width': dataset_util.int64_feature(width),
        'filename': dataset_util.bytes_feature(filename),
        'source_id': dataset_util.bytes_feature(filename),
        'encoded': dataset_util.bytes_feature(encoded_jpg),
        'format': dataset_util.bytes_feature(image_format),
        'xmin': dataset_util.float_list_feature(xmins),
        'xmax': dataset_util.float_list_feature(xmaxs),
        'ymin': dataset_util.float_list_feature(ymins),
        'ymax': dataset_util.float_list_feature(ymaxs),
        'text': dataset_util.bytes_list_feature(classes_text),
        'label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples)
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: %s' % output_path)


if __name__ == '__main__':
    tf.compat.v1.app.run()
