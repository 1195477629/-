# 镜像 ：  https://pypi.tuna.tsinghua.edu.cn/simple
# 准备的包： flask flask_sqlalchemy flask_script pymysql flask_cors
# flask == 2.0.2
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# 创建 flask 实例

application = Flask(__name__)
application.config.from_pyfile('config/dev_settings.py')  # 加载配置
CORS(application, resources=r'/*')
database = SQLAlchemy()
database.init_app(application)
jwt = JWTManager()  # jwt 用来生成token
jwt.init_app(application)

# 启动程序
if __name__ == '__main__':
    try:
        # 注册模块的接口路由信息
        from login.api import LoginController
        application.register_blueprint(LoginController.module_route)

        from sysmanage.api import UserController
        application.register_blueprint(UserController.module_route)

        from webtest.api import WebProjectContoller
        application.register_blueprint(WebProjectContoller.module_route)

        from webtest.api import WebDbBaseController
        application.register_blueprint(WebDbBaseController.module_route)

        from webtest.api import WebBrowserController
        application.register_blueprint(WebBrowserController.module_route)

        from webtest.api import WebKeyWordController
        application.register_blueprint(WebKeyWordController.module_route)

        from webtest.api import WebOperationTypeController
        application.register_blueprint(WebOperationTypeController.module_route)

        from webtest.api import WebInfoController
        application.register_blueprint(WebInfoController.module_route)

        from webtest.api import WebInfoStepContoller
        application.register_blueprint(WebInfoStepContoller.module_route)

        from webtest.api import WebReportViewerContoller
        application.register_blueprint(WebReportViewerContoller.module_route)
        
        from webtest.api import WebCollectionInfoController
        application.register_blueprint(WebCollectionInfoController.module_route)

        from webtest.api import WebCollectionDetailController
        application.register_blueprint(WebCollectionDetailController.module_route)

        from webtest.api import WebHistoryController
        application.register_blueprint(WebHistoryController.module_route)

        from webtest.api import WebInfoPreController
        application.register_blueprint(WebInfoPreController.module_route)

        from webtest.api import WebPageController
        application.register_blueprint(WebPageController.module_route)

        from webtest.api import WebLocationMethodController
        application.register_blueprint(WebLocationMethodController.module_route)

        from webtest.api import WebEleManageController
        application.register_blueprint(WebEleManageController.module_route)
        
        # 启动程序
        import sys

        sys.exit(application.run())
    except Exception as e:
        import traceback
        traceback.print_exc()
