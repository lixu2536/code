import os
import sys
import bpy
import math
import numpy
from stl import mesh


def main():
   
    # 设置渲染为图片
    bpy.data.scenes["Scene"].render.image_settings.file_format = 'PNG'
    # 渲染图片保存路径
    render_path = 'E:\\blender study\\render_image'
    folder = os.path.exists(render_path)
    if not folder:  # 判断文件夹是否存在，并创建。
        os.makedirs(render_path)

    # 渲染函数
    # 获取默认点光源
    light = bpy.data.objects['Light']

    for i in range(20):
        s = (i + 1) * 10
        light.data.energy = s

        # 设置保存图片的文件名
        bpy.data.scenes["Scene"].render.filepath = '{}//{}w'.format(render_path, s)
        # render_path +'//'+ obj_name + '%02d' % (i)

        # 渲染并保存为文件
        bpy.ops.render.render(write_still=True)
        print("render done img {}w".format(s))


if __name__=="__main__":
    main()
