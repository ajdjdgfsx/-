import qrcode
import json
import os

def generate_qr(data, image_path="qr.png", json_path="qr.json", save_image=True, save_json=True):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    
    # 只在需要时保存图片
    if save_image:
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(image_path)
        print(f"[✓] 二维码图片已保存为: {image_path}")
    
    # 只在需要时保存JSON
    if save_json:
        with open(json_path, "w") as f:
            json.dump(matrix, f)
        print(f"[✓] 点阵数据已保存为: {json_path}")

    return matrix

def generate_qr_text(matrix, add_size_tag=False, size_value=1):
    """生成二维码文本内容，可选择是否添加size标签"""
    # 计算需要裁剪的边界（保留1个模块的边框）
    border_size = 1
    
    # 计算裁剪后的尺寸
    height = len(matrix)
    width = len(matrix[0])
    start_row = border_size
    end_row = height - border_size
    start_col = border_size
    end_col = width - border_size
    
    # 生成文本行
    lines = []
    for row in matrix[start_row:end_row]:
        # 创建二维码行字符串
        qr_line = ''.join('█' if cell else '□' for cell in row[start_col:end_col])
        
        # 如果需要添加size标签
        if add_size_tag:
            line = f"<size={size_value}>{qr_line}"
        else:
            line = qr_line
            
        lines.append(line)
    
    return lines

def print_and_save_qr(matrix, add_size_tag=False, size_value=1, txt_path=None):
    """打印二维码并可选保存到文本文件"""
    print("\n[↓] 控制台二维码预览（核心区域）")
    lines = generate_qr_text(matrix, add_size_tag, size_value)
    
    # 打印到控制台
    for line in lines:
        print(line)
    
    # 保存到文本文件
    if txt_path:
        # 确保路径有.txt扩展名
        if not txt_path.endswith('.txt'):
            txt_path += '.txt'
            
        with open(txt_path, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line + "\n")
        print(f"[✓] 二维码文本已保存为: {txt_path}")
    
    return lines

if __name__ == "__main__":
    qr_content = input("请输入要生成二维码的内容：\n> ").strip()
    if not qr_content:
        print("⚠️ 输入为空，已取消生成。")
    else:
        # 询问是否保存图片
        save_image = input("是否保存二维码图片？(y/n): ").strip().lower() == 'y'
        image_path = None
        
        # 如果需要保存图片，获取路径
        if save_image:
            image_path = input("请输入图片保存路径(默认使用qr.png): ").strip()
            if not image_path:
                image_path = "qr.png"
            elif not image_path.endswith('.png'):
                image_path += '.png'
        
        # 询问是否保存JSON
        save_json = input("是否保存点阵JSON数据？(y/n): ").strip().lower() == 'y'
        json_path = None
        
        # 如果需要保存JSON，获取路径
        if save_json:
            json_path = input("请输入JSON保存路径(默认使用qr.json): ").strip()
            if not json_path:
                json_path = "qr.json"
            elif not json_path.endswith('.json'):
                json_path += '.json'
        
        # 询问是否添加size标签
        add_size_tag = input("是否在每行添加<size=n>标签？(y/n): ").strip().lower()
        size_value = 1
        
        # 如果需要添加标签，获取n值
        if add_size_tag == 'y':
            size_input = input("请输入size值(n, 应为整数): ").strip()
            try:
                size_value = int(size_input)
            except ValueError:
                print("⚠️ 输入的不是有效整数，将使用默认值size=1")
                size_value = 1
        
        # 询问是否保存到文本文件
        save_to_txt = input("是否保存二维码文本到文件？(y/n): ").strip().lower()
        txt_path = None
        
        # 如果需要保存到文件，获取文件名
        if save_to_txt == 'y':
            txt_path = input("请输入文本保存路径(默认使用qr.txt): ").strip()
            if not txt_path:
                txt_path = "qr.txt"
        
        # 生成二维码
        matrix = generate_qr(
            data=qr_content,
            image_path=image_path if save_image else None,
            json_path=json_path if save_json else None,
            save_image=save_image,
            save_json=save_json
        )
        
        # 打印并保存二维码文本
        print_and_save_qr(
            matrix, 
            add_size_tag=(add_size_tag == 'y'), 
            size_value=size_value,
            txt_path=txt_path
        )
