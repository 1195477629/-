import copy
import sys, allure

from selenium.webdriver.chrome.service import Service as Chrome_Service
from selenium.webdriver.firefox.service import Service as Firefox_Service
from selenium.webdriver.ie.service import Service as Ie_Service

from selenium.webdriver.common.options import ArgOptions

from webrun.extend.keywords import Keywords
from webrun.extend.script import run_script
from webrun.core.globalContext import g_context
from webrun.utils.VarRender import refresh
from selenium import webdriver


class TestRunner:
    def test_case_execute(self, caseinfo):
        driver = None  # 浏览器对象
        allure.dynamic.title(caseinfo["_case_name"]) # allure 用例标题title，可按需拓展模块等...

        # 定义一个driver_class方便后面结合传过来的过来的key找对应的
        driver_class = {
            "remote": {"driver": webdriver.Remote},
            "chrome": {"driver": webdriver.Chrome, "service": Chrome_Service},
            "firefox": {"driver": webdriver.Firefox, "service": Firefox_Service},
            "ie": {"driver": webdriver.Ie, "service": Ie_Service},
        }

        try:
            # 先确认，然后初始化一个driver 这个你一定得告诉我浏览器类型
            _browser_config = g_context().get_dict("_browser")

            grid_url = _browser_config["grid_url"] # grid 集群地址
            driver_path = _browser_config["driver_path"] # 驱动位置
            capability = _browser_config["capability"] # 浏览器配置项
            browser_name = capability.get('browserName', "") # 浏览器名称
            # 浏览器配置项
            browser_options = ArgOptions()
            for key in capability.keys():
                browser_options.set_capability(key, capability[key])

            if grid_url is not None and len(grid_url) != 0: # 如果配置了grid_url，直接远程集群模式运行
                # 正式投入使用，采用 grid 集群模式
                driver = webdriver.Remote(command_executor=_browser_config["grid_url"], options=browser_options)
            elif driver_path is not None and len(driver_path) != 0: # 如果没配置 grid_url，则加载平台本机指定的驱动
                #  其它的浏览器采用该方法操作，指定驱动方便执行速度快捷
                driver = driver_class[browser_name.lower()]["driver"](
                    service=driver_class[browser_name.lower()]["service"](driver_path),
                    options=browser_options)
            else: # 如果没指定grid_url及驱动位置，则根据浏览器名称自动加载本机环境中的驱动
                driver = driver_class[browser_name.lower()]["driver"](options=browser_options)

            # 单用例范围内的 变量数据
            local_context = caseinfo.get("context", {})
            keywords = Keywords(driver)

            # 执行前置脚本
            context = copy.deepcopy(g_context().show_dict())
            context.update(local_context)
            pre_script = refresh(caseinfo.get("pre_script", None), context) # 全局变量+用例变量渲染
            if pre_script:
                for script in eval(pre_script):
                    run_script.exec_script(script, g_context().show_dict())
            # 准备执行用例 - 刷新用例内变量
            steps = caseinfo.get("steps", None)
            for step in steps:
                step_name = list(step.keys())[0]
                step_value = list(step.values())[0]
                # 刷新步骤内容的变量值
                context = copy.deepcopy(g_context().show_dict())
                context.update(local_context)
                step_value = eval(refresh(step_value, context)) # 全局变量+用例变量渲染
                print(f"开始执行步骤：{step_name} - {step_value}")
                with allure.step(step_name):
                    key = step_value["关键字"]
                    try:
                        key_func = keywords.__getattribute__(key)
                    except AttributeError as e:
                        print("没有这个关键字，动态加载：", e)
                        sys.path.append(g_context().get_dict("key_dir"))
                        module = __import__(key)  # 动态引入模块(temp.py文件)
                        class_ = getattr(module, key)
                        key_func = class_(driver).__getattribute__(key)
                        print("动态加载的函数", key_func)

                    key_func(**step_value)  # 调用关键字方法
                    keywords.截图()
                    # 执行后置脚本
            # 后置脚本执行
            context = copy.deepcopy(g_context().show_dict())
            context.update(local_context)
            post_script = refresh(caseinfo.get("post_script", None), context) # 全局变量+用例变量渲染
            if post_script:
                for script in eval(post_script):
                    run_script.exec_script(script, g_context().show_dict())
        finally:
            if driver is not None:
                driver.quit()
