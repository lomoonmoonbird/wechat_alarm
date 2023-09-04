import time
import traceback
from functools import wraps
from flask import make_response, jsonify, request

from app import app
from runserver import logging


class ClientError(Exception):
    pass

def get_res_message(message, status_code, content=None):
    # 异常处理信息函数，默认content为空
    res_data = {
        "code": status_code,
        "message": message,
        "data": content,
    }
    res = jsonify(res_data)
    res.headers['date'] = time.strftime("%Y-%m-%d %H:%M:%S %a UTF", time.localtime())
    return res


# 异常检测
def check_exception_time(f):
    @wraps(f)
    def check(*args, **kwargs):
        try:
            res = f(*args, **kwargs)
            return res
        except ClientError as e:
            # 以下是异常简要
            # 此处需要用到traceback模块捕获具体异常，以便展示具体的错误位置。以下是格式化后的具体异常
            exception_desc = str(e)
            traceback.print_exc()
            # 以下字典格式不能http返回，所以需要转换成str,提前将traceback.format_exc()也转换成str，否则返回字符串没有引号
            res_data = {
                "code": 400,
                "message": exception_desc,
                "data": str(traceback.format_exc()),
            }
            return make_response(str(res_data))
        except Exception as e:
            res_data = {
                "code": 400,
                "message": '未知异常',
                "data": str(traceback.format_exc()),
            }
            traceback.print_exc()
            return make_response(str(res_data))

    return check

# 定义错误处理的方法
@app.errorhandler(404)
def handle_404_error(err):
    """自定义的处理错误方法"""
    # 这个函数的返回值会是前端用户看到的最终结果
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    # return jsonify({'ip': ip}), 200
    print('ip:{}'.format(ip))
    logging.debug('ip为{}的用户访问url'.format(ip))
    return "出现了404错误， 错误信息：%s" % err
