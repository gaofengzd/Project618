<template>
  <div class="flight-analysis">
    <el-button @click="$router.back()" size="large" style="width: 10%; justify-content: flex-start;">
      <el-icon style="margin-right: 5px"><ArrowLeft /></el-icon>
      返回列表
    </el-button>
    <el-card class="control-panel">
      <div class="panel-header">
        <div class="flight-info">
          <h3>✈️ 航班数据分析: {{ flightId }}</h3>
          <span class="sub-text">请上传飞行数据文件进行分析</span>
        </div>

        <div class="upload-area">
          <el-upload
            action=""
            :auto-upload="false"
            :show-file-list="false"
            :on-change="handleFileChange"
            accept=".xlsx, .xls, .csv"
          >
            <el-button type="primary" size="large" icon="Upload">
              导入飞行数据文件
            </el-button>
          </el-upload>
        </div>
      </div>
    </el-card>

    <div class="charts-container" v-if="hasData">

      <el-card shadow="hover">
        <MultiTrendChart
          title="引擎转速监控 (N1 & N2)"
          unit="%"
          :xAxisData="timeAxis"
          :seriesList="engineData"
        />
      </el-card>

      <el-card shadow="hover">
        <MultiTrendChart
          title="飞行高度 (ALT)"
          unit="ft"
          :xAxisData="timeAxis"
          :seriesList="altData"
        />
      </el-card>

      <el-card shadow="hover">
        <MultiTrendChart
          title="液压系统压力 (HYD)"
          unit="PSI"
          :xAxisData="timeAxis"
          :seriesList="hydData"
        />
      </el-card>
    </div>

    <el-empty v-else description="暂无数据，请点击右上角导入文件" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import * as XLSX from 'xlsx'
import MultiTrendChart, { type SeriesItem } from '../components/MultiTrendChart.vue'

const route = useRoute()
const flightId = computed(() => route.params.id || '未知航班')
const hasData = ref(false)

// 数据源定义
const timeAxis = ref<string[]>([])
const engineData = ref<SeriesItem[]>([])
const altData = ref<SeriesItem[]>([])
const hydData = ref<SeriesItem[]>([])

// 处理文件上传
const handleFileChange = (uploadFile: any) => {
  const file = uploadFile.raw
  const reader = new FileReader()

  reader.onload = (e) => {
    const data = e.target?.result
    // 1. 解析 Excel/CSV
    const workbook = XLSX.read(data, { type: 'binary' })
    const firstSheetName = workbook.SheetNames[0]
    const worksheet = workbook.Sheets[firstSheetName]

    // 2. 转换为 JSON (每行一个对象)
    const jsonData: any[] = XLSX.utils.sheet_to_json(worksheet)

    if (jsonData.length > 0) {
      processData(jsonData)
    }
  }

  reader.readAsBinaryString(file)
}

// 处理数据并分发给图表
const processData = (data: any[]) => {
  // 重置数据
  timeAxis.value = []
  const n11: number[] = [], n12: number[] = [], n21: number[] = [], n22: number[] = []
  const alt: number[] = []
  const hydB: number[] = [], hydG: number[] = [], hydY: number[] = []

  // 遍历每一行数据
  data.forEach((row) => {
    // 假设第一列是时间 (根据你提供的CSV，第一列key可能是空字符串或其他)
    // 获取所有键值，找到第一个键作为时间键
    const keys = Object.keys(row)
    const timeKey = keys[0]

    timeAxis.value.push(Number(row[timeKey]).toFixed(2)) // 格式化时间

    // 提取 N1, N2
    n11.push(row['N11'] || 0)
    n12.push(row['N12'] || 0)
    n21.push(row['N21'] || 0)
    n22.push(row['N22'] || 0)

    // 提取 ALT
    alt.push(row['ALT'] || 0)

    // 提取 HYD
    hydB.push(row['HYD-B'] || 0)
    hydG.push(row['HYD-G'] || 0)
    hydY.push(row['HYD-Y'] || 0)
  })

  // 组装图表1数据: 引擎
  engineData.value = [
    { name: 'N11', data: n11, color: '#409EFF' },
    { name: 'N12', data: n12, color: '#67C23A' },
    { name: 'N21', data: n21, color: '#E6A23C' },
    { name: 'N22', data: n22, color: '#F56C6C' },
  ]

  // 组装图表2数据: 高度
  altData.value = [
    { name: 'ALT (高度)', data: alt, color: '#79bbff' }
  ]

  // 组装图表3数据: 液压
  hydData.value = [
    { name: 'HYD-Blue', data: hydB, color: '#409EFF' }, // 蓝系统用蓝色
    { name: 'HYD-Green', data: hydG, color: '#67C23A' }, // 绿系统用绿色
    { name: 'HYD-Yellow', data: hydY, color: '#E6A23C' }, // 黄系统用黄色
  ]

  hasData.value = true
}
</script>

<style scoped lang="scss">
.flight-analysis {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  h3 { margin: 0; font-size: 20px; color: #303133; }
  .sub-text { color: #909399; font-size: 14px; margin-top: 5px; display: block;}
}

.charts-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
