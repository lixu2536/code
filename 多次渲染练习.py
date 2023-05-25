import bpy
import math
import time

# 根据摄像机的名称，获取实例
camera = bpy.data.objects['Camera']

# 摄像机与物体的距离
distance = 1.375

# 总的张数
loc_total_num = 16

# 每张之间的角度间隔
div_angle = 4.5


# 设置渲染为图片
bpy.data.scenes["Scene"].render.image_settings.file_format = 'PNG'

# 循环渲染16张
for i in range(loc_total_num):
    # 角度从 -4.5° * 8 到 4.5° *7，并转换为弧度值
    angle = (i - loc_total_num / 2) * div_angle / 360 * 2 * math.pi
    
    # 根据三角函数计算摄像机的x,y坐标，z坐标不变
    x = distance * math.sin(angle)
    y = distance * math.cos(angle)
    
    # 将计算到的坐标赋值给到摄像机
    camera.location[0] = x
    camera.location[1] = -y
    
    # 将旋转角度赋值给到摄像机，保证摄像头正对着目标
    camera.rotation_euler[2] = angle
    
    # 设置保存图片的文件名
    bpy.data.scenes["Scene"].render.filepath = '//%02d'%(i)
    
    # 渲染并保存为文件
    bpy.ops.render.render( write_still=True )
    