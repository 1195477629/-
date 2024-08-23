<template>
    <!-- 搜索表单 -->
       <el-form ref="searchFormRef" :inline="true" :model="searchForm" class="demo-form-inline">
        <el-form-item label="元素名称">
              <el-input v-model="searchForm.name" placeholder="根据元素名称筛选" clearable />
          </el-form-item>
          <el-form-item label="所属项目ID">
          <el-select v-model="searchForm.project_id" placeholder="根据项目名称筛选" @change="projectChange" clearable>
          <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />
           </el-select>
          </el-form-item>
          <el-form-item label="所属页面ID" prop="page_id">
          <el-select v-model="searchForm.page_id" placeholder="根据项目名称筛选" clearable >
          <el-option v-for="project in pageList" :key="project.id" :label="project.page_name" :value="project.id"/>    
          </el-select>
          </el-form-item>
  
          <el-row class="mb-4" type="flex" justify="end"> <!-- 居右 type="flex" justify="end" -->
              <el-button type="primary" @click="loadData()">查询</el-button>
              <el-button type="warning" @click="onDataForm(-1)">新增元素</el-button>
          </el-row>
      </el-form>
    <!-- END 搜索表单 -->
  
    <!-- 数据表格 -->
    <el-table :data="tableData" style="width: 100%" max-height="500">
      <!-- 数据列 -->
      <el-table-column
        v-for="col in columnList"
        :prop="col.prop"
        :label="col.label"
        :key="col.prop"
        show-overflow-tooltip="true"
      />
      <!-- 操作 -->
      
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button link type="primary" size="small"  @click.prevent="onDataForm(scope.$index)" >编辑</el-button>
          <el-button link type="primary" size="small"  @click.prevent="onDelete(scope.$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  
    <!-- 分页 -->
    <div class="demo-pagination-block">
      <div class="demonstration"></div>
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    <!-- END 分页 -->
  </template>
    
    <script lang="ts" setup>
  import { ref, reactive } from "vue";
  import { queryByPage, deleteData } from "./WebPageEleManage.js"; // 不同页面不同的接口
  import { useRouter } from "vue-router";
  const router = useRouter();
  
  // 分页参数
  const currentPage = ref(1);
  const pageSize = ref(10);
  const total = ref(0);
  
  // 搜索功能 - 筛选表单
  const searchStatus = ref(false); // 是否应用搜索表单
  const searchForm = reactive({ "name": "", "project_id": "" , "module_id": "" ,"page_id": ""});
  
  // 表格列 - 不同页面不同的列
  const columnList = ref([
    { prop: "id", label: "元素编号" },
    { prop: "name", label: "元素名称" },
    // { prop: "location_method_id", label: "定位方式ID" },
    { prop: "location_method_name", label: "定位方式" },
    { prop: "ele_location_exp", label: "表达式" },
    { prop: "create_time", label: "创建时间" },
  ]);
  
  // 表格数据
  const tableData = ref([]);
  
  // 加载页面数据
  const loadData = () => {
    let searchData = searchForm;
    searchData["page"] = currentPage.value;
    searchData["pageSize"] = pageSize.value;
  
    queryByPage(searchData).then(
      (res: { data: { data: never[]; total: number; msg: string } }) => {
        tableData.value = res.data.data;
        total.value = res.data.total;
      }
    );
  };
  loadData();
  
  // 变更页大小
  const handleSizeChange = (val: number) => {
    console.log("页大小变化:" + val);
    pageSize.value = val;
    loadData();
  };
  
  // 变更页码
  const handleCurrentChange = (val: number) => {
    console.log("页码变化:" + val);
    currentPage.value = val;
    loadData();
  };
  
  // 打开表单 （编辑/新增）
  const onDataForm = (index: number) => {
    let params_data = {};
    if (index >= 0) {
      params_data = {
        id: tableData.value[index]["id"],
      };
    }
    router.push({
      path: "/WebPageEleManageForm", // 不同页面不同的表单路径
      query: params_data,
    });
  };
  
  // 删除项目
  const onDelete = (index: number) => {
      deleteData(tableData.value[index]["id"]).then((res: {}) => {
      loadData();
    });
  };
  
  
  // 其他功能拓展
  import { queryAllProject } from "../project/WebProject.js"; // 不同页面不同的接口
  import { queryAll as queryAllPage } from "../pageManage/WebPage.js"; // 不同页面不同的接口
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
  
  
  // 根据项目ID加载对应的页面数据
  import { queryByPage as apiWebPageQuery } from "../pageManage/WebPage.js"; // 不同页面不同的接口
  function getPageListForProject() { 
    apiWebPageQuery({
      "project_id": searchForm.project_id,
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
    
    <style scoped>
  .demo-pagination-block + .demo-pagination-block {
    margin-top: 10px;
  }
  
  .demo-pagination-block .demonstration {
    margin-bottom: 16px;
  }
  </style>
    