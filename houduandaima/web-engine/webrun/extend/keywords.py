import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
import allure
from webrun.core.globalContext import g_context


class Keywords:
    driver = None
    def __init__(self,webdriver:WebDriver):
        self.driver = webdriver


    # 浏览器操作- 打开浏览器
    def open_browser(self,**kwargs):
        self.driver.get(kwargs["数据内容"])

    # 浏览器操作- 关闭浏览器
    def quit_browser(self,**kwargs):
        self.driver.quit()

    # 浏览器操作- 关闭当前窗口
    def close_browser(self,**kwargs):
        self.driver.close()

    # 浏览器操作- 最大化当前窗口
    def maximized_browser(self,**kwargs):
        self.driver.maximize_window()

    # 元素操作-输入内容
    def input_context(self,**kwargs):
        self.driver.find_element(kwargs["定位方式"],kwargs["目标对象"]).send_keys(kwargs["数据内容"])

    # 元素操作-点击元素
    def option_click(self,**kwargs):
        self.driver.find_element(kwargs["定位方式"],kwargs["目标对象"]).click()

    # 等待-强制等待
    def wait_sleep(self,**kwargs):
        time.sleep(int(kwargs["数据内容"]))

    # 等待-隐式等待
    def im_sleep(self,**kwargs):
        self.driver.implicitly_wait(int(kwargs["数据内容"]))

    # 等待-显示等待
    def ec_sleep(self,**kwargs):
        wait = WebDriverWait(self.driver, int(kwargs["数据内容"]))
        element = wait.until(EC.presence_of_element_located(kwargs["目标对象"]))

    # 断言处理 - 断言浏览器标题
    def assert_browser_title(self,**kwargs):
        assert EC.title_is(kwargs["数据内容"])(self.driver)

    # 断言处理 - 断言当前Url
    def assert_browser_url(self,**kwargs):
        assert EC.url_to_be(kwargs["数据内容"])(self.driver)

    # 断言处理 - 相等
    def assert_text_eql(self,**kwargs):
        # 预期值
        target = kwargs["数据内容"]
        # 当前值
        current = self.driver.find_element(kwargs["定位方式"], kwargs["目标对象"]).text
        print(f"判断是否相等,{target} - {current}")
        assert current == target

    # 断言处理 - 不相等
    def assert_text_noeql(self, **kwargs):
        assert self.driver.find_element(kwargs["定位方式"],kwargs["目标对象"]).text != kwargs["数据内容"]

    # 断言处理 - 包含
    def assert_text_in(self, **kwargs):
        assert kwargs["数据内容"] in self.driver.find_element(kwargs["定位方式"], kwargs["目标对象"]).text

    # 断言处理 - 大于
    def assert_text_gre(self, **kwargs):
        assert self.driver.find_element(kwargs["定位方式"], kwargs["目标对象"]).text > kwargs["数据内容"]

    # 断言处理 - 小于
    def assert_text_less(self, **kwargs):
        assert self.driver.find_element(kwargs["定位方式"], kwargs["目标对象"]).text < kwargs["数据内容"]

    # 断言处理 - 不包含
    def assert_text_notin(self, **kwargs):
        assert kwargs["数据内容"] not in self.driver.find_elements(kwargs["定位方式"], kwargs["目标对象"])

    def 截图(self):
        allure.attach(self.driver.get_screenshot_as_png(), "截图快照", allure.attachment_type.PNG)  # 截图

    def mysql_sql_exec(self, **kwargs):
        print("执行SQL:", kwargs["SQL"])
        import pymysql
        from pymysql import cursors
        config = {"cursorclass": cursors.DictCursor}
        # 读取全局变量 - 根据选择的数据 读取指定的数据库配置 连接对应的数据库
        db_config = g_context().get_dict("_database")[kwargs["数据库"]]
        config.update(db_config)
        con = pymysql.connect(**config)
        cur = con.cursor()
        cur.execute(kwargs["SQL"])
        rs = cur.fetchall()
        cur.close()
        con.close()
        print("数据库查询结果:", rs)

        var_names = kwargs["引用变量"]
        result = {}
        for i, data in enumerate(rs, start=1):
            for j, value in enumerate(var_names):
                result[f'{var_names[j]}_{i}'] = data.get(var_names[j]) # 根据变量名称找读取出来的内容
        g_context().set_by_dict(result)







