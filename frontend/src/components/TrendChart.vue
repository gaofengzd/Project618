<template>
  <div ref="chartContainer" class="chart-container"></div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'

interface Props {
  title?: string
  xAxisData: string[]
  seriesData: number[]
  unit?: string
  threshold?: number
  color?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  unit: '',
  color: '#f56c6c'
})

const chartContainer = ref<HTMLElement | null>(null)
let myChart: echarts.ECharts | null = null

const initChart = () => {
  if (!chartContainer.value) return

  // 避免重复初始化
  if (myChart) {
    myChart.dispose()
  }

  myChart = echarts.init(chartContainer.value)

  const option = {
    title: {
      text: props.title,
      left: 'center',
      textStyle: { fontSize: 14, fontWeight: 'bold' }
    },
    tooltip: {
      trigger: 'axis',
      formatter: `{b} <br/> {a}: {c} ${props.unit}`
    },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: props.xAxisData,
      boundaryGap: false,
      axisLine: { lineStyle: { color: '#999' } }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { type: 'dashed', color: '#eee' } }
    },
    series: [
      {
        name: '监测值',
        type: 'line',
        smooth: true,
        symbol: 'none',
        lineStyle: { width: 2, color: props.color },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: props.color + '33' },
            { offset: 1, color: props.color + '00' }
          ])
        },
        data: props.seriesData,
        markLine: props.threshold ? {
          silent: true,
          lineStyle: { color: '#E6A23C', type: 'dashed' },
          data: [{ yAxis: props.threshold, name: '阈值' }],
          label: { formatter: '{c}' }
        } : undefined
      }
    ]
  }
  myChart.setOption(option)
}

watch(() => props.seriesData, () => { initChart() }, { deep: true })

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
.chart-container { width: 100%; height: 300px; }
</style>
