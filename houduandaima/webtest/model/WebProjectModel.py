from app import database


# 表： 项目表，维护Web自动化的项目
class WebProject(database.Model):
    __tablename__ = "t_web_project"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    project_name = database.Column(database.String(255), comment='项目名称')
    project_desc = database.Column(database.String(255), comment='项目描述')
    create_time = database.Column(database.DateTime, comment='创建时间')
