from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from errors import InterpreterError

# url_get(url)：发送GET请求，返回网页的文本内容
def urllib_get_func(args):
    if len(args) != 1:
        raise InterpreterError("url_get函数需要1个参数：url_get(网址)")
    url = args[0]
    if not isinstance(url, str):
        raise InterpreterError("url_get函数的参数必须是字符串")
    try:
        with urlopen(url, timeout=10) as response:
            # 自动识别编码
            content = response.read()
            encoding = response.headers.get_content_charset() or "utf-8"
            return content.decode(encoding)
    except HTTPError as e:
        raise InterpreterError(f"HTTP请求错误：{e.code} {e.reason}")
    except URLError as e:
        raise InterpreterError(f"网络请求错误：{str(e.reason)}")
    except Exception as e:
        raise InterpreterError(f"请求失败：{str(e)}")

# url_get_bytes(url)：发送GET请求，返回原始的字节内容
def urllib_get_bytes_func(args):
    if len(args) != 1:
        raise InterpreterError("url_get_bytes函数需要1个参数：url_get_bytes(网址)")
    url = args[0]
    if not isinstance(url, str):
        raise InterpreterError("url_get_bytes函数的参数必须是字符串")
    try:
        with urlopen(url, timeout=10) as response:
            return response.read()
    except HTTPError as e:
        raise InterpreterError(f"HTTP请求错误：{e.code} {e.reason}")
    except URLError as e:
        raise InterpreterError(f"网络请求错误：{str(e.reason)}")
    except Exception as e:
        raise InterpreterError(f"请求失败：{str(e)}")

# 原有函数保留，新增POST相关函数
# --------------------------
# url_post(url, data)：发送POST请求，data是字典格式的请求参数，返回网页文本内容
def urllib_post_func(args):
    if len(args) != 2:
        raise InterpreterError("url_post函数需要2个参数：url_post(网址, 请求参数字典)")
    url, data = args[0], args[1]
    if not isinstance(url, str):
        raise InterpreterError("url_post函数的网址参数必须是字符串")
    if not isinstance(data, dict):
        raise InterpreterError("url_post函数的请求参数必须是字典")

    try:
        # 把字典参数编码为表单格式
        encoded_data = urlencode(data).encode('utf-8')
        # 创建Request对象，设置请求头
        req = Request(
            url,
            data=encoded_data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "User-Agent": "Hope Interpreter Urllib/1.0"
            }
        )
        with urlopen(req, timeout=10) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding)
    except HTTPError as e:
        raise InterpreterError(f"HTTP请求错误：{e.code} {e.reason}")
    except URLError as e:
        raise InterpreterError(f"网络请求错误：{str(e.reason)}")
    except Exception as e:
        raise InterpreterError(f"POST请求失败：{str(e)}")

# url_post_json(url, json_data)：发送JSON格式的POST请求，json_data是字典
def urllib_post_json_func(args):
    if len(args) != 2:
        raise InterpreterError("url_post_json函数需要2个参数：url_post_json(网址, JSON字典)")
    url, json_data = args[0], args[1]
    if not isinstance(url, str):
        raise InterpreterError("url_post_json函数的网址参数必须是字符串")
    if not isinstance(json_data, dict):
        raise InterpreterError("url_post_json函数的JSON参数必须是字典")

    try:
        import json
        # 把字典转成JSON字符串并编码
        json_str = json.dumps(json_data).encode('utf-8')
        req = Request(
            url,
            data=json_str,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": "Hope Interpreter Urllib/1.0"
            }
        )
        with urlopen(req, timeout=10) as response:
            encoding = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(encoding)
    except ImportError:
        raise InterpreterError("当前环境不支持JSON处理")
    except HTTPError as e:
        raise InterpreterError(f"HTTP请求错误：{e.code} {e.reason}")
    except URLError as e:
        raise InterpreterError(f"网络请求错误：{str(e.reason)}")
    except Exception as e:
        raise InterpreterError(f"JSON POST请求失败：{str(e)}")

# 更新URLLIB_FUNCTIONS，加入新增的POST函数
URLLIB_FUNCTIONS = {
    # 定义urllib库的函数列表，遵循统一格式
    "url_get": (["url"], urllib_get_func),
    "url_get_bytes": (["url"], urllib_get_bytes_func),
    "url_get": (["url"], urllib_get_func),
    "url_get_bytes": (["url"], urllib_get_bytes_func),
    # 新增的POST请求函数
    "url_post": (["url", "data"], urllib_post_func),
    "url_post_json": (["url", "json_data"], urllib_post_json_func)
}