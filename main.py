import os
import argparse
from cooc_annos2voc import main_coco
from object365_annos2voc import main_object365

headstr = """\
<annotation>
    <folder>VOC</folder>
    <filename>%s</filename>
    <source>
        <database>My Database</database>
        <annotation>COCO</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""

objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''

def make_parser():
    parser = argparse.ArgumentParser(description="conver annotations format to VOC")
    parser.add_argument("-d", "--dataset", dest="dataset", required=True, help="dataset name", type=str, choices=["coco", "object365"])
    parser.add_argument("-i", "--input", dest="input_dir", required=True, help="the input dir of the picture", type=str)
    parser.add_argument("-y", "--dataset-year", dest="dyear", default="", help="the year for coco dataset", type=str)
    parser.add_argument("-c", "--class", dest="classes", nargs = "*", help="the class want to select, ['cell phone', 'handbag', 'laptop', 'cat', 'dog']", type=str)
    parser.add_argument("--output-class", dest="output_class", action='store_true', default=False, help="output the class on the list.txt")
    parser.add_argument("-o", "--output", dest="output_dir", help="the output dir of the result", type=str)
    return parser


def main():
    parser = make_parser()

    args = vars(parser.parse_args())
    dataset = args["dataset"]
    input_dir = args["input_dir"]
    dyear = args["dyear"]
    classes = args["classes"]
    output_class = args["output_class"]
    output_dir = args["output_dir"]

    # anno_dir = os.path.join(output_dir, "annotations")

    if dataset == "object365":
        #  python main.py -p object365 -i "C:\kuangshi\Objects365\Images\val\val\val" -o "C:\kuangshi\result/"
        # paramter: headstr, tailstr, objstr, input_dir, anno_dir, output_dir
        main_object365(input_dir, output_dir, headstr, tailstr, objstr)
    elif dataset == "coco":
        # python main.py -p coco -i "C:\coco\val2014" -o "C:\coco\val2014\result/"
        if dyear == "":
            print("dataset-year is required")
            exit(1)
        main_coco(input_dir, dyear, classes, output_class, output_dir, headstr, objstr, tailstr)

if __name__ == '__main__':
    main()


