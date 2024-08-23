<template>
  <div>
    <!-- 搜索表单 -->
    <el-form ref="searchFormRef" :inline="true" :model="searchForm" class="demo-form-inline">
      <el-form-item label="WEB用例名称">
        <el-input v-model="searchForm.case_name" placeholder="根据Web用例名称筛选"  clearable/>
      </el-form-item>
      <el-form-item label="所属项目ID">
        <el-select
          v-model="searchForm.project_id" placeholder="根据项目名称筛选" clearable  >
          <el-option  v-for="project in projectList" :key="project.id"  :label="project.project_name" :value="project.id" />
        </el-select>
      </el-form-item>
      <el-row class="mb-4" type="flex" justify="end">
        <el-button type="primary" @click="loadData()">查询</el-button>
        <el-button type="warning" @click="onDataForm(-1)">新增用例</el-button>
      </el-row>
    </el-form>
    <!-- END 搜索表单 -->

    <!-- 数据表格 -->
    <el-table :data="tableData" style="width: 100%" max-height="500">
      <!-- 数据列 -->
      <el-table-column
        v-for="col in columnList" :prop="col.prop" :label="col.label" :key="col.prop" :show-overflow-tooltip="true">
        <template #default="scope">
          <span v-if="col.prop === 'is_pre'">
            {{
              scope.row.is_pre === "0"
                ? "否"
                : scope.row.is_pre === "1"
                ? "是"
                : "-"
            }}
          </span>
        </template>
      </el-table-column>
      <!-- 操作 -->
      <el-table-column fixed="right" label="操作">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="onDataForm(scope.$index)"
          >
            编辑
          </el-button>
          <el-button
            link
            type="primary"
            size="small"
            @click.prevent="onDelete(scope.$index)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
    <!-- END 数据表格 -->

    <!-- 分页 -->
    <div class="demo-pagination-block">
      <div class="demonstration"></div>
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    <!-- END 分页 -->
  </div>
</template>

  
<script lang="ts" setup>
import { ref, reactive } from "vue";
import { queryByPage, deleteData } from "./WebInfo.js"; // 不同页面不同的接口
import { useRouter } from "vue-router";

const router = useRouter();

// 分页参数
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 搜索功能 - 筛选表单
const searchForm = reactive({ case_name: "", project_id: "", module_id: "" });

// 表格列 - 不同页面不同的列
const columnList = ref([
  { prop: "id", label: "用例编号" },
  { prop: "case_name", label: "用例名称" },
  { prop: "case_desc", label: "用例描述" },
  { prop: "is_pre", label: "是否前置" },
  // ... 其他列 ...
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
      console.log(res.data.data);
      tableData.value = res.data.data;
      total.value = res.data.total;
    }
  );
};

loadData();

// 变更 页大小
const handleSizeChange = (val: number) => {
  console.log("页大小变化:" + val);
  pageSize.value = val;
  loadData();
};

// 变更 页码
const handleCurrentChange = (val: number) => {
  console.log("页码变化:" + val);
  currentPage.value = val;
  loadData();
};

// 打开表单（编辑/新增）
const onDataForm = (index: number) => {
  let params_data = {};
  if (index >= 0) {
    params_data = {
      id: tableData.value[index]["id"],
    };
  }
  router.push({
    path: "./WebInfoForm", // 不同页面不同的表单路径
    query: params_data,
  });
};

// 删除数据
const onDelete = (index: number) => {
  let searchData = searchForm;
  searchData["page"] = currentPage.value;
  searchData["pageSize"] = pageSize.value;
  deleteData(tableData.value[index]["id"]).then((res: {}) => {
  loadData();
  });
};

// 其他功能拓展
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
</script>
  
<style scoped>
.demo-pagination-block + .demo-pagination-block {
  margin-top: 10px;
}

.demo-pagination-block .demonstration {
  margin-bottom: 16px;
}

/* 更改 el-select 的宽度 */  
.el-select {  
  width: 200px; /* 设置你想要的宽度 */  
}  
</style>
  