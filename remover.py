import os
import sys
import getopt

def _get_noext_names(images_path, labels_path):
    images_noext = os.listdir(images_path)
    labels_noext = os.listdir(labels_path)
    
    for i in range(len(labels_noext)):
        labels_noext[i] = labels_noext[i].replace('.txt','')

    for i in range(len(images_noext)):
        images_noext[i] = images_noext[i].replace('.jpg','')
        images_noext[i] = images_noext[i].replace('.png','')
        images_noext[i] = images_noext[i].replace('.gif','')

    return images_noext, labels_noext

def remove_images(images_noext, labels_noext, images, path):
    for i in range(len(images_noext)):
        if(images_noext[i] not in labels_noext):
            os.remove('%s/%s' % (path,images[i]))

def remove_labels(images_noext, labels_noext, labels, path):
    for i in range(len(labels_noext)):
        if(labels_noext[i] not in images_noext):
            os.remove('%s/%s' % (path,labels[i]))


if __name__ == '__main__':
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:l:",["images=","labels="])
    except getopt.GetoptError:
        print 'Remover.py -i <images-path> -l <labels-path>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == 'h':
            print 'Remover.py -i <images-path> -l <labels-path>'
            print 'Will DELETE ALL FILES in image directory with no matching label file and vice versa'
        elif opt in('-i','--images'):
            images_path = arg
        elif opt in('-l','--labels'):
            labels_path = arg
    
    images = os.listdir(images_path)
    labels = os.listdir(labels_path)
    images_noext, labels_noext = _get_noext_names(images_path, labels_path)
    
    u_input = raw_input("WARNING: This will DELETE ALL FILES in %s that don't have a matching label file in %s and vice versa. Continue? (yes/no): " % (images_path, labels_path))
    
    if not u_input == 'yes':
        print("Aborting")
        sys.exit()
 
    remove_images(images_noext, labels_noext, images, images_path)
    remove_labels(images_noext, labels_noext, labels, labels_path)
