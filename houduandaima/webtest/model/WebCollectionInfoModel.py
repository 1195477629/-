from app import database

# 表：测试集，根据对应的测试用例去组装成对应的测试用例集
class WebCollectionInfo(database.Model):
    __tablename__ = "t_web_collection_info"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    project_id = database.Column(database.Integer, default=None,comment='项目ID')
    collection_name = database.Column(database.String(255), default=None,comment='测试集合名称' )
    collection_desc = database.Column(database.String(255), default=None,comment='测试集合描述')
    collection_env = database.Column(database.String(255), default=None,comment='测试集合全局变量')
    browser_id = database.Column(database.Integer, default=None,comment='浏览器ID')
    create_time = database.Column(database.DateTime, default=None)
