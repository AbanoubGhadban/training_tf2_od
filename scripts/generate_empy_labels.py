import argparse
import re
import os
import xml.etree.ElementTree as gfg 

parser = argparse.ArgumentParser(
    description="Sample TensorFlow XML-to-TFRecord converter")
parser.add_argument("-o",
                    "--output_path",
                    help="Path of output of xml files. Default is the same input folder", type=str, default=None)
parser.add_argument("-i",
                    "--image_dir",
                    help="Path to the folder where the input image files are stored. "
                         "Defaults is CWD",
                    type=str, default='.')
args = parser.parse_args()
if args.output_path is None:
    args.output_path = args.image_dir

def GenerateXML(imgpath, fxmlpath) :
      
    root = gfg.Element("annotation")
    root.set('verified', 'yes')
      
    folderEl = gfg.SubElement(root, 'folder')
    folderEl.text = "imgs"

    filenameEl = gfg.SubElement(root, 'filename')
    filenameEl.text = os.path.basename(imgpath)

    pathEl = gfg.SubElement(root, 'path')
    pathEl.text = imgpath

    sourceEl = gfg.SubElement(root, 'source')
    databaseEl = gfg.SubElement(sourceEl, 'database')
    databaseEl.text = 'Unknown'

    sizeEl = gfg.SubElement(root, 'size')
    widthEl = gfg.SubElement(sizeEl, 'width')
    widthEl.text = '640'
    heightEl = gfg.SubElement(sizeEl, 'height')
    heightEl.text = '480'
    depthEl = gfg.SubElement(sizeEl, 'depth')
    depthEl.text = '3'

    segmentedEl = gfg.SubElement(root, 'segmented')
    segmentedEl.text = '0'

    tree = gfg.ElementTree(root)
    with open (fxmlpath, "wb") as f :
        tree.write(f)

def iterate_dir(source, dest):
    source = source.replace('\\', '/')
    dest = dest.replace('\\', '/')

    if not os.path.exists(dest):
        os.makedirs(dest)
    images = [f for f in os.listdir(source)
              if re.search(r'([a-zA-Z0-9\s_\\.\-\(\):])+(.jpg|.jpeg|.png)$', f)]

    for filename in images:
        xml_filename = os.path.splitext(filename)[0]+'.xml'
        fpath = os.path.abspath(os.path.join(source, filename))
        fxmlpath = os.path.abspath(os.path.join(source, xml_filename))
        GenerateXML(fpath, fxmlpath)

iterate_dir(args.image_dir, args.output_path)
