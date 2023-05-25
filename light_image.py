import bpy

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
    n = 1
    image_path = 'E:\\blender study\\fringe\\{}.bmp'.format(n)
    image_texture = bpy.data.textures.new('MyTexture', type='IMAGE')
    image_texture.image = bpy.data.images.load(image_path)

    # 更改 Image Texture 纹理节点的图片
    texture_node.image = image_texture.image

bpy.ops.outliner.orphans_purge(do_recursive=True)