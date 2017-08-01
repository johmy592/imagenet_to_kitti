import argparse
import sys
import getopt
import os
import shutil

import xml.etree.ElementTree as ET

    


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
            text_file.write('0 0 0 0 0 0 0 0')
            text_file.close
        

if __name__ == '__main__':
    #from_path = sys.argv[1]
    #to_path = sys.argv[2]
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hf:t:",["from=","to="])
    except getopt.GetoptError:
        print 'Converter.py -f <from-folder> -t <to-folder>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Converter.py -f <from-folder> -t <to-folder> '
            print 'from-folder: root of PASCALVOC data, to-folder: where kitti label files should be written'
            sys.exit()
        elif opt in('-f','--from'):
            from_path = arg
        elif opt in ('-t', '--to'):
            to_path= arg
   
    _parse_xml(from_path, to_path)    
