# -*- coding:utf-8 -*-
'''
实现对遥感数据的管理：
1. 数据获取内容：1）连接google storage的数据库 ；2）获取感兴趣区域的遥感影像；3）调用IDM下载遥感影像
2. 数据管理内容：1) 获取下载影像的RGB真彩色合成图片，有一个直观的印象
@ author: zhyin
@ time: 2019/10/12
'''

from osgeo import gdal
import os
import numpy as np


def read_img(filename):
    dataset = gdal.Open(filename)  # 打开文件

    width = dataset.RasterXSize  # 栅格矩阵的列数
    height = dataset.RasterYSize  # 栅格矩阵的行数

    gcs = dataset.GetGeoTransform()  # 仿射矩阵
    pcs = dataset.GetProjection()  # 地图投影信息
    data = dataset.ReadAsArray(0, 0, width, height)  # 将数据写成数组，对应栅格矩阵

    del dataset  # 关闭对象，文件dataset
    return pcs, gcs, data, width, height


def linearstretching(img):
    min = img.min()
    max = img.max()
    img = np.where(img > min, img, min)
    img = np.where(img < max, img, max)
    img = (img - min) / (max - min) * 255
    return img


def band_combination(RS_dir):
    '''
    321真彩色合成
    :param dir: 遥感影像存放目录
    :param path: 遥感影像的行
    :param row: 遥感影像的列
    :return: RGB png格式图片
    '''
    # 遍历文件夹，逐个进行RGB图像合成
    for roots, dirs, files in os.walk(RS_dir):
        for dir in dirs:
            if "L" in dir:
                # 获取每个目录下的TIF的相对路径
                tif_dir = "%s%s/" % (RS_dir, dir)
                tif_name = [("%s_B3.TIF" % dir[-40:]),
                            ("%s_B4.TIF" % dir[-40:]),
                            ("%s_B5.TIF" % dir[-40:])]
                band_tif1 = os.path.join(tif_dir, tif_name[0])
                band_tif2 = os.path.join(tif_dir, tif_name[1])
                band_tif3 = os.path.join(tif_dir, tif_name[2])
                #
                # 读取每个TIF
                pcs, gcs, Bdata, width, height = read_img(band_tif1)
                _, _, Gdata, _, _ = read_img(band_tif2)
                _, _, Rdata, _, _ = read_img(band_tif3)
                #
                # 线性拉伸
                Bdata = linearstretching(Bdata)
                Gdata = linearstretching(Gdata)
                Rdata = linearstretching(Rdata)

                #
                # 定义输出TIFF的格式
                gtiff_driver = gdal.GetDriverByName('GTiff')
                gtiff_name = "%s_nat_color.tif" % dir[-40:]
                out_ds = gtiff_driver.Create(gtiff_name,
                                             width,
                                             height,
                                             3,
                                             gdal.GDT_Byte)
                out_ds.SetProjection(pcs)
                out_ds.SetGeoTransform(gcs)
                #
                # 存入1波段数据
                out_ds.GetRasterBand(3).WriteArray(Bdata)
                #
                # 存入2波段数据
                out_ds.GetRasterBand(2).WriteArray(Gdata)
                #
                # 存入3波段数据
                out_ds.GetRasterBand(1).WriteArray(Rdata)

                out_ds.FlushCache()
                #
                del out_ds


if __name__ == "__main__":
    band_combination (r"L:/a_遥感影像/cratchdata/23031/")
