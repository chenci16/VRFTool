import logging
import logging.handlers
import os

log = logging.getLogger("INFO")


def init_log():
    log_path = os.getcwd() + "/var/log"
    try:
        if not os.path.exists(log_path):
            os.makedirs(log_path)
    except:
        print("创建日志目录失败")
        exit(1)
    if len(log.handlers) == 0:  # 避免重复
        # 2.创建handler(负责输出，输出到屏幕streamhandler,输出到文件filehandler)
        filename = os.path.join(log_path, 'Client.log')
        fh = logging.FileHandler(filename, mode="a", encoding="utf-8")  # 默认mode 为a模式，默认编码方式为utf-8
        sh = logging.StreamHandler()
        # 3.创建formatter：
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - Model:%(filename)s - Fun:%(funcName)s - Message:%(message)s - Line:%(lineno)d')
        # 4.绑定关系：①logger绑定handler
        log.addHandler(fh)
        log.addHandler(sh)
        # # ②为handler绑定formatter
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        # # 5.设置日志级别(日志级别两层关卡必须都通过，日志才能正常记录)
        log.setLevel(logging.INFO)
        fh.setLevel(logging.INFO)
        sh.setLevel(logging.INFO)


init_log()
