<template>
  <!-- 模块1 ： 头部的按钮和标题 -->
  <div class="form-wrapper">
    <div class="form-info">| WEB测试计划</div>
    <el-form-item class="form-buttons">
      <el-button type="primary" @click="submitForm(ruleFormRef)">
        保存
      </el-button>
      <el-button @click="closeForm()">关闭</el-button>
    </el-form-item>
  </div>

  <!-- 模块2：主题内容信息 -->
  <el-form ref="ruleFormRef" :model="webcollection" :rules="rules" :inline="true" class="demo-form-inline">
  <!-- 模块2-1 -- 基础信息维护 -->
  <el-form-item label="测试计划名称：" prop="collection_name">
      <el-input v-model="webcollection.collection_name"  style="width: 480px"/>
    </el-form-item>
    <el-form-item label="所属项目：" prop="id">
      <el-select v-model="webcollection.project_id" placeholder="选择所属项目" clearable filterable>
        <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
      </el-select>
    </el-form-item>
    <el-form-item label="测试计划描述：" prop="collection_desc" >
      <el-input v-model="webcollection.collection_desc"  style="width: 480px"/>
    </el-form-item>
  <!-- END 模块2-1 -- 基础信息维护 -->

  <!--模块2-2 -- 用例信息\运行配置信息\其它等等维护 -->
  <el-form-item label="">
      <el-tabs class="demo-tabs" v-model="tabActiveName" style="width: 1120px">
        <el-tab-pane label="用例维护" name="用例维护">
          <!-- TAB1 -- 用例维护的位置 -->
          <!-- 用例显示的位置 -->
          <el-table :data="tableDataCaseInfo"  row-key="id" style="width: 100%">
              <el-table-column fixed="left" label="操作" width="180">
                <template #default="scope">
                  <el-button link type="primary" size="small" @click.prevent="editCaseParamData(scope.$index)">
                    确认修改
                  </el-button>
                  <el-button link type="primary" size="small" @click.prevent="deleteApiCases(scope.$index)">
                    删除
                  </el-button>
                </template>
              </el-table-column>
              <el-table-column prop="run_order" label="顺序" >
                <template #default="scope">
                  <el-input-number v-model="scope.row.run_order" :min="1" style="width: 120px" placeholder="顺序"/>
                  <!-- <el-input style="width: 50px" v-model="scope.row.run_order" placeholder="顺序-数字类型"></el-input> -->
                </template>
              </el-table-column>
              <el-table-column prop="case_name" label="用例名称" :show-overflow-tooltip="true" />
              <el-table-column prop="param_data" label="变量依赖说明" :show-overflow-tooltip="true" />
              <el-table-column prop="ddt_param_data" label="DDT数据驱动" type="expand" width="120">
              <!--可以到时候为一个用例设置多组不同的数据 -->
              <template #default="case_scope">
                  <!-- 位置1 : 输入描述名称,添加数据 -->
                  <el-input v-model="temp_desc" placeholder="desc参数-测试数据组标题" style="width: 40%;margin-left: 10px;" />
                  <el-button style="width: 15%;margin-left: 10px;" @click="onAddDdtParamsGroup(case_scope.$index)">添加一组数据</el-button>
                   <!-- END 位置1 : 输入描述名称,添加数据 -->

                   <!-- 位置2 : 添加对应的数据显示位置 -->
                  <el-collapse style="margin-top: 10px;">
                    <el-collapse-item 
                      v-for="(ddt_data, ddt_data_index) in case_scope.row.ddt_param_data" 
                      :key="ddt_data_index" 
                      :name="ddt_data_index"
                    >
                    <!-- 显示对应的标题 -->
                      <template #title>
                        <div style="vertical-align: middle;" class="chapters_style_1">
                          <el-button  style="margin-left: 10px; " @click="onDeleteDdtParamsGroup(case_scope.$index, ddt_data_index)">删除</el-button>
                          <span style="margin-left: 10px; "> 第 {{ddt_data_index + 1}} 组 : {{ ddt_data[0].value }}</span>
                        </div>
                      </template>
                     <!-- END 显示对应的标题 -->
                     
                      <!-- 显示变量的位置 -->
                      <el-table :data="ddt_data" class="table_data" max-height="250">
                        <el-table-column prop="key" label="变量名" style="width: 40%" >
                          <template #default="ddt_data_scope">
                            <el-input v-model="ddt_data_scope.row.key" placeholder="变量名称"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column prop="value" label="变量值" style="width: 40%" >
                          <template #default="ddt_data_scope">
                            <el-input v-model="ddt_data_scope.row.value" placeholder="变量值"></el-input>
                          </template>
                        </el-table-column>
                        <el-table-column fixed="right" label="删除" style="width: 15%">
                          <template #default="ddt_data_scope">
                            <el-button link type="primary" size="small" @click.prevent="deleteDdtParams(case_scope.$index,ddt_data_index, ddt_data_scope.$index)">
                              删除
                            </el-button>
                          </template>
                        </el-table-column>
                      </el-table> 
                      <!-- END 显示变量的位置 -->

                      <!-- 添加变量的位置 -->
                      <div class="input-group">
                        <el-input v-model="temp_ddt_params.key" placeholder="变量名" style="width: 40%" />
                        <el-input v-model="temp_ddt_params.value" placeholder="变量值" style="width: 40%" />
                        <el-button style="width: 15%" @click="onAddDdtParams(case_scope.$index,ddt_data_index)">添加</el-button>
                      </div>
                      <!-- END 添加变量的位置 -->
                    </el-collapse-item>
                  </el-collapse>
                   <!-- END 位置2 : 添加对应的数据显示位置 -->

              </template>
              <!--END 可以到时候为一个用例设置多组不同的数据 -->
              </el-table-column>
          </el-table>
          <!-- END 用例显示的位置 -->

          <!-- 添加用例位置 -->
          <el-button type="primary" link @click="shoWebInfosDialog" style="margin-top: 20px;"> + 添加用例</el-button>
          <!-- END 添加用例位置 -->

        </el-tab-pane>

        <el-tab-pane label="运行环境配置" name="运行环境配置">
          <!-- TAB2 -- 运行环境配置 -->
          <!-- 浏览器运行选择 -->
          <el-divider content-position="center">运行环境</el-divider>
          <span>浏览器运行选择：</span>
          <el-select v-model="webcollection.browser_id" placeholder="选择浏览器" clearable filterable>
            <el-option v-for="browser in browserList" :key="browser.id" :label="browser.name" :value="browser.id" />
          </el-select>
          <!-- END浏览器运行选择 -->

          <!-- 全局变量的显示 -->
          <el-divider content-position="center">全局环境变量</el-divider>
          <el-table :data="webcollection.collection_env" class="table_data" max-height="250">
            <el-table-column prop="key" label="变量名" style="width: 40%" />
            <el-table-column prop="value" label="变量值" style="width: 40%" />
            <el-table-column fixed="right" label="删除" style="width: 15%">
              <template #default="scope">
                <el-button link type="primary" size="small" @click.prevent="deleteVars(scope.$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          <!-- END全局变量的显示 -->
          <!-- 全局变量的添加 -->
          <div class="input-group">
            <el-input v-model="vars.key" placeholder="变量名" style="width: 40%" />
            <el-input v-model="vars.value" placeholder="变量值" style="width: 40%" />
            <el-button style="width: 15%" @click="onAddVars">添加</el-button>
          </div>
           <!-- END 全局变量的添加 -->
        </el-tab-pane>

         <!-- Jenkins配置的添加  -->
        <el-tab-pane label="Jenkins环境配置" name="Jenkins环境配置">
          <el-divider content-position="center">配置说明</el-divider>
          <el-text class="mx-1" type="danger" style="margin-bottom: 20px;">如果您需要进行CICD，在Jenkins配置请求当前的接口即可。配置的信息内容如下：</el-text>
          <p> <el-tag type="primary" style="margin-left: 20px;width: 100px;">PATH：</el-tag> <el-tag type="info" style="margin-left: 20px;">/WebCollectionInfo/excuteTest</el-tag></p>
          <p> <el-tag type="primary" style="margin-left: 20px;width: 100px;">请求头：</el-tag><el-tag type="info" style="margin-left: 20px;">Content-Type: application/json</el-tag></p>
          <p> <el-tag type="primary" style="margin-left: 20px;width: 100px;">请求方法：</el-tag><el-tag type="info" style="margin-left: 20px;">POST</el-tag></p>
          <p> <el-tag type="primary" style="margin-left: 20px;width: 100px;">请求参数：</el-tag><el-tag type="info" style="margin-left: 20px;" v-model="JenkinsInfo"> {"id":{{JenkinsInfo}}}</el-tag></p>
        </el-tab-pane>
         <!-- END Jenkins配置的添加  -->
      </el-tabs>
    </el-form-item>
   <!--END 模块2-2 -- 用例信息\运行配置信息\其它等等维护 -->
  

  </el-form>
  

  <!-- 弹窗 - 弹窗加载用例列表 -->
  <el-dialog v-model="infoDialogFormVisible" title="添加用例">
    <!-- 弹窗的搜索条件 -->
    <el-form-item label="项目名称：" style="margin-left: 10px; margin-right: 10px">
      <el-select v-model="searchForm.project_id" placeholder="根据项目名称筛选" clearable filterable style="width: 200px">
        <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
      </el-select>
      <el-form-item label="WEB用例名称：" style="margin-left: 10px; margin-right: 10px">
        <el-input v-model="searchForm.case_name" placeholder="根据Web用例名称筛选" clearable />
      </el-form-item>
      <el-button type="primary" @click="loadWebInfos()">查询</el-button>
    </el-form-item>
    <!-- END 弹窗的搜索条件 -->

    <!-- 显示对应的所有数据 -->
    <el-table :data="webInfoList" style="width: 100%">
      <el-table-column prop="id" label="用例编号" style="width: 5%" />
      <el-table-column prop="case_name" label="用例名称" style="width: 30%" :show-overflow-tooltip="true" />
      <el-table-column prop="case_desc" label="用例描述" style="width: 60%" :show-overflow-tooltip="true" />
      <el-table-column fixed="right" label="操作" style="width: 5%">
        <template #default="scope">
          <el-button type="primary" size="small" @click.prevent="addWebInfo(scope.$index)">
            添加
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- END显示对应的所有数据 -->

     <!-- 分页 -->
        <div class="demo-pagination-block">
        <div class="demonstration"></div>
        <el-pagination 
        v-model:current-page= "currentWebInfoPage" 
        v-model:page-size= "webInfoPageSize" 
        :page-sizes="[5, 10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper" 
        :total="webInfoTotal" @size-change="handleSizeChange"
        @current-change="handleCurrentChange" />
    </div>
    <!-- END 分页 -->
  </el-dialog>
  <!-- END 弹窗 - 弹窗加载用例列表 -->

