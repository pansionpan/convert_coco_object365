import json
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import cv2
import shutil
import os
import subprocess
import argparse
import glob
from tqdm import tqdm

"""
提取每个图片对应的category与bbox值，写入json然后转成需要的VOC格式
"""

# cellphone:79 key:266 handbag:13 laptop:77
classes_names = {79: "cellphone", 266: "key", 13: "handbag", 77: "laptop"}

def save_annotations(anno_file_path, imgs_file_path, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset):
    # open json file(val.json or train.json)
    with open(anno_file_path, 'r') as f:
        data = json.load(f)
        print("提取长度:", len(data["annotations"]))
        # iterate all annotations imformation
        for i in range(0, len(data["annotations"])):
            # check category class whether in the classes list
            if data["annotations"][i]["category_id"] in classes_names.keys():
                # find the image id which class meet the confitions
                class_imgs_id = data["annotations"][i]["image_id"]
                print("class_imgs_id:", class_imgs_id)
                for j in range(0, len(data["images"])):
                    objs = []
                    if class_imgs_id == data["images"][j]["id"]:
                        print(data["images"][j]["file_name"])
                        # img_path use to find the image path
                        img_path = os.path.join(imgs_file_path, data["images"][j]["file_name"])
                        # bbox
                        bbox = data["annotations"][i]["bbox"]
                        xmin = int(bbox[0])
                        ymin = int(bbox[1])
                        xmax = int(bbox[2] + bbox[0])
                        ymax = int(bbox[3] + bbox[1])
                        class_name = classes_names.get(int(data["annotations"][i]["category_id"]))
                        obj = [class_name, xmin, ymin, xmax, ymax, class_name]
                        objs.append(obj)

                        img_name = os.path.basename(img_path)
                        save_head(objs, img_name, img_path, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset)

    print(" 提取完成 ")


def mkr(path):
    if os.path.exists(path):
        shutil.rmtree(path)

    os.makedirs(path)

def write_txt(output_dir, anno_path, img_path, dataset):
    list_name = output_dir + '/annotations_xml_object_{}.txt'.format(dataset)
    if not os.path.exists(list_name):
        with open(list_name, 'w', encoding="utf=8") as fs:
            print(fs)
    with open(list_name, 'r', encoding='utf-8') as list_fs:
        with open(list_name, 'a+', encoding='utf-8') as list_f:
            lines = anno_path + "\t" + img_path + "\n"
            list_f.write(lines)



def write_xml(anno_path, objs, img_path, output_dir, head, objectstr, tailstr, dataset):
    print(anno_path)
    # 如果xml第一次被写入则直接写入即可
    if not os.path.exists(anno_path):
        with open(anno_path, 'w') as f:
            f.write(head)
            for obj in objs:
                f.write(objectstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
            f.write(tailstr)
            write_txt(output_dir, anno_path, img_path, dataset)
    # 如果classes则追加写入
    else:
        with open(anno_path, 'r', encoding='utf-8') as fs:
            content = fs.read()
            with open(anno_path, 'w', encoding='utf-8') as f:
                end_annotation = content.rfind("</annotation>")
                print(end_annotation)
                f.write(content[:-14])
                for obj in objs:
                    f.write(objectstr % (obj[0], obj[1], obj[2], obj[3], obj[4]))
                f.write(tailstr)
    # write_txt(output_dir, anno_path, img_path, dataset, classes_name)


def save_head(objs, img_name, img_path, output_anno_dir, output_dir, headstr, tailstr, objectstr, dataset):
    imgs = cv2.imread(img_path)
    anno_path = os.path.join(output_anno_dir, img_name[:-3] + "xml")
    print("anno_path:", anno_path)

    if (imgs.shape[2] == 1):
        print(img_name + " not a RGB image")
        return

    head = headstr % (img_name, imgs.shape[1], imgs.shape[0], imgs.shape[2])
    write_xml(anno_path, objs, img_path, output_dir, head, objectstr, tailstr, dataset)


def find_anno_img(input_dir):
    # According input dir path find Annotations dir and Images dir
    anno_dir = os.path.join(input_dir, "Annotations")
    img_dir = os.path.join(input_dir, "Images")
    return anno_dir, img_dir


def main_object365(input_dir, output_dir, headstr, tailstr, objectstr):
    anno_dir, img_dir = find_anno_img(input_dir)
    for dataset in ["val"]:
        # xml output dir path
        output_anno_dir = os.path.join(output_dir, "annotations_xml_{}".format(dataset))
        if not os.path.exists(output_anno_dir):
            mkr(output_anno_dir)

        # read jsons file
        anno_file_path = os.path.join(anno_dir, "{}".format(dataset), "{}".format(dataset)+".json")
        # read imgs file
        imgs_file_path = os.path.join(img_dir, "{}".format(dataset))
        save_annotations(anno_file_path, imgs_file_path, output_anno_dir, output_dir,headstr, tailstr, objectstr, dataset)
