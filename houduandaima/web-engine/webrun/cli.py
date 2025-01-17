import os
import sys
import pytest

from webrun.core.CasesPlugin import CasesPlugin

def run():
    # 获取 python运行参数
    # 1. 读取命令行传入的参数
    pytest_cmd_config = []
    for arg in sys.argv:
        if arg.startswith("-"):
            pytest_cmd_config.append(arg)

    print(os.path.join(os.path.dirname(__file__), "core/WebTestRunner.py"))
    # 2. 构建pytest参数
    pytest_args = [os.path.join(os.path.dirname(__file__), "core/WebTestRunner.py")]
    pytest_args.extend(pytest_cmd_config)

    print("run pytest：", pytest_args)

    pytest.main(pytest_args, plugins=[CasesPlugin()])


if __name__ == '__main__':
    # 测试执行入口
    print(os.path.join(os.path.dirname(__file__),'core', "WebTestRunner.py"))
    pytest_args = ["-s", "-v", "--capture=sys",
                   os.path.join(os.path.dirname(__file__),'core', "WebTestRunner.py"),
                   "--clean-alluredir",
                   "--alluredir=allure-results",
                   "--type=yaml",
                   "--cases=F:\ProjectHcEdu\platform\web-engine\examples"
                   # "--keyDir=F:\\engine\\web-engine\\utils"
                   ]
    print("run pytest：", pytest_args)
    pytest.main(pytest_args, plugins=[CasesPlugin()])

    # 集成 allure 示例
    os.system(r"allure generate -c -o report")  # 等于你在命令行里面执行 allure