<el-form>
</el-form>
</template>

<script lang="ts" setup>
import { ref, reactive } from "vue";
import { queryById, insertData, updateData } from "./WebCollectionInfo.js"; // 不同页面不同的接口
import type { FormInstance, FormRules } from "element-plus";
import { useRouter } from "vue-router";
const router = useRouter();

// 表单实例
const ruleFormRef = ref<FormInstance>();

// 表单数据 - 不同的页面，不同的表单字段
const webcollection = reactive({
  id: 0,
  project_id: 0,
  browser_id: 0,
  collection_name: "",
  collection_desc: "",
  collection_env: [] as any[],
  collection_params: [] as any[]
});

// 表单验证规则 - 不同的页面，不同的校验规则
const rules = reactive<any>({
  project_id: [{ required: true, message: "必填项", trigger: "blur" }],
  collection_name: [{ required: true, message: "必填项", trigger: "blur" }],
  collection_desc: [{ required: true, message: "必填项", trigger: "blur" }],
});


// 提交表单
const submitForm = async (form: FormInstance | undefined) => {
  // 1. 校验表单 2.提交集合基础信息 3.提交用例信息
  if (!form) return;
  await form.validate((valid, fields) => {
    if (!valid) {
      return;
    }
    var collection_data = {
      id: webcollection.id,
      project_id: webcollection.project_id,
      browser_id: webcollection.browser_id,
      collection_name: webcollection.collection_name,
      collection_desc: webcollection.collection_desc,
      collection_env: JSON.stringify(webcollection.collection_env)
    }
    // 有ID 代表是修改， 没ID 代表是新增
    if (webcollection.id > 0) {
      updateData(collection_data).then(
        (res: { data: { code: number; msg: string } }) => {
          if (res.data.code == 200) {
            // router.push("/WebCollectionList"); // 跳转回列表页面 - 不同的页面，不同的路径
          }
        }
      );
    } else {
      insertData(collection_data).then(
        (res: { data: { code: number; msg: string } }) => {
          if (res.data.code == 200) {
            // router.push("/WebCollectionList"); // 跳转回列表页面 - 不同的页面，不同的路径
            loadData(res.data.data.id);
          }
        }
      );
    }
  });
};

