# -*- coding:utf8 -*-

from flask import request, jsonify, current_app, redirect
from pay_flask import alipay
from utils.models import Orders
from utils.response_code import RET
from . import pay_blu


# 支付宝手机网页支付: POST /api/pay/aliWapPay
@pay_blu.route('/aliWapPay', methods=["POST"])
def aliWapPay():
    """
    支付宝手机网页支付基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单支付信息
    4.支付宝手机网页支付
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

    # 判断订单序号是否存在
    if not orders_id:
        data={
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

    # 4.支付宝手机网页支付
    # 构造支付宝支付信息字符串
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order_no,  # 订单编号
        total_amount=str(pay_amount),  # 支付金额
        subject="蒲公英-商城购物",  # 订单主题
        return_url="http://pgy.lingxiu.top/QDYM/orderList.html",  # 支付成功后的回调地址
        notify_url=None  # 支付结果通知地址, 可选, 不填则使用默认notify_url
    )

    # 利用订单支付参数字符串拼接网页支付链接网址
    pay_url = "https://openapi.alipaydev.com/gateway.do" + "?" + order_string
    print("支付链接: %s" % pay_url)  # 测试输出

    # return redirect(pay_url)  # 重定向到支付网页地址

    data = {
        "pay_url": pay_url
    }
    return jsonify(code=RET.OK, message="操作成功", data=data)


# 支付宝网页支付结果通知回调 notify
@pay_blu.route('/aliNotify', methods=["GET", "POST"])
def aliNotify():
    """支付宝支付结果通知回调"""

    data = request.form.to_dict()

    # sign 不能参与签名验证
    signature = data.pop("sign")
    print(signature)

    # 3.查询订单支付信息: 订单编号, 支付金额
    try:
        order = Orders.query.filter(Orders.order_no == data.get("out_trade_no")).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 支付状态验证
    success = alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        # 更新订单支付状态
        order.pay_status = 1
        print("支付成功！")
    else:
        print("尚未支付！")
