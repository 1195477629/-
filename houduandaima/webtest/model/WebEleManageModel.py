from app import database


# 表： 元素管理表，根据不同的项目-页面-维护对应的元素及定位方式
class WebEleManage(database.Model):
    __tablename__ = "t_web_ele"
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(255), comment='元素名称')
    location_method_id = database.Column(database.Integer, nullable=False, comment='元素定位方式ID')
    ele_location_exp = database.Column(database.String(255), default=None, comment='定位元素表达式')
    project_id = database.Column(database.Integer, nullable=False, comment='项目ID')
    page_id = database.Column(database.Integer, nullable=False, comment='页面ID')
    ele_desc = database.Column(database.String(255), default=None, comment='元素描述')
    create_time = database.Column(database.DateTime, default=None)