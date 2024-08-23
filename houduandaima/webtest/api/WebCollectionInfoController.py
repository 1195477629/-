from flask import Blueprint, request
from core.resp_model import respModel
from app import database, application
from webtest.model.WebCollectionInfoModel import WebCollectionInfo  # 修改导入的模型类
from datetime import datetime


module_name = "WebCollectionInfo"  # 模块名称
module_model = WebCollectionInfo
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
            # ====筛选条件(如果有筛选条件，在这里拓展 - filter)
            # 添加名称模糊搜索条件
            collection_name = request.json.get("collection_name", "")
            if len(collection_name) > 0:
                filter_list.append(module_model.collection_name.like(f'%{collection_name}%'))
            # 添加 项目筛选条件
            project_id = request.json.get("project_id", 0)
            if type(project_id) is not str and project_id > 0:
                filter_list.append(module_model.project_id == project_id)
            # =====结束
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


@module_route.route(f"/{module_name}/insert", methods=["POST"])
def insert():
    """ 新增数据 """
    try:
        with application.app_context():
            request.json["id"] = None  # ID自增长
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
    """ 删除数据  删除的同时，需要处理掉中间表"""
    try:
        with application.app_context():
            module_model.query.filter_by(id=request.args.get("id")).delete()
            database.session.commit()
        return respModel.ok_resp(msg="删除成功")
    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"服务器错误,删除失败：{e}")


# 扩展接口 - 执行用例接口
# 这里开始远程调用逻辑，生成两个文件夹,文件夹名字用UUID为后缀
import json, os, subprocess, uuid, yaml
# 模块信息,依次导入的包
from webtest.model.WebBrowserModel import WebBrowser
from webtest.model.WebDbBaseModel import WebDbBase  
from webtest.model.WebCollectionDetailModel import WebCollectionDetail
from webtest.model.WebInfoModel import WebInfo
from webtest.model.WebInfoStepModel import WebInfoStep  
from webtest.model.WebKeyWordModel import WebKeyWord
# 历史记录模块
from webtest.model.WebHistoryModel import WebHistoryModel

# 扩展功能：
from webtest.model.WebInfoPreModel import WebInfoPre
from webtest.model.WebPageModel import WebPage
from webtest.model.WebEleManageModel import WebEleManage
from webtest.model.WebLocationMethodModel import WebLocationMethod
import hashlib

