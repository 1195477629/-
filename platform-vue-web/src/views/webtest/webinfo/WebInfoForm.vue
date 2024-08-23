<template>
  <el-form ref="ruleFormRef" :inline="true" :model="webInfo" :rules="rules" class="demo-form-inline">
    <div class="form-wrapper">
      <div class="form-info">| 基础信息</div>
      <el-form-item class="form-buttons">
        <el-button type="primary" @click="onSubmit()">保存</el-button>
        <el-button type="warning" @click="onExecuteTest()">调试执行测试</el-button>
        <el-button type="info" @click="onCancel">关闭</el-button>
      </el-form-item>
    </div>
    <el-form-item label="用例编号：">
      <el-input v-model="webInfo.id" placeholder="用例编号" clearable disabled />
    </el-form-item>
    <el-form-item label="用例名称：">
      <el-input v-model="webInfo.case_name" placeholder="输入用例名称" clearable />
    </el-form-item>
    <!-- <el-form-item label="所属项目ID：" prop="project_id">
      <el-select v-model="webInfo.project_id" placeholder="选择所属项目" filterable clearable>
        <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
      </el-select>
    </el-form-item> -->
     <!-- 添加点击事件 -->
      <el-form-item label="所属项目ID：" prop="project_id">
      <el-select v-model="webInfo.project_id" placeholder="选择所属项目" @change="projectChange" filterable clearable>
        <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
      </el-select>
      </el-form-item>

    <el-form-item label="前置用例：" prop="is_pre">
      <el-select v-model="webInfo.is_pre" placeholder="是否前置用例" clearable>
        <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
      </el-select>
    </el-form-item>
    <el-form-item label="用例描述：">
      <el-input v-model="webInfo.case_desc" style="width: 600px" :rows="3" type="textarea" placeholder="请输入用例描述" />
    </el-form-item>

    <div class="form-wrapper">
      <div class="form-info">| 用例信息</div>
    </div>
   <!-- 用例信息模块 -->
    <el-form-item style="width: 1150px;">
      <el-tabs class="demo-tabs" v-model="tabActiveName" style="width: 100%">
       <!-- 功能1：测试用例步骤 -->
       <el-tab-pane label="当前用例步骤" name="当前用例步骤">

        <!-- 功能1-1 显示已经添加的所有步骤-->
        <el-table :data="tableDataCaseStep" row-key="id" class="table_data" max-height="500">
            <el-table-column fixed="left" label="操作" width="80">
              <template #default="scope">
                <el-button link type="primary" size="small"
                  @click="updateWebInfoStep(scope.row)">
                  确认修改
                </el-button>
                <br />
                <el-button link type="primary" size="small" @click="onDelete(scope.row.id)">
                  删除
                </el-button>
              </template>
            </el-table-column>

            <el-table-column prop="run_order" label="执行顺序" width="125">
              <template #default="scope">
                <!-- <el-input style="width: 50px" v-model="scope.row.run_order" placeholder="顺序-数字类型"></el-input> -->
                <el-input-number v-model="scope.row.run_order" :min="1" style="width: 110px" placeholder="顺序"/>
              </template>
            </el-table-column>
            <el-table-column prop="step_desc" label="步骤描述" width="480">
              <template #default="scope">
                <el-input style="max-width: 600px; width: 360px" v-model="scope.row.step_desc"
                  placeholder="输入步骤描述"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="vaule" label="关键字操作" width="320">
              <template #default="scope">
                <el-cascader v-model="scope.row.value" :options="keyWordAllList" @change="onStepKeyModifyChange(scope.$index)" />
              </template>
            </el-table-column>

            <el-table-column prop="ref_variable" label="关键字参数" type="expand" width="120" style="background-color: antiquewhite;">
              <template #default="scope">
                <!-- 循环遍历出所有的参数数据 -->
                <span style="margin-left: 10px;" v-for="variable in findKeyWordByName(scope.row.value[1]).keyword_desc">
                  <span style="margin-right: 10px;">{{ variable.name }}</span >
                  <!-- 如果是数据库 -->
                  <el-select v-if="variable.name.endsWith('_数据库')"
                    v-model="scope.row.ref_variable[variable.name]"
                    filterable placeholder="选择数据库对象" style="width: 180px" clearable >
                    <el-option v-for="database in databaseList" :key="database.id"
                      :label="database.name" :value="database.ref_name" >
                    </el-option>
                  </el-select>
                  <!-- END 如果是数据库 -->
                  <!-- 如果是页面元素对象 -->
                 <el-cascader v-else-if="variable.name.endsWith('_页面元素')" 
                 v-model="scope.row.ref_variable[variable.name]" 
                 :options="pageElementCascader"  />
                <!-- END 如果是页面元素对象 -->
                  <!-- 普通参数就是一个输入框 -->
                  <el-input v-else style="width: 240px; margin: left 20px ;" v-model="scope.row.ref_variable[variable.name]"
                    :placeholder="variable.placeholder"/>
                  <!-- END 普通参数就是一个输入框 -->
                </span>
              </template>
            </el-table-column>
        </el-table>

        <!-- 功能1-2 添加对应的测试用例步骤-->
        <div class="input-group">
            <!-- <el-input v-model="tmp_webCaseStep.run_order" placeholder="顺序-数字类型"/> -->
            <el-input-number v-model="tmp_webCaseStep.run_order" :min="1" placeholder="顺序" style="margin-left: 20px;width: 110px;"/>
            <el-input v-model="tmp_webCaseStep.step_desc" placeholder="输入步骤描述"/>
             <!-- 1. 以级联的方式去进行数据的显示 -->
            <el-cascader :options="keyWordAllList" @change="onStepAddKeyHandleChange"/> 
            <!-- 1-1 根据关键字参数生成对应的输入框 -->
            <span v-if="tmp_webCaseStep.keyword != undefined" v-for="variable in findKeyWordById(tmp_webCaseStep.keyword.id).keyword_desc">
            <!-- 扩展 如果是数据库，则加载一个下拉列表  -->
            <el-select v-if="variable.name.endsWith('_数据库')"
                v-model="tmp_webCaseStep.ref_variable[variable.name]"
                filterable
                placeholder="选择数据库对象"
                style="width: 180px"
                clearable
              >
               <!-- ref_name 即是写入到数据库当中的数据  -->
                <el-option
                  v-for="database in databaseList"
                  :key="database.id"
                  :label="database.name"
                  :value="database.ref_name" 
                >
                </el-option>
            </el-select>
             <!-- 扩展 如果是_页面元素 -->
            <el-cascader v-else-if="variable.name.endsWith('_页面元素')" 
            v-model="tmp_webCaseStep.ref_variable[variable.name]" 
            :options="pageElementCascader"  />
              <!-- 1-2 普通参数就是一个输入框 -->
            <el-input v-else  v-model="tmp_webCaseStep.ref_variable[variable.name]" :placeholder="variable.placeholder" />
            </span>
             <!-- END  1-1 根据关键字参数生成对应的输入框 -->
            <el-button style="width: 10%" @click="addWebInfoStep">添加</el-button>
        </div>
        
       </el-tab-pane>
       <!-- 功能2：变量定义 -->
       <el-tab-pane label="变量定义" name="变量定义">
          <!-- 2-1 变量描述的数据显示部分 -->
          <el-table  :data="webInfo.param_data"   class="table_data"   max-height="250" >
          <el-table-column prop="key" label="变量名" style="width: 40%" />
          <el-table-column prop="value" label="变量值" style="width: 40%" />
          <el-table-column fixed="right" label="删除" style="width: 15%">
            <template #default="scope">
              <el-button link  type="primary"   size="small"  @click.prevent="deleteVars(scope.$index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
          <!-- 2-2 添加变量描述位置 -->
          <div class="input-group">
          <el-input v-model="vars.key" placeholder="变量名" style="width: 30%"  />
          <el-input v-model="vars.value" placeholder="变量值" style="width: 30%"  />
          <el-button style="width: 20%" @click="onAddVars">添加</el-button>
          </div>
       </el-tab-pane>
       <!-- 功能3：前置脚本 -->
       <el-tab-pane label="执行前事件(pre)" name="执行前事件(pre)">
        <el-input v-model="webInfo.pre_request" type="textarea" :rows="15" placeholder="执行前事件" />
       </el-tab-pane>
       <!-- 功能4：前置脚本 -->
       <el-tab-pane label="执行后事件(post)" name="执行后事件(post)">
       <el-input v-model="webInfo.post_request" type="textarea" :rows="15" placeholder="执行后事件" />
       </el-tab-pane>
       <!-- 功能5: 添加前置用例复用 -->
       <el-tab-pane label="前置用例复用" name="前置用例复用">
        <!-- 5-1 用例显示 -->
        <el-table :data="tableDataCasePre" class="table_data">
            <el-table-column prop="run_order" label="顺序" width="180">
              <template #default="scope">
                <el-input style="width: 50px" v-model="scope.row.run_order" placeholder="顺序-数字类型"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="case_name" label="用例名称" style="width: 40%" :show-overflow-tooltip="true" />
            <el-table-column fixed="right" label="操作" style="width: 15%">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="updateWebInfoPre(scope.$index)">
                  保存修改
                </el-button>
                <el-button link type="primary" size="small" @click="DeleteWebInfoPre(scope.$index)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        <!-- END 5-1 用例显示 -->

        
        <!-- 5-2 添加用例位置 -->
          <el-button type="primary" link @click="shoWebInfosDialog" style="margin-top: 20px;"> + 添加用例</el-button>
        <!-- END 5-2 添加用例位置 -->

       </el-tab-pane>
      </el-tabs>
    </el-form-item>
   <!--END 用例信息模块 -->
  </el-form>

    <!-- 弹窗 - 弹窗加载执行配置 -->
    <el-dialog v-model="webExecuteTestFormVisible" title="执行配置">
    <el-form-item label="浏览器集群选择：" prop="id">
      <el-select v-model="browserIndex" placeholder="选择需集群浏览器" clearable filterable>
        <el-option v-for="browser in browserList" :key="browser.id" :label="browser.name" :value="browser.id" />
      </el-select>
    </el-form-item>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="webExecuteTestFormVisible = false">取消</el-button>
        <el-button type="primary" @click="okExecuteTest">开始执行</el-button>
      </span>
    </template>
  </el-dialog>

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
          <el-button type="primary" size="small" @click.prevent="addWebPreInfo(scope.$index)">
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

