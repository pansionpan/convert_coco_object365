# convert_anno_format

## 程序目的
1. 将COCO数据集中指定类型的数据标注转换成XML格式，并生成对应的图片及标注列表
    指定类型包含，可动态选择类型：
    * 手提包
    * 笔记本电脑
    * 手机
    * 狗
    * 猫

    XML格式定义如下：
    ```
    <annotation>
	<folder>VOC2012</folder>
	<filename>2007_000392.jpg</filename>   //文件名                        
	<source>     //图像来源                                                     
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
	</source>
	<size>		 //图像尺寸（宽、高以及通道数）			
		<width>500</width>
		<height>332</height>
		<depth>3</depth>
	</size>
	<segmented>1</segmented>		 //是否用于分割                     
	<object>      //检测到的物体                                                     
		<name>horse</name>   //物体类别
        <pose>Right</pose>   //拍摄角度                                      
        <truncated>0</truncated>     //是否被截断
        <difficult>0</difficult>   //目标是否难以识别
        <bndbox>        //bounding-box（包含左上角和右下角x,y坐标）                                                 
            <xmin>100</xmin>
            <ymin>96</ymin>
            <xmax>355</xmax>
            <ymax>324</ymax>
        </bndbox>
    </object>
    <object>    //检测到多个物体，依次顺延                                                       
        <name>person</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>198</xmin>
            <ymin>58</ymin>
            <xmax>286</xmax>
            <ymax>197</ymax>
        </bndbox>
    </object>
    </annotation>

    ```

2. 挑选指定的测试数据集
    TBD

## 输入
1. 数据集类型，必须，可供选择的值 [coco，object365]
1. 数据集目录
COCO数据集目录结构如下 
```
/path/to/COCO
    annotations
        instances_train2014.json
        instances_val2014.json
        instances_train2017.json
        instances_val2017.json
    test2014
    test2017
    train2014
    train2017
    val2014
    val2017
```
object365数据集目录结构如下：
```
/path/to/object365
    Annotations
        train
            train.json
        val
            val.json
    Images
        train
            *.jpg
        val
            *.jpg
```

2. 数据年份, 数据集类型为coco时有作用，可选择 [2014, 2017]
3. 包含的类型，支持多个，常用的有：
coco:
class_names = {cellphone, handbag, laptop}
object365:
class_names = {cellphone, key, handbag, laptop}
4. 输出列表文件中是否包含类别信息

## 输出
1. 标注输出目录，不提供时缺省为输入目录
```
/path/to/output
    annotations_xml_train                   // 标注目录
        xxx.xml                             // 标注文件
        yyy.xml                             // 标注文件
    annotations_xml_val                     // 标注目录
        xxx.xml                             // 标注文件
        yyy.xml                             // 标注文件
    annotations_xml_coco_train2014.txt
    annotations_xml_coco_val2014.txt             
    annotations_xml_coco_train2017.txt           
    annotations_xml_coco_val2017.txt             
    annotations_xml_object365_train.txt          
    annotations_xml_object365_val.txt            
```

列表文件格式
```
    XML文件路径 图片路径 [类别1 类别2 ...]
```
XML文件路径为相对于输出目录的相对路径
图片路径为相对于输入目录的相对路径

## 依赖
```
pip install pycocotools
pip install six
pip install numpy
pip install tqdm
pip install opencv-python
```