<template>
  <div class="fault-detail">
    <el-button @click="$router.back()" icon="ArrowLeft" style="margin-bottom: 15px">返回列表</el-button>

    <el-card class="detail-header-card" shadow="never">
      <div class="header-content">
        <div class="item">
          <span class="label">故障类型：</span>
          <span class="value highlight">{{ currentFault.faultName }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">航班号：</span>
          <span class="value">{{ currentFault.flightNo }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">飞机号：</span>
          <span class="value">{{ currentFault.planeId }}</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">发生时间：</span>
          <span class="value">{{ currentFault.date }}</span>
        </div>
      </div>
    </el-card>

    <div class="charts-wrapper" v-if="currentFault.hasData">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header-title">
            <span class="dot red"></span> 起飞 - {{ currentFault.chart1Title }}
          </div>
        </template>
        <TrendChart
          :x-axis-data="timeData"
          :series-data="currentFault.takeoffData"
          :threshold="currentFault.threshold1"
          :unit="currentFault.unit"
          color="#F56C6C"
        />
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header-title">
            <span class="dot red"></span> 下降 - {{ currentFault.chart2Title }}
          </div>
        </template>
        <TrendChart
          :x-axis-data="timeData"
          :series-data="currentFault.descentData"
          :threshold="currentFault.threshold2"
          :unit="currentFault.unit"
          color="#F56C6C"
        />
      </el-card>
    </div>

    <el-empty v-else description="未找到该时间点的详细故障数据" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import TrendChart from '../components/TrendChart.vue'

const route = useRoute()

// 1. 获取 URL 中的参数
const paramId = computed(() => route.params.id as string) // 飞机号
const queryDate = computed(() => route.query.date as string) // 发生时间
const queryFault = computed(() => route.query.fault as string) // 故障名称

// X轴时间轴 (通用)
const timeData = ['00:00', '00:10', '00:20', '00:30', '00:40', '00:50', '01:00', '01:10', '01:20', '01:30', '01:40', '01:50']

// === 模拟后端数据库 (List 结构) ===
// 这种结构允许同一架飞机有多条不同时间的故障记录
const allFaultRecords = [
  // 记录 1: B-1234 的 高温故障
  {
    planeId: 'B-1234',
    flightNo: 'XXX2535',
    faultName: '压缩机出口温度过高',
    date: '2026-01-08 15:15', // 必须与查询列表的时间完全一致
    unit: '℃',
    hasData: true,
    chart1Title: '异常参数趋势 (温度异常 > 80℃)',
    threshold1: 70,
    takeoffData: [25, 26, 26, 58, 80, 85, 90, 95, 86, 88, 85, 80],
    chart2Title: '异常参数趋势 (温度波动)',
    threshold2: 70,
    descentData: [60, 62, 58, 55, 80, 48, 85, 42, 96, 38, 86, 30]
  },
  // 记录 2: B-1234 的 另一次故障 (同一架飞机，不同时间，不同故障)
  {
    planeId: 'B-1234',
    flightNo: 'XXX2535',
    faultName: '转速超阈值',
    date: '2026-01-08 15:15', // 假设同一时间发生的并发故障
    unit: 'RPM',
    hasData: true,
    chart1Title: '引擎转速监测',
    threshold1: 9000,
    takeoffData: [8000, 8100, 9500, 9600, 8500, 8200, 8000, 8000, 8000, 8000, 8000, 8000],
    chart2Title: '转速波动',
    threshold2: 9000,
    descentData: [5000, 4000, 3000, 2000, 1000, 800, 0, 0, 0, 0, 0, 0]
  },
  // 记录 3: B-1236 的 漏气故障
  {
    planeId: 'B-1236',
    flightNo: 'XXX405',
    faultName: '环境管道漏气',
    date: '2026-02-01 16:20',
    unit: 'PSI',
    hasData: true,
    chart1Title: '管道压力监测',
    threshold1: 40,
    takeoffData: [35, 35, 36, 35, 34, 35, 35, 36, 35, 34, 35, 35],
    chart2Title: '压力异常骤降',
    threshold2: 20,
    descentData: [35, 34, 30, 25, 15, 10, 8, 5, 5, 4, 2, 0]
  }
]

// 默认空数据对象
const defaultData = {
  planeId: '-',
  faultName: '未知故障',
  flightNo: '-',
  date: '-',
  unit: '',
  hasData: false, // 标记为无数据
  chart1Title: '', threshold1: 0, takeoffData: [],
  chart2Title: '', threshold2: 0, descentData: []
}

// === 核心逻辑：多条件精确查找 ===
const currentFault = computed(() => {
  // 在数据库中查找同时满足：飞机号、时间和故障名的记录
  const found = allFaultRecords.find(item => {
    // 1. 比对飞机号
    const matchId = item.planeId === paramId.value

    // 2. 比对时间 (如果列表页传的时间是完整字符串，直接全等比较)
    // 注意：实际项目中可能只需要比对到分钟，这里假设字符串完全一致
    const matchDate = item.date === queryDate.value

    // 3. 比对故障名称 (防止同一时间有多个不同故障)
    const matchFault = item.faultName === queryFault.value

    return matchId && matchDate && matchFault
  })

  return found || defaultData
})
</script>

<style scoped lang="scss">
.detail-header-card {
  background-color: #fff;
  margin-bottom: 20px;
  .header-content {
    display: flex;
    align-items: center;
    .item {
      display: flex; align-items: center;
      .label { color: #909399; margin-right: 8px; }
      .value { font-weight: 500; font-size: 16px; }
      .highlight { color: #f56c6c; font-weight: bold; }
    }
  }
}

.charts-wrapper { display: flex; flex-direction: column; gap: 20px; }

.card-header-title {
  display: flex; align-items: center; font-weight: bold; font-size: 15px;
  .dot {
    width: 8px; height: 8px; border-radius: 50%; margin-right: 10px;
    &.red { background: #f56c6c; }
  }
}
</style>