</template>

<script lang="ts" setup>
import { reactive, ref } from "vue";
import { queryById, insertData, updateData } from "./WebInfo.js"; // 不同页面不同的接口
import type { FormInstance, FormRules } from "element-plus";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus"; // 弹窗
import type { Action } from "element-plus";

// 获取当前路由的实例
const router = useRouter(); 

// 初始化搜索 - 用例搜索
const searchForm = reactive({});

// 表单实例
const ruleFormRef = ref<FormInstance>(); 

// 设置后续的默认的选择的Tab
const tabActiveName = ref("当前用例步骤");

// 变量 - 用例的所有数据
const webInfo = reactive({
  id: 0,
  project_id: 0,
  case_name: "",
  case_desc: "",
  param_data: [] as any[],
  pre_request: "", // 执行前事件
  post_request: "", // 执行后事件
  is_pre: "0", // 默认选择否
});

// 变量- 是否下拉列表
const options = [
  {
    value: "1",
    label: "是",
  },
  {
    value: "0",
    label: "否",
  },
];

// 表单验证规则 - 不同的页面，不同的校验规则
const rules = reactive<any>({
  project_id: [{ required: true, message: "必填项", trigger: "blur" }],
  case_name: [{ required: true, message: "必填项", trigger: "blur" }],
  is_pre: [{ required: true, message: "必填项", trigger: "blur" }],
});

