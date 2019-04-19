# -*- coding:utf8 -*-

from flask import request, jsonify, current_app
from utils.models import Orders
from utils.response_code import RET
from . import pay_blu


# 支付检测: POST /api/pay/checkPayStatus
@pay_blu.route('/checkPayStatus', methods=["POST"])
def checkPayStatus():
    """
    支付检测基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单支付信息
    4.判断订单支付状态
    5.返回订单支付状态
    """

    # 1.获取参数
    token = request.json.get("token")
    orders_id = request.json.get("orders_id")

    # 2.校验参数
    # 判断用户是否登陆
    if not token:
        return jsonify(code=RET.TOKENERR, message="用户未登陆")

    # 判断订单id是否存在
    if not orders_id:
        return jsonify(code=RET.MISS, message="缺少参数")

    # 3.查询订单支付信息: 支付状态
    try:
        order = Orders.query.filter(Orders.orders_id == orders_id).first()
        pay_status = order.pay_status
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 4.判断订单支付状态
    if pay_status in [0, 1]:
        data = {
            "pay_status": pay_status
        }
        # 返回支付状态
        print("支付状态: %s" % pay_status)  # 测试输出

        # 模拟测试
        if pay_status:
            # 支付状态为1, 已支付
            print("订单已支付！")
        else:
            # 支付状态为0, 未支付
            print("订单未支付！")
        return jsonify(code=RET.OK, message="操作成功", data=data)
    else:
        # 支付状态参数错误
        return jsonify(code=RET.PARAMERR, message="参数错误")