// 关闭表单 - 回到数据列表页 - 不同的页面，不同的路径
const closeForm = () => {
  router.push("/WebCollectionInfoList");
};

const JenkinsInfo=  ref("")
// 加载表单数据
const loadData = async (id: number) => {
  const res = await queryById(id);
  // 不同的页面，不同的表单字段 (注意这里的res.data.data.xxx，xxx是接口返回的字段，不同的接口，字段不同)
  webcollection.id = res.data.data.id;
  webcollection.project_id = res.data.data.project_id;
  webcollection.browser_id = res.data.data.browser_id;
  webcollection.collection_name = res.data.data.collection_name;
  webcollection.collection_desc = res.data.data.collection_desc;
  webcollection.collection_env = JSON.parse(res.data.data.collection_env);

  // 加载测试用例信息数据
  getWebCaseInfo()

  // 初始化CICD的id值：
  JenkinsInfo.value = res.data.data.id;
};


// 如果有id参数，说明是编辑，需要获取数据
console.log(router);
let query_id = router.currentRoute.value.query.id;
webcollection.id = query_id ? Number(query_id) : 0;

if (webcollection.id > 0) {
  loadData(webcollection.id);
}

// 如果有其他逻辑，请添加
// 1. 加载项目
import { queryAllProject } from "../project/WebProject.js"; // 不同页面不同的接口
const projectList = ref([{
  id: 0,
  project_name: '',
  project_desc: ''
}]);
function getProjectList() {
  queryAllProject().then((res) => {
    projectList.value = res.data.data;
  });
}
getProjectList();

