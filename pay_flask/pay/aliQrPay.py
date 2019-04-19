# -*- coding:utf8 -*-

import os
import time

import qrcode

from flask import request, jsonify, current_app
from pay_flask import alipay
from utils.models import Orders
from utils.response_code import RET
from . import pay_blu


# 支付宝扫码支付: POST /api/pay/aliQrPay
@pay_blu.route('/aliQrPay', methods=["POST"])
def aliQrPay():
    """
    支付宝扫码支付基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单支付信息
    4.支付宝扫码支付
    5.支付结果通知回调
    6.更新订单支付状态
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
        data = {
        }
        return jsonify(code=RET.MISS, message="缺少参数", data=data)

    # 3.查询订单支付信息: 订单编号, 支付金额
    try:
        order = Orders.query.filter(Orders.orders_id == orders_id).first()
        order_no = order.order_no
        pay_amount = order.pay_amount
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 4.支付宝扫码支付, 返回支付二维码图片地址
    # 生成预付订单信息, 交易预创建
    result = alipay.api_alipay_trade_precreate(
        subject="蒲公英-商城购物",
        out_trade_no=order_no,
        total_amount=str(pay_amount),
    )
    # 获取预付订单支付url
    code_url = result.get('qr_code')
    print(code_url)

    # 由预付订单url生成支付二维码
    qrcode_name = "alipay_" + order_no + ".png"  # 二维码图片名称
    img = qrcode.make(code_url)  # 生成二维码图片
    img_url = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) +'/images/' + qrcode_name
    img.save(img_url)  # 保存图片
    print("图片地址: %s" % img_url)  # 测试输出

    # 支付宝扫码支付结果通知回调
    # 检查订单状态
    paid = False
    for i in range(10):
        # 每3s检查一次， 共检查10次
        print("等待 3s")
        time.sleep(3)
        result = alipay.api_alipay_trade_query(out_trade_no=order_no)
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            paid = True
            # 更新订单支付信息
            order.pay_status = 1
            print("支付成功！")
            break
        print("尚未支付！")

    # 30s内未支付, 取消订单
    if paid is False:
        alipay.api_alipay_trade_cancel(out_trade_no=order_no)

    data = {
        "qrcode": img_url
    }
    return jsonify(code=RET.OK, message="操作成功", data=data)

