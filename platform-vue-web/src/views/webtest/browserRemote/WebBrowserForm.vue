<template>
  <el-form
    ref="ruleFormRef"
    :model="ruleForm"
    :rules="rules"
    label-width="120px"
    class="demo-ruleForm"
    status-icon
  >
    <el-form-item label="编号" prop="id" >
      <el-input v-model="ruleForm.id" disabled />
    </el-form-item>
    <el-form-item label="浏览器名称" prop="name" >
      <el-input v-model="ruleForm.name"  placeholder="请输入浏览器名称"/>
    </el-form-item>
    <el-form-item label="浏览器类型" prop="enName"  >
      <el-input v-model="ruleForm.enName" placeholder="请输入浏览器类型，比如：chrome、firefox、ie"/>
    </el-form-item>
    <el-form-item label="所属项目ID" prop="project_id">
      <el-select  v-model="ruleForm.project_id" placeholder="选择所属项目" clearable  filterable >
        <el-option
          v-for="project in projectList"
          :key="project.id"
          :label="project.project_name"
          :value="project.id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="远程地址" prop="remote_url" >
      <el-input v-model="ruleForm.remote_url" placeholder="请输入Grid地址" />
    </el-form-item>
    <el-form-item label="驱动地址" prop="driver_path" >
      <el-input v-model="ruleForm.driver_path" placeholder="请输入浏览器的驱动地址" />
    </el-form-item>
    <el-form-item label="浏览器参数" prop="browser_debug">
      <el-input
        v-model="ruleForm.browser_debug"
        :rows="8"
        type="textarea"
        placeholder='浏览器配置参数，格式如下：(按需配置)&#10;{&#10;# 谷歌配置&#10;"goog:chromeOptions": {
		"args": [
			"--headless", # 无头隐藏模式
			"--user-data-dir=d:\\tttt" # 浏览器数据保存位置
		]
	},
  # 火狐配置
	"moz:firefoxOptions": {
		"args": [
			"--headless" # 无头隐藏模式
		]
	}
}'/>
    </el-form-item>

    <el-form-item label="是否启动" prop="is_enabled">
      <el-radio-group v-model="ruleForm.is_enabled" class="ml-4">
        <el-radio value="1" size="large">启动</el-radio>
        <el-radio value="0" size="large">不启动</el-radio>
      </el-radio-group>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="submitForm(ruleFormRef)" >提交</el-button>
      <el-button @click="resetForm(ruleFormRef)">清空</el-button>
      <el-button @click="closeForm()">关闭</el-button>
    </el-form-item>
  </el-form>
</template>
  
<script lang="ts" setup>
import { ref, reactive } from "vue";
import { queryById, insertData, updateData } from "./WebBrowser.js"; // 不同页面不同的接口
import type { FormInstance, FormRules } from "element-plus";
import { useRouter } from "vue-router";

const router = useRouter();

// 1. 表单实例：用于默认数据，比如提交的时候
const ruleFormRef = ref<FormInstance>();

// 1-1 初始化保存数据的表单数据
const ruleForm = reactive({
  id: 0,
  name: "",
  enName: "",
  project_id: "",
  remote_url:"",
  driver_path:"",
  browser_debug:"",
  is_enabled: "",
});


// 2. 加载对应的所有项目的数据
import { queryAllProject } from "../project/WebProject.js"; // 不同页面不同的接口
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

// 3. 确定页面的必填字段
// 表单验证规则
const rules = reactive<any>({
  name: [{ required: true, message: "必填项", trigger: "blur" }],
  enName: [{ required: true, message: "必填项", trigger: "blur" }],
  project_id: [{ required: true, message: "必填项", trigger: "blur" }],
  state_value: [{ required: true, message: "必填项", trigger: "blur" }],
  is_enabled: [{ required: true, message: "必填项", trigger: "blur" }],
});

// 4. 提交功能
// 提交表单
const submitForm = async (form: FormInstance | undefined) => {
  if (!form) return;
  await form.validate((valid, fields) => {
    if (!valid) {
      return;
    }
    // 有ID代表是修改，没有ID代表是新增
    if (ruleForm.id > 0) {
      updateData(ruleForm).then(
        (res: { data: { code: number; msg: string } }) => {
          if (res.data.code == 200) {
            router.push("/WebBrowserList"); // 跳转回列表页面
          }
        }
      );
    } else {
      insertData(ruleForm).then(
        (res: { data: { code: number; msg: string } }) => {
          console.log(res);
          if (res.data.code == 200) {
            router.push("/WebBrowserList"); // 跳转回列表页面
          }
        }
      );
    }
  });
};

// 5. 编辑功能
// 5-1 加载表单数据
const loadData = async (id: number) => {
  const res = await queryById(id);
  ruleForm.id = res.data.data.id;
  ruleForm.name = res.data.data.name;
  ruleForm.enName = res.data.data.enName;
  ruleForm.project_id = res.data.data.project_id;
  ruleForm.remote_url = res.data.data.remote_url;
  ruleForm.driver_path = res.data.data.driver_path;
  ruleForm.browser_debug = res.data.data.browser_debug;
  ruleForm.is_enabled = res.data.data.is_enabled;
};

// 5-2 如果有id参数，说明是编辑，需要获取数据
let query_id = router.currentRoute.value.query.id;
ruleForm.id = query_id ? Number(query_id) : 0;
if (ruleForm.id > 0) {
  loadData(ruleForm.id);
}


// 6 清空--重置表单
const resetForm = (form: FormInstance | undefined) => {
  if (!form) return;
  form.resetFields();
};

// 7 关闭表单 - 回到数据列表页
const closeForm = () => {
  router.push("/WebBrowserList");
};


</script>
  