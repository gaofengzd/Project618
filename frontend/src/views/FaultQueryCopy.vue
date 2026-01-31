<template>
  <div class="fault-query">
    <el-card class="filter-card">
      <el-form :inline="true">
        <el-form-item label="飞机号">
          <el-input placeholder="请输入" />
        </el-form-item>
        <el-form-item label="日期">
          <div class="demo-datetime-picker">
            <div class="block">
              <el-date-picker
                v-model="value2"
                type="datetimerange"
                start-placeholder="Start date"
                end-placeholder="End date"
                format="YYYY-MM-DD HH:mm:ss"
                date-format="YYYY/MM/DD ddd"
                time-format="A hh:mm:ss"
              />
    </div>
  </div>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search">搜索</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <el-table :data="tableData" style="width: 100%" stripe>
        <el-table-column prop="fault" label="故障名称" width="180" />
        <el-table-column prop="flightNo" label="航班号" />
        <el-table-column prop="planeId" label="机号" />
        <el-table-column prop="date" label="发生时间" width="160" />

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
    </el-card>

    <el-dialog v-model="dialogVisible" title="异常数据趋势图" width="60%">
      <div v-if="dialogVisible">
         <TrendChart
          :title="`起飞 - ${currentFlight}`"
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TrendChart from '../components/TrendChart.vue'

const router = useRouter()
const dialogVisible = ref(false)
const currentFlight = ref('')

const tableData = [
  { fault: '压缩机出口温度过高', flightNo: 'XXX2535', planeId: 'B-1234', date: '2026-01-08 15:15', takeoffStatus: '温度异常(>80°C)', landingStatus: '压力波动' },
  { fault: '转速超阈值', flightNo: 'XXX2535', planeId: 'B-1234', date: '2026-01-08 15:15', takeoffStatus: '转速偏高', landingStatus: '正常' },
  { fault: '环境管道漏气', flightNo: 'XXX405', planeId: 'B-1236', date: '2026-01-08 16:20', takeoffStatus: 'normal', landingStatus: '压力异常' },
]

// 仅显示弹窗 (截图5功能)
const showTrendDialog = (row: any) => {
  currentFlight.value = row.flightNo
  dialogVisible.value = true
}

// 跳转详情页 (截图6功能)
const goToDetail = (row: any) => {
  router.push(`/fault-detail/${row.planeId}`)
}
const value2 = ref('')
</script>

<style scoped>
.filter-card { margin-bottom: 20px; }
@media (max-width: 768px) {
  .demo-datetime-picker .block {
    flex: 100%;
    border-bottom: solid 1px var(--el-border-color);
  }

  .demo-datetime-picker .block:last-child {
    border-bottom: none;
  }

  .line {
    display: none;
  }

  :deep(.el-date-editor.el-input) {
    width: 100%;
  }

  :deep(.el-date-editor.el-input__wrapper) {
    width: 100%;
    max-width: 300px;
  }
}
</style>