@module_route.route(f"/{module_name}/excuteTest", methods=["POST"])
def excuteTest():
    session = database.session
    # 获取配置中指定的 临时文件生成地址
    cases_dir = application.config['CASES_ROOT_WEB_DIR']
    # 该次执行唯一ID
    execute_uuid = uuid.uuid4().__str__()
    # 1.0 创建 该次执行对应的文件夹
    run_tmp_dir = os.path.join(cases_dir, execute_uuid)
    os.makedirs(run_tmp_dir, exist_ok=True)

    try:
        # 获取测试计划ID
        data_id = int(request.json["id"])
        with application.app_context():
            # 1. 测试计划信息
            web_collection_info = module_model.query.filter_by(id=data_id).first()

            # 2. 测试计划 执行对应的浏览器的数据
            browser_info = WebBrowser.query.filter_by(id=web_collection_info.browser_id).first()
            
            # 3. 数据库查询, 附带当前项目的数据库信息
            filter_list = []
            filter_list.append(WebDbBase.project_id == web_collection_info.project_id)  # 当前项目
            filter_list.append(WebDbBase.is_enabled == "1")  # 是启动的状态
            db_infos = WebDbBase.query.filter(*filter_list).all()

        # 第一步： 组装 context.yaml 对应的信息
        test_case_config = {"_browser":{}, "_database":{}}
        # 0. 环境变量， 如果存在，则添加到 context 中
        if web_collection_info.collection_env:
            for d in json.loads(web_collection_info.collection_env):
                test_case_config.update({d["key"]: d["value"]})

        # 1. 加载项目数据库配置信息保存到 context.yaml
        for db_info in db_infos:
           test_case_config["_database"].update({db_info.ref_name: eval(db_info.db_info) })

        # todo: 2. 加载浏览器配置信息 (待完善)
        # todo:config-2. 加载浏览器配置信息 (待完善)
        test_case_config.update({"_browser": {
                                              "grid_url": browser_info.remote_url,
                                              "driver_path": browser_info.driver_path,
                                              "capability": {"browserName": browser_info.enName}
                                              }
                                 })

        # todo: 3. 加载页面元素信息到context.yaml
        with application.app_context():
            # 查询页面和元素信息
            filter_list = []
            filter_list.append(WebPage.project_id == web_collection_info.project_id)  # 当前项目
            pageInfos = WebPage.query.filter(*filter_list).all()
            if len(pageInfos) > 0: test_case_config["_page_element"] = {}
            for page in pageInfos:
                filter_list = []
                filter_list.append(WebEleManage.page_id == page.id)  # 当前项目
                eleInfos = WebEleManage.query.filter(*filter_list).all()
                for ele in eleInfos:
                    location_info = WebLocationMethod.query.filter_by(id=ele.location_method_id).first()
                    test_case_config["_page_element"].update({
                        hashlib.md5(str([page.id,ele.id]).encode()).hexdigest() : {
                        "定位方式": location_info.location_method_name,
                        "目标对象": ele.ele_location_exp
                    } })

        # 当该字段有数据则进行对应的转换，否则是一个空字典
        if len(browser_info.browser_debug) >0:
            test_case_config["_browser"]["capability"].update(eval(browser_info.browser_debug))

        # 生成context.yaml文件夹
        test_case_filename = f"context.yaml"
        test_case_yaml_file = os.path.join(run_tmp_dir, test_case_filename)
        generate_yaml(test_case_config, test_case_yaml_file)

        # 第二步： 生成每一步的测试用例信息
        with application.app_context():
            # 数据库查询,用来接收当前 Collection关联的对应的测试用例
            case_infos = WebCollectionDetail.query.order_by(WebCollectionDetail.run_order.asc()).filter_by(collection_info_id=data_id).all()

        # 2.1 遍历每一个用例，生成对应的 yaml文件
        for case_info in case_infos:
            # 测试用例信息
            case_file_name = uuid.uuid4()
            
            test_case_filename = f"{case_info.run_order}_{case_file_name}.yaml"
            test_case_yaml_file = os.path.join(run_tmp_dir, test_case_filename)

            with application.app_context():
                # # 数据库查询 WebInfo
                web_info = WebInfo.query.filter_by(id=case_info.web_info_id).first()
                # 数据库查询,用来接收当前 WebInfo的测试步骤
                web_steps = WebInfoStep.query.order_by(WebInfoStep.run_order.asc()).filter_by(web_info_id=case_info.web_info_id).all()
                # 扩展功能：数据库查询,用来接收当前 WebInfo的前置测试用来
                pre_cases = WebInfoPre.query.order_by(WebInfoPre.run_order.asc()).filter_by(web_info_id=case_info.web_info_id).all()
           
            # 填充测试用例信息 - 基本格式
            test_case_data = {
                "desc": web_info.case_name,
                "steps": [], # 测试步骤
            }

            # 2.1.0 DDT数据驱动信息
            ddt_datas = json.loads(case_info.ddt_param_data)
            if len(ddt_datas) > 0 : test_case_data["ddts"] = [] # 如果有数据则填充
            for ddt_data in ddt_datas:
                d = {}
                for data in ddt_data:
                    d.update({data["key"]: data["value"]})
                test_case_data["ddts"].append(d)

            # 2.1.1 前后置脚本信息
            # 如果存在 前置脚本，则添加 -- BUGFIX：之前按照换行符做的分割，会导致脚本运行失败
            if web_info.pre_request:
                test_case_data["pre_script"] = []
                test_case_data["pre_script"].insert(0,web_info.pre_request)
            # 如果存在 后置脚本，则添加
            if web_info.post_request:
                test_case_data["post_script"] = []
                test_case_data["post_script"].insert(0,web_info.post_request)

            # 2.1.2 测试步骤
            all_case_steps = []

            # 扩展功能：把对应的前置用例拼接到all_case_steps中去起来
            for pre_info_data in pre_cases:
                print("当前的前置用例：", pre_info_data)
                #   1. 获取对应的前置用例的id ，找到对应的步骤去进行拼接。
                with application.app_context():
                    # 数据库查询,用来接收当前 WebInfo的测试步骤,并且通过run_order排序
                    pre_info_steps = WebInfoStep.query.order_by(WebInfoStep.run_order.asc()).filter_by(
                        web_info_id=pre_info_data.pre_info_id).all()
                    # 把当前的步骤加到所有的步骤当中去
                    all_case_steps.extend(pre_info_steps)

            #    把当前的用例的步骤也拼接进去
            all_case_steps.extend(web_steps)

            # 遍历测试步骤，生成 执行器需要的格式数据
            for web_step in all_case_steps:
                with application.app_context():
                    # 获取对应的数据进行拼接
                    keyWordData = WebKeyWord.query.filter_by(id=web_step.key_word_id).first()
                    stepData = {web_step.step_desc: {
                        "关键字": keyWordData.keyword_fun_name
                    }}
                    # 加载每个步骤中的参数配置，更新到步骤信息中
                    stepData[web_step.step_desc].update(json.loads(web_step.ref_variable))

                    test_case_data["steps"].append(stepData)

            generate_yaml(test_case_data, test_case_yaml_file)

        # 文件生成后生成完毕后，
        report_root_dir = application.config['REPORT_ROOT_DIR'] # 测试报告目录
        key_words_dir = application.config['KEY_WORDS_DIR'] # 关键字目录
 
        os.makedirs(report_root_dir, exist_ok=True)
        report_data_path = os.path.join(report_root_dir, f"{execute_uuid}-data")  # 测试数据保存目录
        report_html_path = os.path.join(report_root_dir, execute_uuid)  # 测试html报告

        # 1. 执行测试
        remote_command = f"webrun --cases={run_tmp_dir} --keyDir={key_words_dir} -sv --capture=tee-sys --alluredir={report_data_path} "
        command_output = subprocess.check_output(remote_command, shell=True, encoding="utf-8")
        history_desc = command_output.split("\n")[-2].replace("=", "") # 截取最后一段
        # TODO 这里可以根据 command_output 命令输出的内容去做一些统计
        # 2. 生成html测试报告
        os.system(f"allure generate {report_data_path} -c -o {report_html_path}")  # 等于你在命令行里面执行 allure
        print("当前的报告路径",report_html_path+"/index.html")
        # 3. 删除一些临时文件，保留html测试报告即可
        # shutil.rmtree(run_tmp_dir)  # 测试套件临时yaml文件 collection_dir
        # shutil.rmtree(report_data_path)  # 测试工具执行后的测试结果数据
        # --------------------扩展功能-把对应的记录存放到历史记录表当中------------------------
        # 保存测试报告
        with application.app_context():
                report = WebHistoryModel(id=0, 
                                         collection_info_id=web_collection_info.id, 
                                         history_desc=history_desc,
                                         history_detail=execute_uuid,
                                         create_time=datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S'))
                database.session.add(report)
                database.session.commit()

        return respModel.ok_resp_text(msg="执行完毕，请查看测试报告", data={
            "report_id": execute_uuid
        })

    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"执行出现错误：{e}")



