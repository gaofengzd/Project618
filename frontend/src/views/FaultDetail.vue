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
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import TrendChart from '../components/TrendChart.vue'
import axios from 'axios'

const route = useRoute()

// 1. 获取 URL 中的参数
const paramId = computed(() => route.params.id as string) // 飞机号
const queryDate = computed(() => route.query.date as string) // 发生时间
const queryFault = computed(() => route.query.fault as string) // 故障名称

// X轴时间轴 (通用)
const timeData = ['00:00', '00:10', '00:20', '00:30', '00:40', '00:50', '01:00', '01:10', '01:20', '01:30', '01:40', '01:50']

// === 修改点: 当前故障数据，初始为空 ===
const currentFault = ref({
  hasData: false,
  planeId: '',
  flightNo: '',
  faultName: '',
  date: '',
  chart1Title: '', threshold1: 0, takeoffData: [],
  chart2Title: '', threshold2: 0, descentData: [],
  unit: ''
})

// === 获取详情数据 ===
const fetchDetail = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:5000/plane/faults/detail', {
      planeId: paramId.value,
      date: queryDate.value,
      fault: queryFault.value
    })

    if (res.data.code === 200) {
      currentFault.value = res.data.data
    }
  } catch (e) {
    console.error('获取详情失败', e)
    // 可以在这里加个 ElMessage.error('获取详情失败')
  }
}

onMounted(() => {
  fetchDetail()
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