// 加载对应的所有项目的数据
import { queryAllProject as queryAllProject } from "../project/WebProject.js"; // 不同页面不同的接口
const projectList = ref([
  {
    id: 0,
    project_name: "",
    project_desc: "",
  },
]);
function getProjectList() {
  queryAllProject().then((res) => {
    projectList.value = res.data.data;
  });
}
getProjectList();

// ----------------------功能部分-------------------------------
// 功能：保存的数据
const onSubmit = () => {
  // 提交之前记得把数组修改为json字符串
  let data = {
    id: webInfo.id,
    project_id: webInfo.project_id,
    case_name: webInfo.case_name,
    case_desc: webInfo.case_desc,
    param_data: JSON.stringify(webInfo.param_data),
    pre_request: webInfo.pre_request, // 执行前事件
    post_request: webInfo.post_request, // 执行后事件
    is_pre: webInfo.is_pre,
  };

  if (webInfo.id > 0) {
    updateData(data).then((res: { data: { code: number; msg: string } }) => {
      if (res.data.code == 200) {
        // router.push("/WebInfoList"); // 跳转回列表页面 - 不同的页面，不同的路径
        // 重新加载当前的页面数据
        loadData(data.id);
      }
    });
  } else {
    insertData(data).then((res: { data: { code: number; msg: string } }) => {
      if (res.data.code == 200) {
        // router.push("/WebInfoList"); // 跳转回列表页面 - 不同的页面，不同的路径
        // 重新加载当前的页面数据
        loadData(res.data.data.id);
      }
    });
  }
};

// 功能：加载对应的数据
// 表格数据
const tableDataCaseStep = ref([]);

const loadData = async (id: number) => {
  const res = await queryById(id);
  // 不同的页面，不同的表单字段 (注意这里的res.data.data.xxx，xxx是接口返回的字段，不同的接口，字段不同)
  // 注意:此处将 后台的json字符串转变为对象
  webInfo.id = res.data.data.id;
  webInfo.project_id = res.data.data.project_id;
  webInfo.case_name = res.data.data.case_name;
  webInfo.case_desc = res.data.data.case_desc;
  webInfo.is_pre = res.data.data.is_pre;
  webInfo.param_data = JSON.parse(res.data.data.param_data);
  webInfo.pre_request = res.data.data.pre_request; // 执行前事件
  webInfo.post_request = res.data.data.post_request; // 执行后事件
 
   // 6.0  加载测试步骤的数据
  let searchData = searchForm;
  searchData["page"] = 1;
  searchData["pageSize"] = 9999;
  searchData["web_info_id"] = webInfo.id;
  const total = ref(0);

  queryAllSetp(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      tableDataCaseStep.value = res.data.data;
      // 把 ref_variable 数据由 json字符串转换为 js 对象
      tableDataCaseStep.value.forEach((step, index) => {
        tableDataCaseStep.value[index]["ref_variable"] = JSON.parse(tableDataCaseStep.value[index]["ref_variable"])
      });
      total.value = res.data.total;
    }
  );


  // 初始化，加载一下当中的数据库数据：
  loadDatabaseInfos()

  // 初始化，加载一下前置用例的数据
  getWebInfoPre()

  // 初始化，触发页面元素信息重新加载
  loadPageElementForProject();
};

