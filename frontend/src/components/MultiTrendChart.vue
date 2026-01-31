<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

// 定义单条曲线的数据结构
export interface SeriesItem {
  name: string
  data: number[]
  color?: string
}

interface Props {
  title?: string
  xAxisData: string[] // 时间轴
  seriesList: SeriesItem[] // 多条曲线数据
  unit?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  unit: ''
})

const chartContainer = ref<HTMLElement | null>(null)
let myChart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartContainer.value) return
  if (myChart) myChart.dispose()

  myChart = echarts.init(chartContainer.value)

  // 构建 Series 配置
  const echartsSeries = props.seriesList.map(item => ({
    name: item.name,
    type: 'line',
    smooth: true,
    symbol: 'none', // 去掉数据点的小圆圈，看起来更像波形
    data: item.data,
    lineStyle: item.color ? { color: item.color } : undefined,
    itemStyle: item.color ? { color: item.color } : undefined
  }))

  const option = {
    title: {
      text: props.title,
      left: 'center',
      textStyle: { fontSize: 14, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      order: 'valueDesc'
    },
    legend: {
      bottom: 0, // 图例放在底部
      data: props.seriesList.map(i => i.name)
    },
    grid: {
      top: '15%',
      left: '3%',
      right: '4%',
      bottom: '10%', // 留出空间给图例
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: props.xAxisData,
      axisLabel: { show: false } // 数据点太多时不显示X轴文字，保持整洁
    },
    yAxis: {
      type: 'value',
      name: props.unit,
      splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
    },
    series: echartsSeries
  }

  myChart.setOption(option)
}

watch(() => props.seriesList, () => { initChart() }, { deep: true })

const handleResize = () => myChart?.resize()

onMounted(() => {
  nextTick(() => {
    initChart()
    window.addEventListener('resize', handleResize)
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  myChart?.dispose()
})
</script>

<style scoped>
.chart-container { width: 100%; height: 350px; }
</style>
