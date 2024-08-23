<template>
    <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="120px" class="demo-ruleForm" status-icon>
      <el-form-item label="项目编号" prop="id">
        <el-input v-model="ruleForm.id" disabled />
      </el-form-item>
      <el-form-item label="所属项目ID" prop="project_id">
    <el-select v-model="ruleForm.project_id" placeholder="选择所属项目" @change="projectChange" clearable filterable>
          
      <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id"/>     
    </el-select>
  </el-form-item>
  <el-form-item label="所属页面ID" prop="page_id">
    <el-select v-model="ruleForm.page_id" placeholder="选择所属页面" clearable filterable>
      <el-option v-for="project in pageList" :key="project.id" :label="project.page_name" :value="project.id"/>     
    </el-select>
  </el-form-item>
      <el-form-item label="元素名称" prop="name">
        <el-input v-model="ruleForm.name" />
      </el-form-item>
      <el-form-item label="定位方式ID" prop="location_method_id">
    <el-select v-model="ruleForm.location_method_id" placeholder="选择定位方式" clearable filterable >
      <el-option v-for="project in locationMethod" :key="project.id" :label="project.location_method_name" :value="project.id"/>     
    </el-select>
  </el-form-item>
  <el-form-item label="表达式" prop="ele_location_exp" >
        <el-input v-model="ruleForm.ele_location_exp" placeholder="比如：Xpath、ID的值" />
  </el-form-item>
      <el-form-item label="元素描述" prop="ele_desc">
        <el-input v-model="ruleForm.ele_desc" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
        <el-button @click="resetForm(ruleFormRef)">清空</el-button>
        <el-button @click="closeForm()">关闭</el-button>
      </el-form-item>
    </el-form>
  </template>
  
  <script lang="ts" setup>
  import { ref, reactive } from "vue";
  import { queryById, insertData, updateData } from './WebPageEleManage.js'; // 不同页面不同的接口
  import type { FormInstance, FormRules } from 'element-plus';
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  // 表单实例
  const ruleFormRef = ref<FormInstance>();
  
  // 表单数据
  const ruleForm = reactive({
    id: 0,
    name: '',
    ele_desc: '',
    project_id:'',
    page_id: '',
    ele_location_exp:'',
    location_method_id:''
  });
  
  // 表单验证规则
  const rules = reactive<any>({
    name: [
      { required: true, message: '必填项', trigger: 'blur' }
    ],
    project_id: [
      { required: true, message: '必填项', trigger: 'blur' }
    ],
    page_id: [
      { required: true, message: '必填项', trigger: 'blur' }
    ],
    ele_location_exp: [
      { required: true, message: '必填项', trigger: 'blur' }
    ],
    location_method_id: [
      { required: true, message: '必填项', trigger: 'blur' }
    ]
  });
  
  // 提交表单
  const submitForm = async (form: FormInstance | undefined) => {
    if (!form) return;
    await form.validate((valid, fields) => {
      if (!valid) {
        return;
      }
      // 有ID代表是修改，没有ID代表是新增
      if (ruleForm.id > 0) {
        updateData(ruleForm).then((res: { data: { code: number; msg: string; }; }) => {
          if (res.data.code == 200) {
            router.push('/WebPageEleManageList'); // 跳转回列表页面
          }
        });
      } else {
        insertData(ruleForm).then((res: { data: { code: number; msg: string; }; }) => {
          console.log(res)
          if (res.data.code == 200) {
            router.push('/WebPageEleManageList'); // 跳转回列表页面
          }
        });
      }
    });
  };
  
  // 重置表单
  const resetForm = (form: FormInstance | undefined) => {
    if (!form) return;
    form.resetFields();
  };
  
  // 关闭表单 - 回到数据列表页
  const closeForm = () => {
    router.push('/WebPageEleManageList');
  };
  
  // 加载表单数据
  const loadData = async (id: number) => {
    const res = await queryById(id);
    ruleForm.id = res.data.data.id;
    ruleForm.project_id = res.data.data.project_id;
    ruleForm.page_id = res.data.data.page_id;
    ruleForm.name = res.data.data.name;
    // 定位方式
    ruleForm.location_method_id = res.data.data.location_method_id;
    ruleForm.ele_location_exp = res.data.data.ele_location_exp;
    ruleForm.ele_desc = res.data.data.ele_desc;
  };
  
  // 如果有id参数，说明是编辑，需要获取数据
  let query_id = router.currentRoute.value.query.id;
  ruleForm.id = query_id ? Number(query_id) : 0;
  if (ruleForm.id > 0) {
    loadData(ruleForm.id);
  }


  // 1. 加载数据：项目、模块、页面，根据实际情况添加
import { queryAllProject } from "../project/WebProject.js"; // 不同页面不同的接口
import { queryAll as queryAllPage } from "../pageManage/WebPage.js"; // 不同页面不同的接口
import { queryAll as queryAllLocationMethod} from "./WebEleLocationMethod.js"; // 不同页面不同的接口

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



const pageList = ref([{
  id: 0,
  page_name: '',
  page_desc: ''
}]);
function getPageList() {
  queryAllPage().then((res) => {
    pageList.value = res.data.data;
  });
}
getPageList();


const locationMethod = ref([{
  id: 0,
  location_method_name: '',
  location_method_desc: ''
}]);
function getLocationMethodList() {
  queryAllLocationMethod().then((res) => {
    locationMethod.value = res.data.data;
  });
}
getLocationMethodList();


// 根据项目ID加载对应的页面数据
import { queryByPage as apiWebPageQuery } from "../pagemanage/WebPage.js"; // 不同页面不同的接口
function getPageListForProject() { 
  apiWebPageQuery({
    "project_id": ruleForm.project_id,
    "page": 1,
    "pageSize": 999999
  }).then((res) => {
    pageList.value = res.data.data;
  });
}
const projectChange = (value: number) => { // 类型变动触发
  getPageListForProject()
}


</script>
  