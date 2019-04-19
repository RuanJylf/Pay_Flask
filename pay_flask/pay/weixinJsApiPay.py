# -*- coding:utf8 -*-

from flask import request, jsonify, current_app, redirect
from utils.models import Orders
from utils.response_code import RET
from utils.weixin import *
from . import pay_blu


# 微信公众号支付: POST /api/pay/weixinJsApiPay
@pay_blu.route('/weixinJsApiPay', methods=["POST"])
def weixinJsApiPay():
    """
    微信公众号支付基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单信息
    4.微信公众号支付
    5.支付结果通知回调
    6.更新订单支付状态
    """

    # 1.获取参数
    orders_id = request.json.get("orders_id")
    get_info = request.json.get("get_info")
    # openid = request.cookies.get("openid")
    openid = request.json.get("openid")  # 模拟测试

    # 2.校验参数
    # 判断订单序号是否存在
    if not orders_id:
        data = {
        }
        return jsonify(code=RET.MISS, message="缺少参数", data=data)

    if not openid:
        # 未获取到openid
        if get_info == '0':
            # 构造一个url，携带一个重定向的路由参数，
            # 然后访问微信的一个url,微信会回调你设置的重定向路由，并携带code参数
            url = get_redirect_url()[0]
            return redirect(url)
        else:
            # 获取用户的openid
            urlinfo = get_redirect_url()[1]
            print("用户信息: %s" % urlinfo)
            code = urlinfo["response_type"]
            state = urlinfo["state"]
            openid = get_openid(code, state)

    # 3.查询订单信息
    try:
        order = Orders.query.filter(Orders.orders_id == orders_id).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 4.微信公众号支付
    # 获取支付订单参数
    params = get_jsapi_params(order, openid)
    print("参数字典: %s" % params)

    pay_param = {
        'appId': params['appid'],
        'timeStamp': params['time_stamp'],
        'nonceStr': params['nonce_str'],
        'package': params['package'],
        'signType': "MD5",
        'paySign': params['sign'],
    }
    print("支付参数: %s" % pay_param)

    # 利用支付参数拼接支付链接
    pay_url = "weixin://wxpay/bizpayurl?appid=%s&time_stamp=%s&nonce_str=%s&package=%s&sign_type=%s&pay_sign=%s" \
              % (pay_param['appId'], pay_param['timeStamp'], pay_param['nonceStr'],
                 pay_param['package'], pay_param['signType'], pay_param['paySign'])
    print("支付链接: %s" % pay_url)  # 测试输出
    # return redirect(pay_url)

    data = {
        "pay_param": pay_param
    }
    return jsonify(code=RET.OK, message="操作成功", data=data)


    # TODO 支付结果通知回调 notify

    # TODO 更新订单支付状态 update_status