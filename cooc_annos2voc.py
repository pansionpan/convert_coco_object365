from pycocotools.coco import COCO
import os
import shutil
from tqdm import tqdm
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw
import argparse

def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    
    os.makedirs(path)

def id2name(coco):
    classes=dict()
    for cls in coco.dataset['categories']:
        classes[cls['id']]=cls['name']
    return classes


def write_xml(anno_path, objstr, head, objs, tail):
    print("write xml file: ", anno_path)
    with open(anno_path, 'w', encoding='utf-8') as f:
        f.write(head)
        for obj in objs:
            f.write(objstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
        f.write(tail)

def save_annos(img_path, anno_path, filename, objs, headstr, objstr, tailstr):
    img = cv2.imread(img_path)
    if (img.shape[2] == 1):
        print(filename + " not a RGB image")
        return
    # shutil.copy(img_path, dst_imgpath)

    head = headstr % (filename, img.shape[1], img.shape[0], img.shape[2])
    write_xml(anno_path, objstr, head, objs, tailstr)


def create_annos(coco, img_id, cls_map, cls_ids):
    annIds = coco.getAnnIds(imgIds = [img_id], catIds = cls_ids, iscrowd = None)
    anns = coco.loadAnns(annIds)

    print(anns)

    objs = []
    for ann in anns:
        cls_id = ann['category_id']
        if cls_id in cls_ids and 'bbox' in ann:
            bbox = ann['bbox']
            xmin = int(bbox[0])
            ymin = int(bbox[1])
            xmax = int(bbox[2] + bbox[0])
            ymax = int(bbox[3] + bbox[1])
            obj = [cls_map[cls_id], xmin, ymin, xmax, ymax, cls_id]
            objs.append(obj)

    return objs

def main_coco(input_dir, dyear, class_names, output_class, output_dir, headstr, objstr, tailstr):
    for dataset in ["train", "val"]:
        img_dir = os.path.join(input_dir, dataset + dyear)
        anno_dir = os.path.join(output_dir, 'annotations_xml_{}'.format(dataset))
        if not os.path.exists(anno_dir):
            mkr(anno_dir)

        annFile = os.path.join(input_dir, "annotations", "instances_{}{}.json".format(dataset, dyear))

        list_file = os.path.join(output_dir, 'annotations_xml_coco_{}{}.txt'.format(dataset, dyear))

        coco = COCO(annFile)

        #show all classes in coco
        cls_map = id2name(coco)

        #[1, 2, 3, 4, 6, 8]
        cls_ids = coco.getCatIds(catNms = class_names)
        print("class_ids:", cls_ids)

        # accord to the class_id find all images id
        img_ids = []
        for cls_id in cls_ids:
            img_ids.extend(coco.getImgIds(catIds = cls_id))
        img_ids = set(img_ids)
        print("image ids:", img_ids)

        print("list_file:", list_file)
        with open(list_file, 'w', encoding='utf-8') as f:
            for imgId in tqdm(img_ids):
                img = coco.loadImgs(imgId)
                filename = img[0]['file_name']
                img_id = img[0]['id']

                objs = create_annos(coco, img_id, cls_map, cls_ids)

                anno_path = os.path.join(anno_dir, filename[:-3] + 'xml')
                img_path = os.path.join(img_dir, filename)

                save_annos(img_path, anno_path, filename, objs, headstr, objstr, tailstr)

                # write list file
                line = anno_path + "\t" + img_path + "\t"
                if output_class:
                    object_cls_ids = set([str(obj[5]) for obj in objs])
                    print("cls_ids:", object_cls_ids)
                    line += "\t".join(object_cls_ids)

                line += "\n"

                f.write(line)
