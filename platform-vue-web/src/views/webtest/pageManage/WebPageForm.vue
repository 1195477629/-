<template>
    <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="120px" class="demo-ruleForm" status-icon>
      <el-form-item label="页面编号" prop="id">
        <el-input v-model="ruleForm.id" disabled />
      </el-form-item>
      <el-form-item label="所属项目ID" prop="project_id">
    <el-select v-model="ruleForm.project_id" placeholder="选择所属项目" clearable filterable >
      <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />     
    </el-select>
    </el-form-item>
      <el-form-item label="页面名称" prop="page_name">
        <el-input v-model="ruleForm.page_name" />
      </el-form-item>
      <el-form-item label="页面描述" prop="page_des">
        <el-input v-model="ruleForm.page_desc" />
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
  import { queryById, insertData, updateData } from './WebPage.js'; // 不同页面不同的接口
  import type { FormInstance, FormRules } from 'element-plus';
  import { useRouter } from "vue-router";
  
  const router = useRouter();
  
  // 表单实例
  const ruleFormRef = ref<FormInstance>();
  
  // 表单数据
  const ruleForm = reactive({
    id: 0,
    project_id: '',
    page_name: '',
    page_desc: ''
  });
  
  // 表单验证规则
  const rules = reactive<any>({
    page_name: [
      { required: true, message: '必填项', trigger: 'blur' }
    ],
    project_id: [
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
            router.push('/WebPageList'); // 跳转回列表页面
          }
        });
      } else {
        insertData(ruleForm).then((res: { data: { code: number; msg: string; }; }) => {
          console.log(res)
          if (res.data.code == 200) {
            router.push('/WebPageList'); // 跳转回列表页面
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
    router.push('/WebPageList');
  };
  
  // 加载表单数据
  const loadData = async (id: number) => {
    const res = await queryById(id);
    ruleForm.id = res.data.data.id;
    ruleForm.project_id = res.data.data.project_id;
    ruleForm.page_name = res.data.data.page_name;
    ruleForm.page_desc = res.data.data.page_desc;
  };
  
  // 如果有id参数，说明是编辑，需要获取数据
  let query_id = router.currentRoute.value.query.id;
  ruleForm.id = query_id ? Number(query_id) : 0;
  if (ruleForm.id > 0) {
    loadData(ruleForm.id);
  }

  // 其他逻辑

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

</script>
  