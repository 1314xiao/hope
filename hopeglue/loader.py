#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2026/10/5 18:21
# Hope Loader 外层启动器

import sys
import os
import struct
import tempfile
import subprocess
import zipfile
import shutil


MAGIC = b"HOPEPKG"
MAGIC_LEN = 7
META_SIZE = 16

def read_package(exe_path:str):
    with open(exe_path, "rb") as f:
        f.seek(0, os.SEEK_END)
        total_size = f.tell()
        # 定位到MAGIC起始位置
        magic_pos = total_size - MAGIC_LEN
        f.seek(magic_pos)
        magic_buf = f.read(MAGIC_LEN)
        if magic_buf != MAGIC:
            print("ERROR: HOPEPKG magic not found")
            return None, None
        # 读取前面16字节：env_len, script_len
        meta_pos = magic_pos - META_SIZE
        f.seek(meta_pos)
        env_len, scr_len = struct.unpack(">QQ", f.read(META_SIZE))
        # 计算env、script的起始偏移
        scr_start = meta_pos - scr_len
        env_start = scr_start - env_len
        # 读取环境zip
        f.seek(env_start)
        env_bytes = f.read(env_len)
        # 读取脚本
        f.seek(scr_start)
        scr_bytes = f.read(scr_len)
    return env_bytes, scr_bytes


def main():
    exe_file = sys.executable
    env_zip_bytes, script_bytes = read_package(exe_file)
    if env_zip_bytes is None or script_bytes is None:
        input("pause")
        sys.exit(1)

    tmp_base = tempfile.mkdtemp()
    try:
        env_dir = os.path.join(tmp_base, "hope_env")
        os.makedirs(env_dir)
        zip_fd, zip_tmp = tempfile.mkstemp(suffix=".zip")
        os.close(zip_fd)
        with open(zip_tmp, "wb") as fw:
            fw.write(env_zip_bytes)
        with zipfile.ZipFile(zip_tmp, "r") as zf:
            zf.extractall(env_dir)
        os.remove(zip_tmp)

        script_path = os.path.join(tmp_base, "main.hope")
        with open(script_path, "wb") as fw:
            fw.write(script_bytes)

        hope_bin = os.path.join(env_dir, "hope.exe")
        if not os.path.isfile(hope_bin):
            print("ERROR: hope.exe missing in embedded env")
            input("pause")
            sys.exit(1)

        proc = subprocess.run([hope_bin, script_path], cwd=env_dir)
        sys.exit(proc.returncode)
    finally:
        shutil.rmtree(tmp_base, ignore_errors=True)


if __name__ == "__main__":
    main()