// ---------------------功能1: Tab页面默认选择---------------------------
const tabActiveName = ref("用例维护"); // tab页


// ---------------------功能2: 加载对应的浏览器集群---------------------------
import { queryByPage as queryByPageAllbrowser } from "../browserRemote/WebBrowser.js"; // 不同页面不同的接口
const browserList = ref([{
  id: 0,
  name: "",
  enName: "",
  project_id: "",
  remote_url: "",
  browser_debug: "",
  is_enabled: "",
}]);
function getbrowserList() {
  let searchData = {
    "page": 1,
    "pageSize": 999
  }
  queryByPageAllbrowser(searchData).then((res) => {
    browserList.value = res.data.data;
  });
}
getbrowserList();

// ---------------------功能3: 全局变量的显示和添加---------------------------
const vars = reactive({
  key: "",
  value: "",
});

const deleteVars = (index: number) => {
  webcollection.collection_env.splice(index, 1);
};

const onAddVars = () => {
  // 保存起来
  webcollection.collection_env.push({
    key: vars.key,
    value: vars.value,
  });
  // 置空
  vars.key = "";
  vars.value = "";
};
// ---------------------END 功能3: 全局变量的显示和添加---------------------------


// ---------------------功能4: 获取当前用例列表---------------------------
import {
  queryByPage as queryByPageForDetail,
  insertData as insertDataForDetail,
  updateData as updateDataForDetail,
  deleteData as deleteDataForDetail,
} from "./WebCollectionDetail.js"; // 不同页面不同的接口
const searchForm = reactive({ "project_id": '', "case_name": '' })// 搜索
const tableDataCaseInfo = ref([]);

