# imagenet_to_kitti
Step by step guide going from downloading imagenet data to having KITTI data ready to be used 
in DIGITS.


1. To download the images I use: https://github.com/dividiti/ck-caffe/tree/master/script/imagenet-downloader 
   in order to get reasonable names of the files.
   Make sure you download from http://www.image-net.org/api/text/imagenet.synset.geturls.getmapping?wnid=n##### 
   in order to get correct mapping between image and wnid

2. Go to the folder with the downloaded datasets and rename: 
   
   `$ rename 's/^0*//' *` 

   to remove 0s in folder names. 
   
3. Use pyrenamer as follows: 
   
   `$ pyrenamer`
   
   Navigate to dataset folder.
   
   Under options: chose an applicable Selection pattern (e.g *.jpg)
   
   Under options: select "Add files recursively"
   
   In "Renamed file name pattern" put: {1}_{dir} 
   
   Click rename
   
   Repeat for all Selection patterns that match your image files.

4. Move files from subdirectories: 
   `$ mv */* .`

5. Create new folders with the following structure:
   
* pascal_root
  * Annotations
  * JPEGImages

   You can name "pascal_root" to whatever you want, just use the same path in the converter later.

6. Move all images to  $PASCAL_ROOT/JPEGImages folder. 

7. Download bbox annotations for your images: http://image-net.org/api/download/imagenet.bbox.synset?wnid=####
   and put the XML files in your $PASCAL_ROOT/Annotations.

8. Create a directory where you want to put your KITTI data, here refered to as $KITTI_ROOT.

9. Run: `$ python converter.py -f $PASCAL_ROOT -t $KITTI_ROOT`

   After this step you should have data ready for training under $KITTI_ROOT. Note that this only creates training data,
   if you want validation data you will have to set this up by yourself by for example manually moving a set of images 
   and corresponding labels to a validation folder.

10. If you are downloading data from imagenet there is a good chance that not all images have bounding boxes labels
    associated with them, and also some of the image downloads will most likely fail. DIGITS requires images and labels
    to match perfectly in order to make a dataset. To resolve this issue, remover.py can be used.

    WARNING: Be careful to put in correct paths and back up you labels/images before running this.
             remover.py will DELETE ALL FILES in <images-path> that dont have a corresponding label file
	     in <labels-path> and vice versa.

    When you have taken this into concideration, you can run: 
    `$ python remover.py -i <images-path> -l <labels-path>`
    
    <images-path> should be like $KITTI_ROOT/train/images/, and <labels-path> $KITTI_ROOT/train/labels/ if you followed
    the steps above.
