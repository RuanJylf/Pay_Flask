# -*- coding:utf8 -*-

from flask import request, jsonify, current_app
from utils.models import Orders
from utils.response_code import RET
from . import pay_blu


# 无需支付的情况: POST /api/pay/skipThirdPay
@pay_blu.route('/skipThirdPay', methods=["POST"])
def skipThirdPay():
    """
    无需支付基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单支付信息
    4.判断支付金额与支付状态
    5.返回响应
    """

    # 1.获取参数: token, orders_id
    token = request.json.get("token")
    orders_id = request.json.get("orders_id")

    # 2.校验参数
    # 判断用户是否登陆
    if not token:
        return jsonify(code=RET.TOKENERR, message="用户未登陆")

    # 判断订单序号是否存在
    if not orders_id:
        data = {
        }
        return jsonify(code=RET.MISS, message="缺少参数", data=data)

    # 3.查询订单支付信息: 支付金额, 支付状态
    try:
        order = Orders.query.filter(Orders.orders_id == orders_id).first()
        pay_amount = order.pay_amount
        pay_status = order.pay_status
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 4.判断支付金额是否为0.00
    if pay_amount == "0.00" or pay_status == 1:
        # 如果支付金额为0.00, 或者订单支付状态为1已支付, 无需支付
        data = {
        }
        print("无需支付, 请前往商城选购商品！")
        return jsonify(code=RET.OK, message="操作成功", data=data)
    elif pay_amount != "0.00" and pay_status == 0:
        # 支付金额不为0.00, 支付状态为0未支付, 前往支付
        print("订单尚未支付, 请前往支付！")
        return jsonify(code=RET.OK, message="操作成功")
    else:
        # 订单参数错误
        return jsonify(code=RET.PARAMERR, message="参数错误")