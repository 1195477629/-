# 开发环境--需要的配置
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:4940110@localhost:3306/platfrom?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 打印sql语句
SQLALCHEMY_ECHO = True
SECRET_KEY = "1234567812345678"


#WEB自动化的路径
KEY_WORDS_DIR = r"/keyswords" # 关键字生成的文件夹
CASES_ROOT_WEB_DIR = r"/yamls" # 测试用例生成的文件夹

# 测试报告存放的路径
CASES_ROOT_DIR = r"/report_dir" # 用例数据文件夹
REPORT_ROOT_DIR = r"/report"   # 用例报告文件夹