let query_id = router.currentRoute.value.query.id;
webInfo.id = query_id ? Number(query_id) : 0;

if (webInfo.id > 0) {
  // 当ID大于0的时候，加载当前用例的信息
  loadData(webInfo.id);
  // 获取其它的信息
  getProjectList();
}

// 功能：关闭按钮方法
const onCancel = () => {
  router.push("/WebInfoList");
};

// ----------------------关键字 变量定义---------------------------
const vars = reactive({
key: "",
value: "",
});

const deleteVars = (index: number) => {
  // splice() 方法可以在任意位置修改数组,并返回被删除的元素 （下标,个数）
webInfo.param_data.splice(index, 1);
};

const onAddVars = () => {
// 保存起来
webInfo.param_data.push({
  key: vars.key,
  value: vars.value,
});
// 置空
vars.key = "";
vars.value = "";
};
// ----------------------END 关键字 变量定义---------------------------


// ----------------------添加测试用例---------------------------
// ----------------------3.0 添加测试用例之关键字数据显示---------------------------
// 示例：显示关键字的数据
const keyWordAllListDome = [
  {
    value: 'webdriver_exec',
    label: '浏览器操作',
        children: [
          {
            value: 'open_browser',
            label: '打开页面',
          },
          {
            value: 'quit_browser',
            label: '关闭浏览器',
          },
          {
            value: 'maximized_browser',
            label: '最大化浏览器',
          }
        ],
      }, {
    value: 'options_exec',
    label: '元素操作',
        children: [
          {
            value: 'input_context',
            label: '输入内容',
          },
          {
            value: 'option_click',
            label: '点击元素',
          }
        ],
      },
    ]

// 因为如上的数据是固定的，所以我们需要添加一个接口返回对应的当前这个数据。 
// 1. 变量- 添加用例步骤数据 - 临时数据存放
const tmp_webCaseStep = reactive({
  id: 0,
  run_order: 0,
  step_desc: "",
  operation_type: undefined,
  keyword: undefined,
  ref_variable: {}, // 保存关键对应的参数值
});

// 2. 字段- 加载操作方法-关键字  
import { queryAll as queryAllApiKey, queryAllKeyWordList as queryAllKeyWordList,} from "../keyword/WebKeyWord.js"; // 不同页面不同的接口
  
const keyWordAllList = ref([]); // 关键字类型+关键字-树形数据

// 后台查询 关键字_类型-树形数据
// function getKeyWordList() {
//   queryAllKeyWordList().then((res) => {
//     keyWordAllList.value = res.data.data;
//     // 把关键字中的 参数描述由json内容转换为 js 对象
//     keyWordAllList.value.forEach((keywordType, index) => {
//     // 遍历每一个 分类下的 children
//       var children = keyWordAllList.value[index]["children"]
//       children.forEach((keyword, i) => {
//         var data = JSON.parse(children[i]["keyword_desc"])
//         children[i]["keyword_desc"] = data
//       });
//     });
//     console.log("关键字类型+关键字-上下级树形数据加载完毕")
//     console.log(keyWordAllList.value)
//   });
// }
// getKeyWordList();
// ----------------------END 3.0 添加测试用例之关键字数据显示---------------------------


// ----------------------4.0 增加测试用例步骤功能之关键字数据动态显示对应的数据---------------------------
const keyWordList = ref([
  {
    id: 0,
    name: "--无--",
    keyword_desc: "[]",
    keyword_fun_name: "",
    operation_type_id: "",
    is_ture: "",
  },
]);

// 后台查询 关键字_类型-树形数据
function getKeyWordList() {
  // 请求接口1： 加载所有的关键字方法的数据 
  queryAllApiKey().then((res) => {
    // keyWordList.value = res.data.data;
    keyWordList.value.push(...res.data.data);
    // 把关键字中的 参数描述由json内容转换为 js 对象
    keyWordList.value.forEach((keyword, index) => {
      keyWordList.value[index]["keyword_desc"] = JSON.parse(keyWordList.value[index]["keyword_desc"])
    });

    console.log("关键字数据加载完毕")
    console.log(keyWordList.value)
  });

  // 请求接口2：加载对应的树状数据 
  queryAllKeyWordList().then((res) => {
    keyWordAllList.value = res.data.data;
    // 把关键字中的 参数描述由json内容转换为 js 对象
    keyWordAllList.value.forEach((keywordType, index) => {
    // 遍历每一个 分类下的 children
      var children = keyWordAllList.value[index]["children"]
      children.forEach((keyword, i) => {
        var data = JSON.parse(children[i]["keyword_desc"])
        children[i]["keyword_desc"] = data
      });
    });
    console.log("关键字类型+关键字-上下级树形数据加载完毕")
    console.log(keyWordAllList.value)
  });
}
getKeyWordList();


