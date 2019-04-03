import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import csv
from xml.dom.minidom import Document
import makeSplit
from setting import bnd_len, source_path, VOC_ROOT

root_path = source_path
save_path = VOC_ROOT+'VOC/JPEGImages/'


def make_xml(img, save_name, objects, path=VOC_ROOT+"VOC\Annotations"):
    """
    根据给定的信息生成xml
    :param img: 进行处理的图像
    :param save_name: 存储的名称
    :param objects: 物件列表，每一项有五个值,分别为 名称，Uspecified, 0, 0, [xmin,ymin,xmax,ymax]
    :param path: 保存路径
    :return:
    """
    doc = Document()
    # img = np.zeros((10, 10, 3))
    # objects = [
    #     ['face', 'Uspecified', 0, 0, [1, 1, 2, 2]],
    #     ['face2', 'Uspecified', 0, 0, [1, 1, 3, 3]],
    # ]
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    folder = doc.createElement('folder')
    annotation.appendChild(folder)
    folder_text = doc.createTextNode('VOCType')
    folder.appendChild(folder_text)
    filename = doc.createElement('filename')
    filename_text = doc.createTextNode(save_name)
    filename.appendChild(filename_text)
    annotation.appendChild(filename)
    file_path = doc.createElement('path')
    file_path_text = doc.createTextNode(path)
    file_path.appendChild(file_path_text)
    annotation.appendChild(file_path)

    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    source.appendChild(database)
    database_text = doc.createTextNode('Unknown')
    database.appendChild(database_text)

    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    height = doc.createElement('height')
    depth = doc.createElement('depth')
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)

    assert(img.shape[0] > 0)
    assert(img.shape[1] > 0)
    assert(img.shape[2] > 0)
    # 注意此处第一个参数是宽度
    width_text = doc.createTextNode(str(img.shape[1]))
    height_text = doc.createTextNode(str(img.shape[0]))
    depth_text = doc.createTextNode(str(img.shape[2]))
    width.appendChild(width_text)
    height.appendChild(height_text)
    depth.appendChild(depth_text)

    segmented = doc.createElement('segmented')
    segmented_text = doc.createTextNode('0')
    segmented.appendChild(segmented_text)
    annotation.appendChild(segmented)

    for o in objects:
        object = doc.createElement('object')
        annotation.appendChild(object)

        name = doc.createElement('name')
        object.appendChild(name)
        name_text = doc.createTextNode(o[0])
        name.appendChild(name_text)

        pose = doc.createElement('pose')
        pose_text = doc.createTextNode(o[1])
        object.appendChild(pose)
        pose.appendChild(pose_text)

        truncated = doc.createElement('truncated')
        truncated_text = doc.createTextNode(str(o[2]))
        object.appendChild(truncated)
        truncated.appendChild(truncated_text)

        difficult = doc.createElement('difficult')
        difficult_text = doc.createTextNode(str(o[3]))
        object.appendChild(difficult)
        difficult.appendChild(difficult_text)
        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmin_text = doc.createTextNode(str(o[4][0]))
        xmin.appendChild(xmin_text)
        ymin = doc.createElement('ymin')
        # print(len(o))
        ymin_text = doc.createTextNode(str(o[4][1]))
        ymin.appendChild(ymin_text)
        xmax = doc.createElement('xmax')
        xmax_text = doc.createTextNode(str(o[4][2]))
        xmax.appendChild(xmax_text)
        ymax = doc.createElement('ymax')
        ymax_text = doc.createTextNode(str(o[4][3]))
        ymax.appendChild(ymax_text)

        bndbox.appendChild(xmin)
        bndbox.appendChild(ymin)
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymax)

    with open(path + "\\" + save_name + '.xml', 'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))


def clear(img):
    """
    取全图均值，将图中小于均值的点灰度值设为0，即全黑
    :param img: 处理的图片
    :return: 处理后的图片
    """
    # print()
    ave = np.mean(img)+20
    # print(ave)
    l = len(img)
    l2 = len(img[0])
    for i in range(l):
        for j in range(l2):
           img[i][j] = 0 if img[i][j] <= ave else img[i][j]
    return img


if __name__ == "__main__":
    file = open(root_path+"list.csv")
    file.readline()
    info = csv.reader(file)
    count = 1
    for row in info:
        # 计算名称
        name = str(count)
        while len(name) < 6:
            name = '0' + name

        # 读取标记内容
        id = row[0]
        x = int(row[1])
        y = int(row[2])
        judge = row[3]

        # 生成xml文件
        img = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_a.jpg")
        max_bnd_x = len(img[0])
        max_bnd_y = len(img)
        xmin = x - bnd_len
        xmin = xmin if xmin >= 1 else 1
        ymin = y - bnd_len
        ymin = ymin if ymin >= 1 else 1
        xmax = x + bnd_len
        xmax = xmax if xmax <= max_bnd_x else max_bnd_x
        ymax = y + bnd_len
        ymax = ymax if ymax <= max_bnd_y else max_bnd_y

        isstar = 0
        stars = ['newtarget', 'isstar', 'asteroid', 'isnova	', 'known']
        for i in stars:
            if judge == i:
                isstar = 1
                # print(judge)
                break

        make_xml(img, name, [[str(isstar), 'Uspecified', 0, 0, [xmin, ymin, xmax, ymax]]])

        # 查询该文件是否存在
        if os.path.exists(save_path+name + '.jpg'):
            count += 1
            # print(name+" exits")
            continue
        # print(name)
        # 读取
        imga = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_a.jpg")
        imgb = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_b.jpg")
        imgc = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_c.jpg")
        img = imga

        # 转换为灰度图
        imga = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
        imgb = cv2.cvtColor(imgb, cv2.COLOR_BGR2GRAY)
        imgc = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("before", imga)
        # img = np.zeros((len(imga), len(imga[0]), 3), dtype=int)
        imga = clear(imga)

        # 将三张灰度图合成
        l = len(imga)
        for i in range(l):
            for j in range(len(imga[0])):
                img[i][j][0] = imga[i][j]
                img[i][j][1] = imgb[i][j]
                img[i][j][2] = imgc[i][j]

        # 保存图像
        cv2.imwrite(save_path+name + '.jpg', img)

        # cv2.rectangle(imgc, (xmin, ymin), (xmax, ymax),(100, 0, 0), 2)
        # cv2.rectangle(imga, (xmin, ymin), (xmax, ymax), (100, 0, 0), 2)
        # cv2.rectangle(imgb, (xmin, ymin), (xmax, ymax), (100, 0, 0), 2)
        # cv2.imshow("after", imga)
        # cv2.imshow("b", imgb)
        # cv2.imshow("c", imgc)

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        count += 1

    # 分割数据集
    makeSplit.split_train_test()
