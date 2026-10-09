from hope_sdk_client import HopeSdkClient

def main():
    client = HopeSdkClient(r"hope.exe")

    hope_source = """
func add(x, y) {
    return x + y
}

func multiply(x, y) {
    return x * y
}

func calc(x, y) {
    set sum_val = add(x, y)
    set diff_val = add(x, multiply(y, 1)) 
    return multiply(sum_val, diff_val)
}
"""
    print("=== 加载Hope函数(add/multiply/calc) ===")
    client.run_code(hope_source)

    # 调用calc，计算公式 (x+y)*(x+(y*1))
    x, y = 3, 4
    calc_result = client.call("calc", x, y)
    print(f"Hope calc({x},{y}) = (x+y)*(x+(y*1)) = {calc_result}")

    client.close()
    print("\n=== 程序结束，SDK正常退出 ===")

if __name__ == "__main__":
    main()
