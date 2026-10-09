from hope_sdk_client import HopeSdkClient

# 传入exe路径
client = HopeSdkClient(r"hope.exe")

# 执行hope源码,自定义函数
client.run_code("""
func my_func(a,b,c) {
    return a+b+c
}
""")

# 调用函数
my=client.call("my_func", 1, 2, 3)
print(my)

# 设置全局变量
client.set_global("name", "hope")

# 读取全局变量
val = client.get_global("name")
print(val)

client.close()
