# -*- coding:utf8 -*-

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from pay_flask import create_app, db

app = create_app('development')


# 数据迁移
manager = Manager(app)
# 将app与db关联
Migrate(app, db)
# 将迁移命令添加到manager中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
