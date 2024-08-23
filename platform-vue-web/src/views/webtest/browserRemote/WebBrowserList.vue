<template>
  <!-- 搜索表单 -->
  <el-form  ref="searchFormRef" :inline="true"  :model="searchForm" class="demo-form-inline">
     <el-form-item label="浏览器名称">
     <el-input v-model="searchForm.name" placeholder="根据名称筛选" clearable/>
     </el-form-item>

     <el-form-item label="所属项目ID" prop="project_id">
     <el-select v-model="searchForm.project_id" placeholder="选择所属项目" clearable >
      <!-- 通过项目进行筛选-需要加载所有的项目的数据 -->
      <el-option v-for="project in projectList" :key="project.id" :label="project.project_name" :value="project.id" />     
     </el-select>
     </el-form-item>
    
     <el-row class="mb-4" type="flex" justify="end">
      <el-button type="primary" @click="loadData()">查询</el-button>
      <el-button type="warning" @click="onDataForm(-1)">新增数据</el-button>
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
      :show-overflow-tooltip="true"
    >
    <template #default="scope">
      <span v-if="col.prop === 'is_enabled'">  
          {{ scope.row.is_enabled === "0"?'否' : scope.row.is_enabled === "1"?'是':'-' }}
      </span> 
    </template>
    </el-table-column>

    <!-- 操作 -->
    <el-table-column fixed="right" label="操作">
      <template #default="scope">
        <el-button link type="primary" size="small"  @click.prevent="onDataForm(scope.$index)">
          编辑
        </el-button>

        <el-button link type="primary" size="small"  @click.prevent="onDelete(scope.$index)">
          删除
        </el-button>
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
// 其他功能拓展
import { ref, reactive } from "vue";
import { queryByPage, deleteData } from "./WebBrowser.js"; // 不同页面不同的接口
import { useRouter } from "vue-router";
const router = useRouter();

// 分页参数
const currentPage = ref(1);
const pageSize = ref(10);
const total = ref(0);

// 搜索条件初始化
const searchForm = reactive({ "name": "", "project_id": ""  ,"page_id": ""});

// 1. 加载对应的数据进行显示
// 1-1 表格列 - 不同页面不同的列
const columnList = ref([
  { prop: "id", label: "编号" },
  { prop: "name", label: "浏览器名称" },
  { prop: "enName", label: "浏览器英文名" },
  { prop: "remote_url", label: "Grid地址" },
  { prop: "browser_debug", label: "浏览器调试参数" },
  { prop: "is_enabled", label: "是否启动" },
  // { prop: "create_time", label: "创建时间" },
]);

// 1-2 表格数据
const tableData = ref([]);

// 1-3 加载页面数据
const loadData = () => {
  let searchData = searchForm;
  searchData["page"] = currentPage.value;
  searchData["pageSize"] = pageSize.value;

  queryByPage(searchData).then(
    (res: { data: { data: never[]; total: number; msg: string } }) => {
      tableData.value = res.data.data;
      console.log(res.data.data)
      total.value = res.data.total;
    }
  );
};
loadData();


// 2. 搜索功能 - 筛选表单
// 2-1 加载出来所有的项目的数据：所有需要增加一个项目当中增加一个接口查询所有的数据
import { queryAllProject} from "../project/WebProject.js"; // 不同页面不同的接口
// import { queryByPage as queryByPageAllProject} from "../project/WebProject.js"; // 不同页面不同的接口

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


// 2-2 变更页大小
const handleSizeChange = (val: number) => {
  console.log("页大小变化:" + val);
  pageSize.value = val;
  loadData();
};

// 2-3 变更页码
const handleCurrentChange = (val: number) => {
  console.log("页码变化:" + val);
  currentPage.value = val;
  loadData();
};

// 3. 打开表单 （编辑/新增）
const onDataForm = (index: number) => {
  let params_data = {};
  if (index >= 0) {
    params_data = {
      id: tableData.value[index]["id"],
    };
  }
  router.push({
    path: "/WebBrowserForm", // 不同页面不同的表单路径
    query: params_data,
  });
};

// 4. 删除项目
const onDelete = (index: number) => {
    deleteData(tableData.value[index]["id"]).then((res: {}) => {
    loadData();
  });
};
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
  