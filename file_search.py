import os

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
    with os.scandir(base_path) as iterator:
        for entry in iterator:
            if entry.name in white_names:
                continue
            if entry.is_dir():
                folder_size = get_folder_size(entry.path)
                print(f"文件夹 {entry.name} 的大小为: {folder_size:.2f} MB")



def main():
    folder_path = input("请输入要遍历的文件夹路径（默认为当前目录）: ")
    
    if not folder_path:
        folder_path = "."

    if os.path.exists(folder_path):
        # folder_size = get_folder_size(folder_path)
        # print(f"文件夹 {folder_path} 的大小为: {folder_size:.2f} MB")
        # print("各子文件夹的大小：")
        print_folder_sizes(folder_path)
    else:
        print("指定的文件夹路径不存在")

# windows 下文件夹快捷方式以后缀ink结果, 可以检查 entry.path, is_dir 的参数在 windows 下没用
if __name__ == "__main__":
    # 白名单, 跳过遍历
    white_names = ["$RECYCLE.BIN", "MSOCache", "System Volume Information"]
    main()
