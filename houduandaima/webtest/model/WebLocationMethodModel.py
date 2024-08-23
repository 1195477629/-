from app import database


# 表： 定位方式表，比如：ID,XPath...
class WebLocationMethod(database.Model):
    __tablename__ = "t_web_ele_location"
    id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    location_method_name = database.Column(database.String(255))
    location_method_desc = database.Column(database.String(255))
    create_time = database.Column(database.DateTime)