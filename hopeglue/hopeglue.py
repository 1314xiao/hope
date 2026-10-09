#!/usr/bin/python
# _*_ coding: utf-8 _*_
# @Author: xiao hai
# @Time: 2026/10/5 18:21
# HopeGlue打包工具，方案1 Loader架构

import os
import struct
import zipfile
import sys


MAGIC = b"HOPEPKG"
MAGIC_LEN = 7
META_SIZE = 16  # 8字节env长度 + 8字节脚本长度

def make_env_zip(env_root: str, out_zip_path: str):
    with zipfile.ZipFile(out_zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(env_root, "hope.exe"), arcname="hope.exe")
        zf.write(os.path.join(env_root, "lib_config.hope"), arcname="lib_config.hope")

        lib_root = os.path.join(env_root, "Lib")
        for dirpath, _, files in os.walk(lib_root):
            for fn in files:
                fullp = os.path.join(dirpath, fn)
                arc = os.path.relpath(fullp, env_root)
                zf.write(fullp, arcname=arc)

        libs_root = os.path.join(env_root, "hope_libs")
        for dirpath, _, files in os.walk(libs_root):
            for fn in files:
                fullp = os.path.join(dirpath, fn)
                arc = os.path.relpath(fullp, env_root)
                zf.write(fullp, arcname=arc)

        internal_root = os.path.join(env_root, "_internal")
        for dirpath, _, files in os.walk(internal_root):
            for fn in files:
                fullp = os.path.join(dirpath, fn)
                arc = os.path.relpath(fullp, env_root)
                zf.write(fullp, arcname=arc)


def glue(loader_exe: str, hope_env_dir: str, script_file: str, output_exe: str):
    tmp_zip = "_env_temp.zip"
    make_env_zip(hope_env_dir, tmp_zip)

    with open(tmp_zip, "rb") as f:
        env_data = f.read()
    with open(script_file, "rb") as f:
        scr_data = f.read()

    env_len = len(env_data)
    scr_len = len(scr_data)

    with open(output_exe, "wb") as out:
        # 1. loader本体
        with open(loader_exe, "rb") as f:
            out.write(f.read())
        # 2. 环境zip
        out.write(env_data)
        # 3. 用户脚本
        out.write(scr_data)
        # 4. 元数据：env长度，脚本长度
        out.write(struct.pack(">QQ", env_len, scr_len))
        # 5. 唯一标记，放在文件最末尾
        out.write(MAGIC)

    os.remove(tmp_zip)
    print(f"✅打包完成: {output_exe}")
    print(f"✅内嵌完整运行环境 + 脚本: {script_file}")
    print(f"环境包大小: {env_len} bytes，脚本大小: {scr_len} bytes")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("用法: hopeglue.exe loader.exe 环境根目录 输入脚本.hope 输出.exe")
        print("示例: hopeglue.exe loader.exe D:\\hope 2.hope 2.exe")
        sys.exit(1)
    loader_path = sys.argv[1]
    env_path = sys.argv[2]
    script_path = sys.argv[3]
    out_exe_path = sys.argv[4]
    glue(loader_path, env_path, script_path, out_exe_path)