// 请求接口3：加载关键字类型
import { queryAll } from "./WebOperationType.js"; // 不同页面不同的接口
const operationTypeList = ref([
  {
    id: 0,
    operation_type_name: "--无--",
    ex_fun_name: "--无--",
    create_time: "",
  },
]);
function getOperationTypeList() {
  queryAll().then((res) => {
    operationTypeList.value = res.data.data;
  });

  console.log("关键字类型-数据加载完毕")
  console.log(operationTypeList.value)
}
getOperationTypeList();


function findKeyWordById(key_word_id) { // 根据关键字ID查找关键字信息
  console.log("根据ID查找关键字信息:" + key_word_id)
  var result = {}
  // 所以我们需要获取所有的关键字数据，可以添加到：getKeyWordList 方法中
  keyWordList.value.forEach((keyword, index) => {
    if (key_word_id == keyword.id) result = keyword
  });
  return result
}

//  当前用例步骤-添加事件
const onStepAddKeyHandleChange = (value) => {
  console.log("当前选择的数据是", value);

  //  选择对应的操作之后动态的修改提示信息
  const foundItemKW = keyWordList.value.find(
    (item) => item.keyword_fun_name === value[1]
  );
  console.log("当前需要查找的foundItemKW：",foundItemKW)
  const foundItemOP = operationTypeList.value.find(
    (item) => item.ex_fun_name === value[0]
  );
  console.log("当前需要查找的foundItemOP：",foundItemOP)

  // 赋值给 webCaseStep 对象
  if (foundItemKW) {
    console.log(foundItemKW.keyword_desc); // 输出找到的 keyword_desc
    tmp_webCaseStep.keyword = foundItemKW;
  } else {
    console.log("没有找到 keyword_fun_name 对应的项");
  }

  if (foundItemOP) {
    tmp_webCaseStep.operation_type = foundItemOP;
  } else {
    console.log("没有找到 keyword_fun_name 对应的项");
  }
};
// ----------------------END 4.0 增加测试用例步骤功能之关键字数据动态显示对应的数据---------------------------


// ---------------------5.0 添加对应的测试步骤---------------------------
import {
  queryByPage as queryByPageForStep,
  insertData as insertDataForStep,
  updateData as updateDataForStep,
  deleteData as deleteDataForStep,
  queryAllSetp as queryAllSetp
} from "./WebInfoStep.js"; // 不同页面不同的接口


function addWebInfoStep(data) {
  if (webInfo.id == 0) { // 如果测试用例没保存，则提示保存
    ElMessageBox.alert("请先保存该测试用例，再添加测试步骤。", "提示", {
      confirmButtonText: "确认保存",
      callback: (action: Action) => {
        // 提交数据
        // onSubmit();
        if (action == "confirm") {
          // 提交之前记得把数组修改为json字符串
          let data = {
            id: webInfo.id,
            project_id: webInfo.project_id,
            case_name: webInfo.case_name,
            case_desc: webInfo.case_desc,
            param_data: JSON.stringify(webInfo.param_data),
            pre_request: webInfo.pre_request, // 执行前事件
            post_request: webInfo.post_request, // 执行后事件
            is_pre: webInfo.is_pre,
          };
          // 提交数据
          insertData(data).then(
            (res: { data: { data: any; code: number; msg: string } }) => {
              if (res.data.code == 200) {
                data.id = res.data.data.id;
                // 添加成功,刷新数据
                loadData(data.id);
              }
            }
          );
        }
      },
    });
  } else { // 如果是新增加测试步骤，则调用新增接口
    var insertStepData = {
      web_info_id: webInfo.id,
      key_word_id: tmp_webCaseStep.keyword.id,
      step_desc: tmp_webCaseStep.step_desc,
      ref_variable: JSON.stringify(tmp_webCaseStep.ref_variable),
      run_order: tmp_webCaseStep.run_order,
    };
    insertDataForStep(insertStepData).then(
      (res: { data: { code: number; msg: string } }) => {
        // 添加成功,刷新列表
        if (res.data.code == 200) {
          loadData(webInfo.id);
        }
        // 添加完毕，清除之前的参数内容
        tmp_webCaseStep.ref_variable = {}
      }
    );
  }
}
// ---------------------END 5.0 添加对应的测试步骤---------------------------


// --------------------6.0 测试步骤数据回显---------------------------
// 6-1 点击关联事件
function findKeyWordByName(key_word_name) { // 根据关键字ID查找关键字信息
  console.log("根据NAME查找关键字信息:" + key_word_name)
  var result = {}
  keyWordList.value.forEach((keyword, index) => {
    if (key_word_name == keyword.keyword_fun_name) result = keyword
  });
  return result
}
// 6-2 点击修改对应的数据key_word_id，方便后期修改数据
const onStepKeyModifyChange = (index) => { 
  const foundItemKW = keyWordList.value.find(
    (item) => item.keyword_fun_name === tableDataCaseStep.value[index].value[1]
  );

  console.log("初始的关键字ID",tableDataCaseStep.value[index].key_word_id)
  // 当点击，则把对应的当前点击的ID 给当前值，方便后期修改数据
  tableDataCaseStep.value[index].key_word_id = foundItemKW.id
  console.log("修改后的关键字ID",tableDataCaseStep.value[index].key_word_id)

  findKeyWordByName(tableDataCaseStep.value[index].value[1]).keyword_desc
};

