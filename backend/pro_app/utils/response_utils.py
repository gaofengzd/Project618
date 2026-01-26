from flask import jsonify

def success_response(data=None, msg="操作成功"):
    """成功响应封装"""
    return jsonify({
        'code': 200,
        'msg': msg,
        'data': data or []
    })

def error_response(msg="操作失败", code=500):
    """失败响应封装"""
    return jsonify({
        'code': code,
        'msg': msg,
        'data': []
    })