import os
import sys
import bpy
import math
import numpy
from stl import mesh


def main():
    # 模型路径
    model_path = 'E:\\blender study\\model'
    model_list = os.listdir(model_path)  # 检索文件夹下文件名
    # print(model_list)   # ['Barry Bear.stl', 'Cat in Armor.stl', 'machop.stl', 'puppy.stl']

    # 获取目录下的stl文件.
    stl_list = [item for item in model_list if item.endswith('.STL') or item.endswith('.stl')]
    # print(stl_list)  # ['Barry Bear.stl', 'Cat in Armor.stl', 'machop.stl', 'puppy.stl']

    # 修改Blender引擎设置.（先在环境配置好）
    # bpy.context.scene.render.engine = 'CYCLES'

    # 设置渲染为图片
    bpy.data.scenes["Scene"].render.image_settings.file_format = 'BMP'

    # 指定投影的条纹图
    for i in range(9, 12):
        fringe_light(i+1)

        # 渲染图片保存路径
        render_path = 'E:\\blender study\\render_image\\render{}'.format(i+1)
        folder = os.path.exists(render_path)
        if not folder:  # 判断文件夹是否存在，并创建。
            os.makedirs(render_path)

        # 根据模型文件依次导入、渲染（保存）、旋转、渲染（保存）、移除物体。
        for item in stl_list:
            stl_path = os.path.join(model_path, item)
            # print(stl_path)  # E:\blender study\model\Barry Bear.stl

            obj_name = os.path.splitext(item)[0]
            # print(obj_name)  # Barry Bear

            # 使用numpy-stl库查询stl模型的实际尺寸参数
            in_mesh = mesh.Mesh.from_file(stl_path)
            # volume, cog, inertia = in_mesh.get_mass_properties()
            # #  体积，重心，重心的惯性矩阵
            xyz = (in_mesh.max_ - in_mesh.min_)
            sizel = round(xyz[0], 2)
            sizew = round(xyz[1], 2)
            sizeh = round(xyz[2], 2)
            # print(sizel)  # 85.6m X

        # # print all objects (全选的一种方式)
        # scene_name = []     # 存放物体名
        # for obj in bpy.data.objects:
        #     # print(obj.name)
        #     # scene_name.append(obj.name)     # 读取场景中的物体名
        #     bpy.data.objects.remove(obj)    # data.objects.remove 删除命令
        #     # 循环删除场景内容

        # 或使用ops.object.selcet_all进行全选
        # bpy.ops.object.selcet_all(action='SELECT')
        # bpy.data.objects.remove()

            # 导入新STL文件
            # bpy.ops.import_mesh.stl(filepath="E:\\blender study\\puppy.stl")
            bpy.ops.import_mesh.stl(filepath=stl_path)
            # obj = bpy.data.objects[]

            # 对导入物体进行原点设置到几何中心
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

            # 设置物体跟随原点到世界中心
            bpy.context.object.location[1] = 0
            bpy.context.object.location[2] = 0
            bpy.context.object.location[0] = 0

            # 物体尺寸缩放
            scale_size = 0.8/sizeh
            bpy.context.object.scale[1] = scale_size
            bpy.context.object.scale[2] = scale_size
            bpy.context.object.scale[0] = scale_size

            # 物体表面平滑操作
            bpy.ops.object.shade_smooth()
            # 物体实例
            obj = bpy.data.objects[obj_name]

            # 摄像机实例
            camera = bpy.data.objects['Camera']
            # 每张之间的角度间隔
            div_angle = 4.5
            # 渲染张数
            loc_total_num = 1
            # 渲染函数
            rendering(obj, obj_name, loc_total_num, div_angle, render_path)
            print("render done stl {}".format(item))

            bpy.data.objects.remove(obj)  # 从工程中删除物体，但请注意，它的data还保留着
            bpy.ops.outliner.orphans_purge(do_recursive=True)  # 删除所有无引用的数据data，即垃圾回收


def fringe_light(n=1):
    # 获取默认点光源
    light = bpy.data.objects['Light']

    # 选择当前工作区域的对象
    bpy.context.view_layer.objects.active = light

    # 获取点光源的节点树
    nodes = light.data.node_tree.nodes
    for i in range(len(nodes)):
        print(nodes[i].name)
        print(nodes[i].type)

    # 遍历所有节点，找到和自发光节点相连的 Image Texture 节点
    emission_node = None
    texture_node = None
    for node in nodes:
        if node.type == "EMISSION":
            emission_node = node
        elif node.type == "TEX_IMAGE" and texture_node is None:
            texture_node = node
            break

    if texture_node is None:
        print("未找到与自发光节点相连的 Image Texture 节点")
    else:
        # 创建Image纹理并设置图片路径
        image_path = 'E:\\blender study\\fringe\\{}.bmp'.format(n)
        image_texture = bpy.data.textures.new('MyTexture', type='IMAGE')
        image_texture.image = bpy.data.images.load(image_path)

        # 更改 Image Texture 纹理节点的图片
        texture_node.image = image_texture.image

    bpy.ops.outliner.orphans_purge(do_recursive=True)


def rendering(object_item, object_name, num, set_angle, path):
    """
    渲染循环
    :param object_item: stl物体列表实例
    :param object_name: 物体名称
    :param num: 旋转次数（渲染张数）
    :param set_angle: 单次变换角度
    :param path: 渲染结果保存路径
    :return:
    """
    for i in range(num):
        # 角度从 -4.5° * 8 到 4.5° *7，并转换为弧度值
        angle = (i - num / 2) * set_angle / 360 * 2 * math.pi

        # # 根据三角函数计算摄像机的x,y坐标，z坐标不变
        # x = distance * math.sin(angle)
        # y = distance * math.cos(angle)
        #
        # # 将计算到的坐标赋值给到摄像机？？
        # camera.location[0] = x
        # camera.location[1] = -y

        # # 将旋转角度赋值给到摄像机，保证摄像头正对着目标
        # camera.rotation_euler[2] = angle

        # 物体z轴旋转角度
        object_item.rotation_euler[2] = angle

        # 设置保存图片的文件名
        s = '%02d' % i
        bpy.data.scenes["Scene"].render.filepath = '{}//{}{}'.format(path, object_name, s)
        # render_path +'//'+ obj_name + '%02d' % (i)

        # 渲染并保存为文件
        bpy.ops.render.render(write_still=True)
        print("render done img {}".format(i+1))


# 添加摄像机
# bpy.ops.object.camera_add(enter_editmode=False, align='VIEW',
#                           location=(0, -20, 0), rotation=(math.pi/2, 0, 0), scale=(1, 1, 1))


# bpy.data.objects['Camera'].data.lens

# light 投射图像
# bpy.ops.image.open(filepath="D:\\Fringe Matlab\\2.bmp", directory="D:\\Fringe Matlab\\",
#                    files=[{"name":"2.bmp", "name":"2.bmp"}], relative_path=True, show_multiview=False)


if __name__=="__main__":
    main()
