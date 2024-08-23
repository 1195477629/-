# 用来专门查看报告的
from flask import Blueprint, request
from core.resp_model import respModel
from app import database, application
from datetime import datetime
from flask import send_from_directory


# 模块信息
module_name = "WebReportViewer"  # 模块名称
module_route = Blueprint(f"route_{module_name}", __name__)

@module_route.route(f'/{module_name}/<path:dir>/<filename>',methods=["GET"])
def report_viewer(dir, filename):
    report_root_dir = application.config['REPORT_ROOT_DIR']
    return send_from_directory(f"{report_root_dir}/{dir}/", filename)