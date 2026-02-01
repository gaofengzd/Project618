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
            <span v-if="scope.row.takeoffStatus === 'normal'">正常</span>
            <el-tag v-else type="danger" effect="plain" style="cursor: pointer" @click="showTrendDialog(scope.row)">
              {{ scope.row.takeoffStatus }} <el-icon><TrendCharts /></el-icon>
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="下降状态">
          <template #default="scope">
            <el-tag v-if="scope.row.landingStatus !== 'normal'" type="danger" effect="plain">
              {{ scope.row.landingStatus }}
            </el-tag>
            <span v-else>正常</span>
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

    <el-dialog v-model="dialogVisible" :title="`异常趋势 - ${currentFlight}`" width="60%">
      <div v-if="dialogVisible">
        <TrendChart
          title="起飞阶段温度趋势"
          :x-axis-data="['00:00', '00:10', '00:20', '00:30', '00:40', '00:50']"
          :series-data="[20, 25, 30, 80, 75, 85]"
          :threshold="70"
          unit="℃"
        />
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import TrendChart from '../components/TrendChart.vue'

const router = useRouter()
const dialogVisible = ref(false)
const currentFlight = ref('')

// === 1. 数据定义 ===
// 原始数据 (Source of Truth)
const allTableData = [
  { fault: '压缩机出口温度过高', flightNo: 'XXX2535', planeId: 'B-1234', date: '2026-01-08 15:15', takeoffStatus: '温度异常(>80°C)', landingStatus: '温度波动' },
  { fault: '转速超阈值', flightNo: 'XXX2535', planeId: 'B-1234', date: '2026-01-08 15:15', takeoffStatus: '转速偏高', landingStatus: '正常' },
  { fault: '环境管道漏气', flightNo: 'XXX405', planeId: 'B-1236', date: '2026-02-01 16:20', takeoffStatus: 'normal', landingStatus: '压力异常' },
]

// 展示数据 (Display List)
const filteredTableData = ref([...allTableData])

// === 2. 搜索表单 ===
const searchForm = reactive({
  planeId: '',
  faultName: '', // 新增字段
  dateRange: [] as string[] // 存储 [开始日期, 结束日期]
})

// === 3. 核心搜索逻辑 ===
const handleSearch = () => {
  filteredTableData.value = allTableData.filter(item => {
    // 1. 匹配机号 (模糊搜索，忽略大小写)
    const matchId = !searchForm.planeId || item.planeId.toLowerCase().includes(searchForm.planeId.toLowerCase())
    // 2. 匹配故障名称 (新增逻辑：模糊搜索)
    const matchFault = !searchForm.faultName || item.fault.includes(searchForm.faultName)
    // 3. 匹配日期范围
    let matchDate = true
    if (searchForm.dateRange && searchForm.dateRange.length === 2) {
      const itemDate = new Date(item.date).getTime()
      const startDate = new Date(searchForm.dateRange[0] + ' 00:00:00').getTime()
      const endDate = new Date(searchForm.dateRange[1] + ' 23:59:59').getTime()

      matchDate = itemDate >= startDate && itemDate <= endDate
    }

    return matchId && matchFault && matchDate
  })
}

// 重置逻辑
const handleReset = () => {
  searchForm.planeId = ''
  searchForm.dateRange = []
  filteredTableData.value = [...allTableData]
}

// 其他交互逻辑
const showTrendDialog = (row: any) => {
  currentFlight.value = row.flightNo
  dialogVisible.value = true
}

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
