from flask import Blueprint, request
from core.resp_model import respModel
from app import database, application
from webtest.model.WebDbBaseModel import WebDbBase  # 请替换为你的ApiModule模型类
from datetime import datetime

# 模块信息
module_name = "WebDbBase"  # 模块名称
module_model = WebDbBase
module_route = Blueprint(f"route_{module_name}", __name__)


@module_route.route(f"/{module_name}/queryByPage", methods=["POST"])
def queryByPage():
    """ 查询数据(支持模糊搜索) """
    try:
        # 分页查询
        page = int(request.json["page"])
        page_size = int(request.json["pageSize"])
        with application.app_context():
            filter_list = []
            # 添加 项目筛选条件
            project_id = request.json.get("project_id", 0)
            if type(project_id) is not str and project_id > 0:
                filter_list.append(module_model.project_id == project_id)
            # 添加模块名称模糊搜索条件
            connect_name = request.json.get("connect_name", "")
            if len(connect_name) > 0:
                filter_list.append(module_model.connect_name.like(f'%{connect_name}%'))
            #  是否启动该数据库
            is_enabled = request.json.get("is_enabled", "")
            if len(is_enabled) > 0:
                filter_list.append(module_model.is_enabled.like(f'%{is_enabled}%'))
            # 数据库查询
            datas = module_model.query.filter(*filter_list).limit(page_size).offset((page - 1) * page_size).all()
            total = module_model.query.filter(*filter_list).count()
            return respModel().ok_resp_list(lst=datas, total=total)
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")

@module_route.route(f"/{module_name}/queryById", methods=["GET"])
def queryById():
    """ 查询数据(单条记录) """
    try:
        data_id = int(request.args.get("id"))
        with application.app_context():
            # 数据库查询
            data = module_model.query.filter_by(id=data_id).first()
        if data:
            return respModel().ok_resp(obj=data)
        else:
            return respModel.ok_resp(msg="查询成功,但是没有数据")
    except Exception as e:
        print(e)
        return respModel.error_resp(f"服务器错误,请联系管理员:{e}")

# @module_route.route(f"/{module_name}/insert", methods=["POST"])
# def insert():
#     """ 新增数据 """
#     try:
#         with application.app_context():
#             request.json["id"] = None  # ID自增长
#             data = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
#             database.session.add(data)
#             # 获取新增后的ID并返回
#             database.session.flush()
#             data_id = data.id
#             database.session.commit()
#         return respModel.ok_resp(msg="添加成功", dic_t={"id": data_id})
#     except Exception as e:
#         print(e)
#         return respModel.error_resp(msg=f"添加失败:{e}")

@module_route.route(f"/{module_name}/insert", methods=["POST"])
def insert():
    """ 新增数据 """
    try:
        with application.app_context():
            request.json["id"] = None  # ID自增长

            ref_name = request.json["ref_name"]  # 引用名称名获取
            # 进行查询确定是否有引用名称数据
            data = module_model.query.filter_by(ref_name=ref_name).first()
                
            if data:
                # 如果有数据则提示用户：引用名称重复
                return respModel.error_resp(msg="数据库已存在重复的关键字方法，请重新输入。")
            else:
                data = module_model(**request.json, create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
                database.session.add(data)
                # 获取新增后的ID并返回
                database.session.flush()
                data_id = data.id
                database.session.commit()
        return respModel.ok_resp(msg="添加成功", dic_t={"id": data_id})
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"添加失败:{e}")

@module_route.route(f"/{module_name}/update", methods=["PUT"])
def update():
    """ 修改数据 """
    try:
        with application.app_context():
            module_model.query.filter_by(id=request.json["id"]).update(request.json)
            database.session.commit()
        return respModel.ok_resp(msg="修改成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"修改失败，请联系管理员:{e}")


@module_route.route(f"/{module_name}/delete", methods=["DELETE"])
def delete():
    """ 删除数据 """
    try:
        with application.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            database.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")