// ---------------------END 6.0 测试步骤数据回显---------------------------


// --------------------7.0 测试步骤删除、修改数据---------------------------

// 当前用例步骤：删除
const onDelete = (id: number) => {
  deleteDataForStep(id).then((res: {}) => {
    loadData(webInfo.id);
  });
};

// 当前用例步骤：修改
function updateWebInfoStep(data) {
  console.log("当前修改步骤的数据为",data)
  updateDataForStep({
    id: data.id,
    web_info_id: data.web_info_id,
    key_word_id: data.key_word_id,
    step_desc: data.step_desc,
    ref_variable: JSON.stringify(data.ref_variable),
    run_order: data.run_order,
  }).then(
    (res: { data: { code: number; msg: string } }) => {
      // 添加成功,刷新列表
      if (res.data.code == 200) {
        loadData(webInfo.id);
      }
    }
  );
}
// --------------------END 7.0 测试步骤删除、修改数据---------------------------



// --------------------8.0 测试步骤删除、修改数据---------------------------
// 8-1 初始化数据
import { queryByPage, deleteData } from "./WebInfo.js"; // 不同页面不同的接口
const webExecuteTestFormVisible = ref(false); // 是否展示弹窗
const CaseInfoID = ref(-1); // 当前需要执行的用例ID
const browserIndex = ref(0); // 存对应的浏览器ID ，方便后面使用

// 8.2 加载对应的浏览器集群
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

function getbrowserList(index:number) {
  console.log("当前的项目ID 是：",webInfo.project_id)
  let searchData = {
    "page": 1,
    "pageSize": 999,
    "project_id":index // 只显示当前项目的浏览器数据
  }
  queryByPageAllbrowser(searchData).then((res) => {
    browserList.value = res.data.data;
  });
}
getbrowserList(0); // 默认什么直接为0，显示所有的数据

// 8.3 显示当前的弹窗信息，如果没有保存，则进行保存操作
const onExecuteTest = () => {
  // 判断当前的测试用例是否保存。
  if (webInfo.id == 0) {
    ElMessageBox.alert("该操作，将自动【保存】该测试用例。", "提示", {
      confirmButtonText: "我已知晓,继续",
      callback: (action: Action) => {
        // 提交数据
        if (action == "confirm") {
          // 提交之前记得把数组修改为json字符串
          let data = {
            id: webInfo.id,
            project_id: webInfo.project_id,
            case_name: webInfo.case_name,
            case_desc: webInfo.case_desc,
            param_data: JSON.stringify(webInfo.param_data),
            pre_request: webInfo.pre_request, // 执行前事件
            post_request: webInfo.post_request, // 执行后事件
            is_pre: webInfo.is_pre,
          };
          // 提交数据
          insertData(data).then(
            (res: { data: { data: any; code: number; msg: string } }) => {
              if (res.data.code == 200) {
                data.id = res.data.data.id;
                // 重新加载一下数据，并且弹出对应的弹窗
                loadData(data.id);
                //  显示当前的弹窗内容并且设置当前执行的用例数据同时加载浏览器数据。
                webExecuteTestFormVisible.value = true;
                // 设置之前需要执行的测试用例ID
                CaseInfoID.value = webInfo.id;
                console.log("当前的测试用例：", CaseInfoID.value);
                // 加载浏览器数据，只显示当前项目ID的数据
                getbrowserList(webInfo.project_id)
              }
            }
          );
        }
      },
    });
  } else if (webInfo.id > 0) {
    //  显示当前的弹窗内容并且设置当前执行的用例数据同时加载浏览器数据。
    webExecuteTestFormVisible.value = true;
    // 设置之前需要执行的测试用例ID
    CaseInfoID.value = webInfo.id;
    console.log("当前的测试用例：", CaseInfoID.value);
    // 加载浏览器数据，只显示当前项目ID的数据
    getbrowserList(webInfo.project_id)
  }
};

// 8.4 开始执行功能：执行测试-确定按钮
import { excuteTest } from "./WebInfo.js"; // 不同页面不同的接口
const okExecuteTest = () => {
  console.log("当前选择的浏览器：", browserIndex.value);

  //  加载当前测试用例的数据
  let searchData = reactive({});
  searchData["id"] = webInfo.id;
  searchData["browser_id"] = browserIndex.value;
  
  excuteTest(searchData).then((res: {}) => {
    window.open(import.meta.env.VITE_APP_API_URL+"/WebReportViewer/" + res.data.data.report_id + "/index.html", '_blank');
  });
  // 关闭当前的执行窗口
  webExecuteTestFormVisible.value = false;
};

// --------------------END 8.0 测试步骤删除、修改数据---------------------------


// --------------------9.0 加载对应的数据库数据 --------------------

