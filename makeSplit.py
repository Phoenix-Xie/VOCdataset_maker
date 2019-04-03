import os
from setting import VOC_ROOT as root
import random
from setting import test_percent, train_percent, val_percent

trainval_percent = train_percent + val_percent


def split_train_test():
    """
    将数据集划分为训练集和测试集
    :return:
    """
    wk_root = root+'/VOC/ImageSets/Main/'
    if not os.path.exists(wk_root):
        os.makedirs(wk_root)
    test_txt = open(wk_root+"test.txt", 'w', newline='\n')
    train_txt = open(wk_root + "train.txt", 'w', newline='\n')
    val_txt = open(wk_root + "val.txt", 'w')
    trainval_txt = open(wk_root + "trainval.txt", 'w', newline='\n')

    img_root = root+'/VOC/JPEGImages'
    test_level = test_percent
    train_level = train_percent+test_percent
    val_level = train_percent+val_percent+test_percent

    if test_percent+train_percent+val_percent != 1:
        print('三个文件总和不为1')
        return
    for dirpath, dirnames, filenames in os.walk(img_root):
        for filename in filenames:
            filename = filename.split('.')
            level = random.random()
            filename = filename[0] + '\n'
            if level <= test_level:
                test_txt.write(filename)
            elif level <= train_level:
                train_txt.write(filename)
                trainval_txt.write(filename)
            else:
                val_txt.write(filename)
                trainval_txt.write(filename)


if __name__ == "__main__":
    split_train_test()