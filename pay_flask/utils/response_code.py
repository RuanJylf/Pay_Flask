# -*- coding:utf8 -*-

# 自定义错误状态码

class RET:

    OK                  = 1
    MISS                = 0
    TOKENERR            = 100
    FAIL                = 101
    SUCCESS             = 102
    PARAMERR            = 103
    DBERR               = 104
    OPENIDERR           = 105
    URLERR              = 106


error_map = {

    RET.OK                    : u"操作成功",
    RET.MISS                  : u"缺少参数",
    RET.TOKENERR              : u"用户未登陆",
    RET.FAIL                  : u"支付失败",
    RET.SUCCESS               : u"支付成功",
    RET.PARAMERR              : u"参数错误",
    RET.DBERR                 : u"数据库查询错误",
    RET.OPENIDERR             : u"获取用户openid失败",
    RET.URLERR                : u"获取url失败",

}
