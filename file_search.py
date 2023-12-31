import os
import re

# 文件夹大小, 子节转MB, GB
def format_folder_size(folder_size):
    mb = folder_size / 1024 / 1024
    gb = mb / 1024
    if gb > 1:
        return "{:.0f}GB".format(gb)
    return "{:.0f}MB".format(mb)

def print_order_results(results):
    data = ""
    for s in results:
        data += s + "\r\n"
    # 提取文件夹名称和大小信息并存储为元组列表
    folder_info_list = re.findall(r"文件夹\s+([^的]+)\s+的大小为:\s+(\d+\.?\d*)\s*(\w+)", data)
    # 根据文件夹大小排序
    sorted_folders = sorted(folder_info_list, key=lambda x: float(x[1]) * (1024 if x[2] == 'GB' else 1) if x[2] != 'MB' else float(x[1]), reverse=True)
    # 打印排序结果
    for name, size, unit in sorted_folders:
        print(f"文件夹 {name} 的大小为: {size} {unit}")



def get_folder_size(folder_path):
    total_size = 0
    try:
        with os.scandir(folder_path) as iterator:
            for entry in iterator:
                if entry.is_file():
                    total_size += entry.stat().st_size
                elif entry.is_dir():
                    total_size += get_folder_size(entry.path)
    except PermissionError:
        #print(f"无法访问文件夹 {folder_path}，权限不足")
        return total_size
    except FileNotFoundError:
        #print(f"无法访问当前目录 {folder_path} 下的文件夹，路径不存在")
        return total_size
    return total_size

def print_folder_sizes(base_path="."):
    total_size = 0
    with os.scandir(base_path) as iterator:
        for entry in iterator:
            if entry.name in white_names:
                continue
            if entry.is_dir():
                folder_size = get_folder_size(entry.path)
                # print(f"文件夹 {entry.name} 的大小为: {format_folder_size(folder_size)}")
                results.append(f"文件夹 {entry.name} 的大小为: {format_folder_size(folder_size)}")
                total_size += folder_size
    return total_size



def main():
    folder_path = input("请输入要遍历的文件夹路径（默认为当前目录）: ")
    
    if not folder_path:
        folder_path = "."

    if os.path.exists(folder_path):
        folder_size = print_folder_sizes(folder_path)
        # print(f"文件夹 {folder_path} 的大小为: {format_folder_size(folder_size)}")
        results.append(f"文件夹 {folder_path} 的大小为: {format_folder_size(folder_size)}")
    else:
        print("指定的文件夹路径不存在")

# windows 下文件夹快捷方式以后缀ink结果, 可以检查 entry.path, is_dir 的参数在 windows 下没用
if __name__ == "__main__":
    # 白名单, 跳过遍历
    white_names = ["$RECYCLE.BIN", "MSOCache", "System Volume Information"]
    # 结果
    results = []
    # 开始遍历
    main()
    # 输出结果
    print_order_results(results)