// 9-1 加载对应的数据库数据
const projectChange = (value: number) => {
  // 触发数据库信息加载
  loadDatabaseInfos()
  // 触发页面元素信息重新加载
  loadPageElementForProject();
};

import { queryByPage as queryByPageList } from "../project/DbBaseManage.js"; // 不同页面不同的接口

// TODO 拓展 加载数据库
const databaseList = ref([]);
const loadDatabaseInfos = async () => {
  let searchData = {};
  searchData["project_id"] = webInfo.project_id;
  searchData["page"] = 1;
  searchData["pageSize"] = 99999; // 理论无限大

  queryByPageList(searchData).then(
      (res: { data: { data: never[]; total: number; msg: string } }) => {
        console.log("-------数据库信息查询返回值------", res.data.data);
        databaseList.value = [] // 清空已有的数据库信息
        databaseList.value.push(...res.data.data); // 重新放置新的项目数据库信息
      }
    );
  
}
// --------------------END 9.0 加载对应的数据库数据 --------------------



// ----------------------功能10: 弹窗-测试用例弹窗相关的脚本------------------------------------------
const infoDialogFormVisible = ref(false) // 是否展示弹窗

// -------6-1. 显示弹窗的点击事件-------
const shoWebInfosDialog = () => {
  // 判断当前的测试用例是否保存。
  if (webInfo.id == 0) {
    ElMessageBox.alert("该操作，将自动【保存】该测试用例。", "提示", {
      confirmButtonText: "我已知晓,继续",
      callback: (action: Action) => {
        // 提交数据
        if (action == "confirm") {
          // 提交之前记得把数组修改为json字符串
          let data = {
            id: webInfo.id,
            project_id: webInfo.project_id,
            case_name: webInfo.case_name,
            case_desc: webInfo.case_desc,
            param_data: JSON.stringify(webInfo.param_data),
            pre_request: webInfo.pre_request, // 执行前事件
            post_request: webInfo.post_request, // 执行后事件
            is_pre: webInfo.is_pre,
          };
          // 提交数据
          insertData(data).then(
            (res: { data: { data: any; code: number; msg: string } }) => {
              if (res.data.code == 200) {
                data.id = res.data.data.id;
                // 重新加载一下数据，并且弹出对应的弹窗
                loadData(data.id);
                //  显示当前的弹窗内容并且设置当前执行的用例数据同时加载浏览器数据。
                webExecuteTestFormVisible.value = true;
                // 设置之前需要执行的测试用例ID
                CaseInfoID.value = webInfo.id;
                console.log("当前的测试用例：", CaseInfoID.value);
                // 加载浏览器数据，只显示当前项目ID的数据
                getbrowserList(webInfo.project_id)
              }
            }
          );
        }
      },
    });
  } else if (webInfo.id > 0) {
    //  显示当前的弹窗内容并且设置当前执行的用例数据同时加载浏览器数据。
    infoDialogFormVisible.value = true;
    //  加载数据
    loadWebInfos()
  }
};


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

// -------6-3 显示当前前置用例弹窗的添加用例的数据-------
import { queryByPage as queryWebInfoByPage } from "../webinfo/WebInfo.js"; // 不同页面不同的接口

const webInfoList = ref([] as any[]); // 关联的用例

function loadWebInfos() {
  let searchData = searchForm;
  searchData["page"] = currentWebInfoPage.value;
  searchData["pageSize"] = webInfoPageSize.value;
  searchData["is_pre"] = "1";
   queryWebInfoByPage(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      console.log(res.data.data);
      webInfoList.value = res.data.data;
      webInfoTotal.value = res.data.total;
    }
  );
}
// -------END 6-3 显示当前前置用例弹窗的添加用例的数据-------

// -------6-4 添加前置用例到当前的数据-------
import { insertData as insertDataForPre,} from "./WebInfoPre.js"; // 不同页面不同的接口
function addWebPreInfo(index: number) {
  // console.log("当前点击的CASE",webInfoList.value[index])

  let InsertData = {
    web_info_id: webInfo.id,
    pre_info_id: webInfoList.value[index].id,
    run_order: webInfoList.value[index].data,
  };

  insertDataForPre(InsertData).then(
    (res: { data: { code: number; msg: string } }) => {
      // 添加成功,刷新列表
      if (res.data.code == 200) {
        // 重新加载一下前置用例，并且及时刷新页面
        getWebInfoPre();
        // 同步用例参数到变量列表
        JSON.parse(webInfoList.value[index].param_data).forEach((data, index) => {
          webInfo.param_data.push(data)
        });
      }
    }
  );
}
// -------END 6-4 添加前置用例到当前的数据-------


// -------6-5 前置用例显示、删除、修改到当前的数据-------
import {
  queryByPage as queryByPageForPre,
  updateData as updateDataForPre,
  deleteData as deleteDataForPre,
} from "./WebInfoPre.js"; // 不同页面不同的接口

