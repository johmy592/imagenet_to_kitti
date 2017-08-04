# Creates a dataset in KITTI format from Imagenet data with bounding boxes
# in the PASCALVOC format. 
#
#  NOTE: Only training data is created. If validation data is desired
#        one can for example manually move some label files and 
#        corresponding images to a validation folder. 



import argparse
import sys
import getopt
import os
import shutil

import xml.etree.ElementTree as ET

    

""" Parses the XML-files from the PASCALVOC data and writes .txt label
files in the KITTI format.

NOTE: Only fields used by DIGITS to train a detectnet model are written.
      Other fields are set to 0  
"""
def _parse_xml(root, to_path):
    annotation_path = "%s/Annotations" % (root)
    xml_files = [f for f in os.listdir(annotation_path)]
    for f in xml_files:
        tree = ET.parse("%s/%s" %(annotation_path, f))
        xml_root = tree.getroot()
        size = xml_root.find('size')
        detections = xml_root.findall('object')
        image_name = xml_root.find('filename').text
        text_file = open('%s/%s.%s' % (to_path, image_name, 'txt'), 'w')
        for obj in detections:
            text_file.write(obj.find('name').text)
            text_file.write(' %s' % (obj.find('truncated').text))
            text_file.write(' 0 0 ')
            bbox = obj.find('bndbox')
            text_file.write('%s %s %s %s ' % (bbox.find('xmin').text, bbox.find('ymin').text
                                              ,bbox.find('xmax').text, bbox.find('ymax').text))
            text_file.write("0 0 0 0 0 0 0 0\n")
            text_file.close
        

def _copy_images(root, images_dir):
    img_src = '%s/JPEGImages' % (root)
    image_files = [f for f in os.listdir(img_src)]
    for img in image_files:
        shutil.copy2('%s/%s' % (img_src,img), images_dir)    

def _create_dirs(to_path):
    train_dir = '%s/%s' % (to_path,'train')
    images_dir = '%s/%s' % (train_dir,'images')
    labels_dir = '%s/%s' % (train_dir,'labels')
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
        os.makedirs(images_dir)
        os.makedirs(labels_dir)
    elif not os.path.exists(images_dir) and not os.path.exists(labels_dir):
        os.makedirs(images_dir)
        os.makedirs(labels_dir)

    return labels_dir,images_dir

if __name__ == '__main__':
        
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:t:",["from=","to="])
    except getopt.GetoptError:
        print 'Converter.py -f <from-folder> -t <to-folder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Converter.py -f <from-folder> -t <to-folder> '
            print 'from-folder: root of PASCALVOC data, to-folder: folder where kitti data will be created'
            sys.exit()
        elif opt in('-f','--from'):
            from_path = arg
        elif opt in ('-t', '--to'):
            to_path= arg
    labels_dir, images_dir = _create_dirs(to_path)     
    _parse_xml(from_path, labels_dir)
    _copy_images(from_path, images_dir)    
