from PIL import Image, ImageDraw


def create_puzzle_piece(image, x, y, width, height, is_left, is_right, is_top, is_bottom):
    # 创建一个透明的拼图块
    piece = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(piece)

    # 定义凹凸边缘的尺寸
    edge_size = 20

    # 绘制拼图块的边缘
    if is_left:
        draw.pieslice([(0, 0), (edge_size * 2, edge_size * 2)], 90, 180, fill=(255, 255, 255, 255))
    if is_right:
        draw.pieslice([(width - edge_size * 2, 0), (width, edge_size * 2)], 0, 90, fill=(255, 255, 255, 255))
    if is_top:
        draw.pieslice([(0, 0), (edge_size * 2, edge_size * 2)], 180, 270, fill=(255, 255, 255, 255))
    if is_bottom:
        draw.pieslice([(0, height - edge_size * 2), (edge_size * 2, height)], 270, 360, fill=(255, 255, 255, 255))

    # 将原始图片的部分区域粘贴到拼图块上
    image_crop = image.crop((x, y, x + width, y + height))

    # 创建一个与裁剪图像相同大小的透明度掩码
    mask = Image.new('L', (width, height), 255)
    mask_draw = ImageDraw.Draw(mask)

    # 在掩码上绘制边缘的透明度
    if is_left:
        mask_draw.pieslice([(0, 0), (edge_size * 2, edge_size * 2)], 90, 180, fill=0)
    if is_right:
        mask_draw.pieslice([(width - edge_size * 2, 0), (width, edge_size * 2)], 0, 90, fill=0)
    if is_top:
        mask_draw.pieslice([(0, 0), (edge_size * 2, edge_size * 2)], 180, 270, fill=0)
    if is_bottom:
        mask_draw.pieslice([(0, height - edge_size * 2), (edge_size * 2, height)], 270, 360, fill=0)

    # 使用掩码将裁剪的图像粘贴到拼图块上
    piece.paste(image_crop, (0, 0), mask)

    # 绘制凹凸边缘
    if is_left:
        draw.polygon([(0, 0), (edge_size, edge_size), (0, height)], fill=(0, 0, 0, 0))
    if is_right:
        draw.polygon([(width, 0), (width - edge_size, edge_size), (width, height)], fill=(0, 0, 0, 0))
    if is_top:
        draw.polygon([(0, 0), (edge_size, edge_size), (width, 0)], fill=(0, 0, 0, 0))
    if is_bottom:
        draw.polygon([(0, height), (edge_size, height - edge_size), (width, height)], fill=(0, 0, 0, 0))

    return piece


def split_image_into_puzzle(image_path, rows, cols):
    # 加载原始图片
    image = Image.open(image_path)
    width, height = image.size

    # 计算每个拼图块的尺寸
    piece_width = width // cols
    piece_height = height // rows

    # 分割图片并生成拼图块
    for row in range(rows):
        for col in range(cols):
            x = col * piece_width
            y = row * piece_height
            is_left = col == 0
            is_right = col == cols - 1
            is_top = row == 0
            is_bottom = row == rows - 1

            piece = create_puzzle_piece(image, x, y, piece_width, piece_height, is_left, is_right, is_top, is_bottom)
            piece.save(f'puzzle_piece_{row}_{col}.png')

# 使用示例
split_image_into_puzzle('images/wallhaven-85qp31.jpg', 4, 4)
