from app import database


# 表： 页面表，维护Web自动化不同项目的页面
class WebPage(database.Model):
    __tablename__ = "t_web_page"

    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    page_name = database.Column(database.String(255), default=None, comment='页面名称')
    page_desc = database.Column(database.String(255), default=None, comment='页面描述')
    project_id = database.Column(database.Integer, nullable=False, comment='项目ID')
    # module_id = database.Column(database.Integer, nullable=False,comment='模块ID')
    create_time = database.Column(database.DateTime, default=None, comment='创建时间')