import yaml
def generate_yaml(json_data, url_path):
    if url_path is None:
        raise ValueError("The 'filname' parameter is required.")

    url_path = url_path

    # 检查json_data是否是字典或JSON字符串
    if isinstance(json_data, dict):
        # 已经是字典，直接转换
        with open(url_path, 'w', encoding='utf-8') as file:
            yaml.dump(json_data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
    elif isinstance(json_data, str):
        try:
            # 尝试将JSON字符串加载为字典
            json_data = json.loads(json_data)
            with open(url_path, 'w', encoding='utf-8') as file:
                yaml.dump(json_data, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except json.JSONDecodeError:
            raise ValueError("The provided string is not a valid JSON.")
    else:
        raise ValueError("The 'json_data' parameter must be a dictionary or a JSON string.")


# 扩展接口：复制测试集合计划
from webtest.model.WebCollectionDetailModel import WebCollectionDetail

@module_route.route(f"/{module_name}/copyData", methods=["POST"])
def copyData():
    """ 复制的接口 """
    try:
        with application.app_context():
            # todo: 1. 获取当前测试集以及对应关联用例
            data_id = request.json["id"]
            # 数据库查询,接收前端传递过来的 Collection
            collection_info = module_model.query.filter_by(id=data_id).first()
            # 数据库查询,用来接收当前 Collection关联的对应的测试用例
            web_collection_detail = WebCollectionDetail.query.order_by(WebCollectionDetail.run_order.asc()).filter_by(collection_info_id=data_id).all()

            # todo：2. 拼接测试集和用例的数据
            coll_data = {"id": None,
                         "project_id": collection_info.project_id,
                         "collection_name": collection_info.collection_name + " copy",
                         "collection_desc":collection_info.collection_desc,
                         "collection_env":collection_info.collection_env,
                         "browser_id": collection_info.browser_id,
                         "create_time": datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')
                         }
            data = module_model(**coll_data)
            # 获取新增后的ID并返回
            database.session.add(data)
            # 获取新增后的ID并返回
            database.session.flush()
            data_id = data.id
            database.session.commit()

            # todo：3. 拼接用例的数据
            for case in web_collection_detail:
                case_data = {"id":None,
                             "collection_info_id": data_id,# 之前获取的测试集合的id
                             "web_info_id": case.web_info_id,
                             "ddt_param_data": case.ddt_param_data,
                             "run_order": case.run_order,
                             "create_time": datetime.strftime(datetime.today(), '%Y-%m-%d %H:%M:%S')
                            }
                data = WebCollectionDetail(**case_data)
                # 获取新增后的ID并返回
                database.session.add(data)
                # 获取新增后的ID并返回
                database.session.flush()
                database.session.commit()
            return respModel.ok_resp(msg="复制成功", dic_t={"id": data_id})

    except Exception as e:
        print(e)
        return respModel.error_resp(msg=f"添加失败:{e}")