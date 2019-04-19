# -*- coding:utf8 -*-

from flask import Blueprint

# 创建蓝图，并设置蓝图前缀

pay_blu = Blueprint("pay", __name__, url_prefix='/api/pay')

from . import aliWapPay, aliQrPay, weixinJsApiPay, weixinQrPay, skipThirdPay, checkPayStatus