function getWebCaseInfo() {
  let searchData = searchForm;
  searchData["page"] = 1;
  searchData["pageSize"] = 9999;
  searchData["collection_info_id"] = webcollection.id;
  const total = ref(0);

  queryByPageForDetail(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      tableDataCaseInfo.value = res.data.data;
      // json字符串转 js对象
      tableDataCaseInfo.value.forEach((item, index) => {
      tableDataCaseInfo.value[index]["ddt_param_data"] = JSON.parse(tableDataCaseInfo.value[index]["ddt_param_data"])
      });
      total.value = res.data.total;
    }
  );
}
// ---------------------END 功能4: 获取当前用例列表---------------------------

// ---------------------功能5: 删除用例列表---------------------------
// 
const deleteApiCases = (index: number) => {
  deleteDataForDetail(tableDataCaseInfo.value[index]["id"]).then((res: {}) => {
  getWebCaseInfo() // 重新加载列表
  })
};
// ---------------------END 功能5: 删除用例列表---------------------------

// ----------------------功能6: 弹窗-测试用例弹窗相关的脚本------------------------------------------
const infoDialogFormVisible = ref(false) // 是否展示弹窗

// -------6-1. 显示弹窗的点击事件-------
import { ElMessage, ElMessageBox } from 'element-plus' // 弹窗
import type { Action } from 'element-plus'

function shoWebInfosDialog() {
  // 如果是新建集合,提示将自动保存,获取到ID之后再进行用例关联
  if (webcollection.id == 0) {
    ElMessageBox.alert("该操作，将自动【保存】该测试用例", "提示", {
      // if you want to disable its autofocus
      // autofocus: false,
      confirmButtonText: "我已知晓,继续",
      callback: (action: Action) => {
        if (action == "confirm") {
          // 提交之前记得把数组修改为json字符串
          var collection_data = {
            id: webcollection.id,
            project_id: webcollection.project_id,
            browser_id: webcollection.browser_id,
            collection_name: webcollection.collection_name,
            collection_desc: webcollection.collection_desc,
            collection_env: JSON.stringify(webcollection.collection_env)
          }
          // 提交数据
          insertData(collection_data).then(
            (res: { data: { data: any; code: number; msg: string } }) => {
              if (res.data.code == 200) {
                infoDialogFormVisible.value = true;
                // 打开页面的同时加载当前页面的数据
                loadWebInfos()
                loadData(res.data.data.id);
              }
            }
          );
        }
      },
    });
  } else {
    // 打开页面的同时加载当前页面的数据
    infoDialogFormVisible.value = true;
    loadWebInfos()
  }
}

// -------6-2 分页相关的-----
const webInfoPageSize = ref(5); // 每页大小
const webInfoTotal = ref(0);  // 总数
const currentWebInfoPage = ref(1) // 页码


// 变更页大小
const handleSizeChange = (val: number) => {
    console.log("页大小变化:" + val)
    webInfoPageSize.value = val
    loadWebInfos()
}

// 变更页码
const handleCurrentChange = (val: number) => {
    console.log("页码变化:" + val)
    currentWebInfoPage.value = val
    loadWebInfos()
}
// -------END 分页相关的-----

// -------6-3 显示当前的数据-------
import { queryByPage as queryWebInfoByPage } from "../webinfo/WebInfo.js"; // 不同页面不同的接口

const webInfoList = ref([] as any[]); // 关联的用例

function loadWebInfos() {
  let searchData = searchForm;
  searchData["page"] = currentWebInfoPage.value;
  searchData["pageSize"] = webInfoPageSize.value;
   queryWebInfoByPage(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      console.log(res.data.data);
      webInfoList.value = res.data.data;
      webInfoTotal.value = res.data.total;
    }
  );
}
// -------END 6-3 显示当前的数据-------


