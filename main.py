import os

input_root = "D:\\doc\\示范\\dfmfj\\root"
out_root = "D:\\doc\\示范\\dfmfj"


def start_format():
    for filepath, dirnames, filenames in os.walk(input_root):
        for filename in filenames:
            print(filepath.replace(input_root,"")+'\\'+filename)


if __name__ == '__main__':
    start_format()

