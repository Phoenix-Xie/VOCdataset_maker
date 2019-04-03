import matplotlib.pyplot as plt
import numpy as np
import os
import cv2
import csv
# if __name__ == '__main__':
#     img1 = cv2.imread('image/2.jpg')
#     plt.imshow(img1)
#     # print(img1.shape)
#     print(img1)
#     for i, line in enumerate(img1):
#         for j, column in enumerate(line):
#             flag = True
#             for k, depth in enumerate(column):
#                 if depth < 240:
#                     flag = False
#             if flag:
#                 img1[i][j][0] = 100
#                 img1[i][j][0] = 100
#                 img1[i][j][0] = 100
#     cv2.imshow('image', img1)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# 保留的rgb范围
max_rgb = 255
min_rgb = 0
set_rgb = 0
bondingbox_pad = 10


def clear_img(img):
    """

    :param img:
    :return:
    """
    for i, line in enumerate(img):
        for j, colum in enumerate(line):
            flag = True
            for k, color in enumerate(colum):
                if color <= min_rgb or color >= max_rgb:
                    flag = False
                    break
            if flag:
                for k, color in enumerate(colum):
                    img[i][j][k] = set_rgb
    return img


root_path = r"D:\BaiduNetdiskDownload\af2019-cv-training-20190312\af2019-cv-training-20190312\\"
if __name__ == "__main__":
    file = open(root_path+"list.csv")
    file.readline()
    info = csv.reader(file)
    for row in info:
        id = row[0]
        x = int(row[1])
        y = int(row[2])
        judge = row[3]
        print(root_path + id)
        # 读取
        imga = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_a.jpg")
        imgb = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_b.jpg")
        imgc = cv2.imread(root_path + "\\"+id[:2] + "\\" + id+"_c.jpg")

        # 转换为灰度值图

        # imga = cv2.cvtColor(imga, cv2.COLOR_BGR2GRAY)
        # imgb = cv2.cvtColor(imgb, cv2.COLOR_BGR2GRAY)
        # imgc = cv2.cvtColor(imgc, cv2.COLOR_BGR2GRAY)

        # 标记
        cv2.rectangle(imga, (x - bondingbox_pad, y - bondingbox_pad), (x + bondingbox_pad, y+bondingbox_pad), (99, 99, 238), 2)
        cv2.rectangle(imgb, (x - bondingbox_pad, y - bondingbox_pad), (x + bondingbox_pad, y + bondingbox_pad), (99, 99, 238), 2)
        cv2.rectangle(imgc, (x - bondingbox_pad, y - bondingbox_pad), (x + bondingbox_pad, y + bondingbox_pad), (99, 99, 238), 2)

        # font = cv2.FONT_HERSHEY_COMPLEX
        # text = judge
        # cv2.putText(imga, text, (x-10, y-10), font, 2, (99, 99, 238), 1)
        # cv2.putText(imgb, text, (x - 10, y - 10), font, 2, (99, 99, 238), 1)
        # cv2.putText(imgc, text, (x - 10, y - 10), font, 2, (99, 99, 238), 1)

        cv2.imshow(judge+'_a'+str(imga.shape), imga)
        cv2.imshow(judge+'_b', imgb)
        cv2.imshow(judge+'_c', imgc)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    # for parent, dirnames, filenames in os.walk(root_path):
    #     c = 0
    #     for filename in filenames:
    #         c += 1
    #         if c != 1:
    #             c %= 3
    #             continue
    #         print(filename)
    #         imga = cv2.imread(root_path+"\\"+filename)
    #         print(imga.shape)
    #         print(imga)
    #         imgb = cv2.imread(root_path + "\\" + filename[:-5]+'b'+filename[-4:])
    #         imgc = cv2.imread(root_path + "\\" + filename[:-5]+'c'+filename[-4:])
    #         imga = clear_img(imga)
    #         print(imga)
    #         imgb = clear_img(imgb)
    #         cv2.imshow('a', imga)
    #         cv2.imshow('b', imgb)
    #         cv2.imshow('c', imgc)
    #         cv2.waitKey(0)
    #         cv2.destroyAllWindows()