// -------6-4 添加当前的数据到对应的测试计划当中-------
function addWebInfo(index: number) {
  // console.log("当前点击的CASE",webInfoList.value[index])

  let InsertData = {
    collection_info_id: webcollection.id,
    web_info_id: webInfoList.value[index].id,
    ddt_param_data: JSON.stringify([]),
    run_order: webInfoList.value[index].run_order,
  };

  insertDataForDetail(InsertData).then(
    (res: { data: { code: number; msg: string } }) => {
      // 添加成功,刷新列表
      if (res.data.code == 200) {
        // 重新加载一下前置用例，并且及时刷新页面
        getWebCaseInfo()
        loadData(webcollection.id);
      }
    }
  );
}
// -------END 6-4 添加当前的数据到对应的测试计划当中-------




// --------6-5 用例维护界面-用例的参数维护及修改------------------
// 1. 临时存储 数据变量
const temp_ddt_params = reactive([]); 

// 2. 保存一组数据
const temp_desc = ref("") // 临时存储 数据描述
const onAddDdtParamsGroup = (case_index: number, ) => {
  // 获取用例需要的参数
  let case_param_data = JSON.parse(tableDataCaseInfo.value[case_index].param_data)
  // 插入元素到指定位置-标题
  case_param_data.splice(0, 0, {
    "key": "desc",
    "value": temp_desc.value
  })
  console.log("当前的参数为：",case_param_data)
  // 插入到 测试计划的指定用例中
  tableDataCaseInfo.value[case_index].ddt_param_data.push(reactive(case_param_data))
  // 清空 desc 内容
  temp_desc.value=""
  console.log("当前的所有数据为",tableDataCaseInfo.value)
  // 所以我们就可以通过下标获取对应的数据
  // console.log(tableDataCaseInfo.value[0]["ddt_param_data"])
}

// 3. 删除一组数据
const onDeleteDdtParamsGroup =(case_scope_index, ddt_data_index) => {
  // case_scope_index 哪一条用例 ddt_data_index 第几组 
  tableDataCaseInfo.value[case_scope_index].ddt_param_data.splice(ddt_data_index, 1);
}

// 4.删除某个变量
const deleteDdtParams = (case_scope_index: number, ddt_data_index: number, row: number) => {
  // case_scope_index 哪一条用例 ddt_data_index 第几组  row 第几个变量
  tableDataCaseInfo.value[case_scope_index].ddt_param_data[ddt_data_index].splice(row, 1);
};

// 5.添加某个变量
const onAddDdtParams = (case_scope_index, ddt_data_index) => {
  // case_scope_index 哪一条用例 ddt_data_index 第几组 
  // 保存起来
  tableDataCaseInfo.value[case_scope_index].ddt_param_data[ddt_data_index].push({
    key: temp_ddt_params.key,
    value: temp_ddt_params.value,
  });
  // 置空
  temp_ddt_params.key = "";
  temp_ddt_params.value = "";
};

// 6. 确认修改一组数据 
import { updateData as updateWebCaseCol } from "./WebCollectionDetail.js"; // 不同页面不同的接口

const editCaseParamData = (index: number) => {
  // 修改运行参数与执行顺序
  updateWebCaseCol({
    "id": tableDataCaseInfo.value[index].id,
    "ddt_param_data": JSON.stringify(tableDataCaseInfo.value[index].ddt_param_data),
    "run_order": tableDataCaseInfo.value[index].run_order
  }).then((res: { data: { code: number; msg: string; }; }) => {
    if (res.data.code == 200) {
      console.log("用例执行信息修改成功")
    }
  })
};
// --------END 6-5 用例维护界面-用例的参数维护及修改------------------






</script>

<style>
.el-divider__text{
  background-color: unset;
}

/* ---分页相关的样式--- */

.demo-pagination-block+.demo-pagination-block {
    margin-top: 10px;
}

.demo-pagination-block .demonstration {
    margin-bottom: 16px;
}

.el-collapse-item__header{
  background-color: beige;
}
</style>