// 6-5-1. 前置用例：数据显示
const tableDataCasePre = ref([]);
function getWebInfoPre() {
  let searchData = searchForm;
  searchData["page"] = 1;
  searchData["pageSize"] = 9999;
  searchData["web_info_id"] = webInfo.id;
  const total = ref(0);

  queryByPageForPre(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      tableDataCasePre.value = res.data.data;
      total.value = res.data.total;
    }
  );
}

// 6-5-2. 前置用例：删除数据
const DeleteWebInfoPre = (id: number) => {
  ElMessageBox.alert("请根据需要，在变量定义中，手动删除该前置用例的变量信息", "提示", {
    confirmButtonText: "继续",
    callback: (action: Action) => {
      deleteDataForPre(tableDataCasePre.value[id].id).then((res: {}) => {
        getWebInfoPre();// 重新加载用例复用
      });
    }
  })
};
// 6-5-3. 前置用例 信息修改
const updateWebInfoPre = (id: number) => {
  updateDataForPre({
    id: tableDataCasePre.value[id].id,
    run_order: tableDataCasePre.value[id].run_order,
  }).then((res: { data: { code: number; msg: string } }) => {
    if (res.data.code == 200) {
      getWebInfoPre() // 重新加载用例复用
    }
  });
}
// -------END 6-5 前置用例显示、删除、修改到当前的数据-------



// -------7 加载页面-元素的数据加载-------
import { queryByPage as webPageQuery } from "../pagemanage/WebPage.js"; // 不同页面不同的接口
import { queryByPage as webEleQuery } from "../pageelemanage/WebPageEleManage.js"; // 不同页面不同的接口
const pageElementList = ref([]); // 页面元素信息
const webPageList = ref([]); // 项目页面信息
const pageElementCascader = ref([]); // 项目页面+元素级联树形信息
const loadPageElementForProject = async () => {
  if (webInfo.project_id == undefined || webInfo.project_id == "" ) {
    console.log("没有选择任何项目")
    return // 如果没有项目信息，不加载任何内容
  }
  // 1. 后端接口查询 页面信息
  var webPageResult = await webPageQuery({
    project_id: webInfo.project_id,
    page: 1,
    pageSize: 999999,
  });
  webPageList.value = [];
  //  有可能存在无元素的情况，所以这个位置，我们使用扩展运算符（...）将新列表的元素添加到 webPageList 中
  webPageList.value.push(...webPageResult.data.data);
  console.log("页面数据加载完毕")

  // 2. 后端查询 元素信息
  var pageElementResult = await webEleQuery({
    project_id: webInfo.project_id,
    page: 1,
    pageSize: 999999,
  })
  pageElementList.value = [];
  //  有可能存在无元素的情况，所以这个位置，我们使用扩展运算符（...）将新列表的元素添加到 pageElementList 中
  pageElementList.value.push(...pageElementResult.data.data);
  console.log("元素数据加载完毕")
  
  // 3. 组装树形数据用于级联展示
  pageElementCascader.value = [] // 清空
  webPageList.value.forEach((page, index) => { // 遍历页面
    console.log("页面信息......")
    console.log(page)

    var childrens = []
    pageElementList.value.forEach((ele) => {// 遍历元素，属于这个页面的（组成一个树形数据的子节点）
      if(ele.page_id === page.id) {
          childrens.push({
            id: ele.id, 
            value: ele.id, 
            label: ele.name
          })
      }
    })
    var page = {  // 组装一个 树形数据，每个页面都包含了下属的 元素
      id: page.id, 
      value: page.id, 
      label: page.page_name,
      children: childrens
    }
    pageElementCascader.value.push(page) // 插入
  });
  console.log("-------页面元素信息加载完毕-------")
  console.log(webPageList)
  console.log(pageElementList)
  console.log(pageElementCascader)

}
// -------END 7 加载页面-元素的数据加载-------
</script>

<style>
/* 控制保存和取消按钮右对齐 */
.form-wrapper {
  margin-bottom: 20px;
  /* 根据需要调整间隔大小 */
  border-bottom: 1px solid #ccc;
  /* 添加横线，颜色和粗细可以根据需要调整 */
  display: flex;
  align-items: center;
  /* 垂直居中 */
  justify-content: space-between;
  /* 水平分布，使得两端元素靠边 */
}

.demo-form-inline .el-select {
  --el-select-width: 145px;
  margin-right: 10px;
  /* 设置右边距 */
  margin-left: 5px;
  /* 设置右边距 */
}

/* 控制添加的间隙 */
.input-group {
  margin-top: 15px;
  /* 根据需要调整间隔大小 */
}

/* ---------------------调整当前用例步骤的样式--------------------- */
.input-group .el-input-number{
  width: 150px;
  /* 根据需要调整间隔大小 */
  margin-left: 10px;
}

.input-group .el-input {
  width: 180px;
  /* 根据需要调整间隔大小 */
  margin-left: 10px;
}

.input-group .el-button {
  width: 180px;
  /* 根据需要调整间隔大小 */
  margin-left: 10px;
}


.el-table__expanded-cell {
  background-color: beige;
}
</style>