# -*- coding:utf8 -*-

from pay_flask import db


# Mysql数据库模型类
class Orders(db.Model):
    """订单"""

    __tablename__ = "md_orders"

    # 定义订单表中各字段约束
    orders_id = db.Column(db.Integer, primary_key=True)  # 订单序号
    order_no = db.Column(db.Integer, nullable=False)  # 订单编号
    pay_amount = db.Column(db.DECIMAL, nullable=False)  # 支付金额
    pay_status = db.Column(db.SmallInteger, nullable=False, default=0)   # 支付状态
