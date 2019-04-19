# -*- coding:utf8 -*-

from flask import request, jsonify, current_app
from utils.models import Orders
from utils.response_code import RET
from utils.weixin import *
from . import pay_blu


# 微信扫码支付: POST /api/pay/weixinQrPay
@pay_blu.route('/weixinQrPay', methods=["POST"])
def weixinQrPay():
    """
    微信扫码支付基本逻辑
    1.获取参数
    2.校验参数
    3.查询订单支付信息
    4.微信扫码支付
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

    # 3.查询订单信息: 订单编号
    try:
        order = Orders.query.filter(Orders.orders_id == orders_id).first()
        order_no = order.order_no
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(code=RET.DBERR, message="数据库查询错误")

    # 4.微信扫码支付
    # 获取微信扫码支付订单参数
    params = get_native_params(order)
    print("参数字典: %s" % params)

    # 模拟测试
    pay_dict = {
        'appid': APP_ID,  # 公众账号ID
        'mch_id': MCH_ID,  # 商户号
        'nonce_str': random_str(16),  # 随机字符串
        'time_stamp': int(time.time()),  # 时间戳
        'product_id': order_no,  # 商品信息或订单编号
        'sign': params['sign'],
    }

    # 利用支付参数拼接支付链接
    pay_dict['code_url'] = "weixin://wxpay/bizpayurl?appid=%s&mch_id=%s&nonce_str=%s&product_id=%s&time_stamp=%s&sign=%s" \
          % (pay_dict['appid'], pay_dict['mch_id'], pay_dict['nonce_str'], pay_dict['product_id'], pay_dict['time_stamp'],
             pay_dict['sign'])
    pay_dict['return_code'] = "SUCCESS" if pay_dict['code_url'] else "Fail"

    # xml = trans_dict_to_xml(params)  # 转换字典为XML
    # response = requests.request('post',UFDODER_URL, data=xml)  # 以POST方式向微信公众平台服务器发起请求
    # pay_dict = trans_xml_to_dict(response.content)  # 将请求返回的数据转换为字典
    print("回调字典: %s" % pay_dict)

    # 生成微信扫码支付链接， 必须在微信客户端打开
    code_url = pay_dict.get('code_url')
    print("支付链接: %s" % code_url)
    if pay_dict.get('return_code') == 'SUCCESS':  # 如果请求成功
        # 利用支付链接生成二维码
        img_url = create_qrcode(order_no, code_url)
        print("二维码地址: %s" % img_url)  # 测试输出

        data = {
            "qrcode": img_url
        }
        return jsonify(code=RET.OK, message="操作成功", data=data)
    else:
        # return_code = Fail, 获取code_url失败
        return jsonify(code=RET.URLERR, message="获取url失败")


    # TODO 支付结果通知回调 notify

    # TODO 更新订单支付信息 update_status

