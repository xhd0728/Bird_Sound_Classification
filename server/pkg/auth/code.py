import random

import redis

from config.redis import *
from pkg.auth.email import send_email

redis_conn = redis.Redis(REDIS_HOST, REDIS_PORT)


def check_busy(email):
    ttl = redis_conn.ttl(email)
    if ttl and ttl > 240:
        return True
    return False


def cache_code(email, code):
    redis_conn.set(email, code, ex=300)  # 五分钟过期时间


def send_code(email):
    busy = check_busy(email)  # 发送邮件过于频繁
    if busy:
        return False, "发送邮件过于频繁"
    code = "".join(random.choices("1234567890", k=6))
    data = {"code": code}
    try:
        send_email(email, category="send-code", data=data)
    except:
        return False, "系统繁忙或邮件地址有误，请确认后再重试"
    cache_code(email, code)
    return True, "成功发送邮件"


def check_code(email, code):
    if not isinstance(code, str):
        return False
    if len(code) != 6 or not code.isdigit():
        return False
    redis_code = redis_conn.get(email)
    if not redis_code:
        return False
    result = bool(str(redis_conn.get(email).decode('utf8')) == code)
    return result
