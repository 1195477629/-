from app import database


# 表：单个测试用例对应的前置用例表
class WebInfoPre(database.Model):
    __tablename__ = "t_web_info_pre"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    web_info_id = database.Column(database.Integer, comment='当前用例ID')
    pre_info_id = database.Column(database.Integer, comment='前置用例ID')
    # param_data = database.Column(database.String(255), comment='参数')
    run_order = database.Column(database.Integer, comment='执行顺序')
    create_time = database.Column(database.DateTime)