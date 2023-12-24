import os

def get_folder_size(folder_path):
    total_size = 0
    with os.scandir(folder_path) as iterator:
        for entry in iterator:
            if entry.is_file():
                total_size += entry.stat().st_size
            elif entry.is_dir():
                total_size += get_folder_size(entry.path)
    return total_size

def print_folder_sizes(base_path="."):
    with os.scandir(base_path) as iterator:
        for entry in iterator:
            if entry.is_dir():
                folder_size = get_folder_size(entry.path)
                print(f"文件夹 {entry.name} 的大小为: {folder_size/1024/1024:.2f} MB")

def main():
    folder_path = input("请输入要遍历的文件夹路径（默认为当前目录）: ")
    
    if not folder_path:
        folder_path = "."

    if os.path.exists(folder_path):
        folder_size = get_folder_size(folder_path)
        print(f"文件夹 {folder_path} 的大小为: {folder_size/1024/1024:.2f} MB")
        print("各子文件夹的大小：")
        print_folder_sizes(folder_path)
    else:
        print("指定的文件夹路径不存在")

if __name__ == "__main__":
    main()
