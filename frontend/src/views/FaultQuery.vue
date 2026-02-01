<template>
  <div class="fault-query">
    <el-card class="filter-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="飞机号">
          <el-input
            v-model="searchForm.planeId"
            placeholder="请输入 (如 B-1234)"
            style="width: 150px"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="故障名称">
          <el-input
            v-model="searchForm.faultName"
            placeholder="支持模糊搜索(如 温度)"
            style="width: 170px"

            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="→"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            style="width: 230px;"
          />
        </el-form-item>
        <el-form-item>
        <!-- <el-form-item style="margin-bottom: 0; display: flex; justify-content: center; width: 100%;" class="no-margin-right">
          <div style="width: 100%; display: flex; justify-content: center;"> -->
            <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
            <el-button icon="Refresh" @click="handleReset">重置</el-button>
          <!-- </div> -->
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table :data="filteredTableData" style="width: 100%" stripe>
        <el-table-column prop="fault" label="故障名称" width="180" />
        <el-table-column prop="flightNo" label="航班号" />
        <el-table-column prop="planeId" label="机号" />
        <el-table-column prop="date" label="发生时间" width="160" sortable />

        <el-table-column label="起飞状态" width="150">
          <template #default="scope">
            <span v-if="scope.row.takeoffStatus === '正常' || scope.row.takeoffStatus === 'normal'">正常</span>
            <el-tag v-else type="danger" effect="plain" style="cursor: pointer">
              {{ scope.row.takeoffStatus }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="下降状态">
          <template #default="scope">
            <span v-if="scope.row.landingStatus === '正常' || scope.row.landingStatus === 'normal'">正常</span>
            <el-tag v-else type="danger" effect="plain" style="cursor: pointer">
              {{ scope.row.landingStatus }}
            </el-tag>
            <!-- <el-tag v-if="scope.row.landingStatus !== '正常' || scope.row.landingStatus !== 'normal'" type="danger" effect="plain">
              {{ scope.row.landingStatus }}
            </el-tag>
            <span v-else>正常</span> -->
          </template>
        </el-table-column>

        <el-table-column label="操作" width="120" fixed="right">
          <template #default="scope">
            <el-button size="small" type="primary" link @click="goToDetail(scope.row)">
              查看详情 >
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="filteredTableData.length === 0" description="暂无符合条件的故障记录" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
// const dialogVisible = ref(false)
// const currentFlight = ref('')

// === 1. 数据定义 ===
// 原始数据 (Source of Truth)
const filteredTableData = ref([])

// === 2. 搜索表单 ===
const searchForm = reactive({
  planeId: '',
  faultName: '', // 新增字段
  dateRange: [] as string[] // 存储 [开始日期, 结束日期]
})

// === 3. 核心搜索逻辑 ===
const handleSearch = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:5000//plane/faults/search', {
      planeId: searchForm.planeId,
      faultName: searchForm.faultName,
      dateRange: searchForm.dateRange
    })

    if (res.data.code === 200) {
      filteredTableData.value = res.data.data
    }
  } catch (e) {
    console.error('查询失败', e)
  }
}

// 重置逻辑
const handleReset = () => {
  searchForm.planeId = ''
  searchForm.faultName = ''
  searchForm.dateRange = []
  handleSearch() // 重置后立即查询所有
}

// 页面加载时自动查询
onMounted(() => {
  handleSearch()
})

// 其他交互逻辑
// const showTrendDialog = (row: any) => {
//   currentFlight.value = row.flightNo
//   dialogVisible.value = true
// }

const goToDetail = (row: any) => {
  // 使用 router.push 的对象写法，传递 query 参数
  router.push({
    name: 'FaultDetail', // 确保你的路由配置里给这个页面起了名字叫 FaultDetail
    params: { id: row.planeId },
    query: {
      date: row.date,
      fault: row.fault
    }
  })
}
</script>

<style scoped>
.filter-card { margin-bottom: 20px; }
</style>
