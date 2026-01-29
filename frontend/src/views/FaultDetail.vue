<template>
  <div class="fault-detail">
    <el-button @click="$router.back()" icon="ArrowLeft" style="margin-bottom: 15px">返回列表</el-button>

    <el-card class="detail-header-card" shadow="never">
      <div class="header-content">
        <div class="item">
          <span class="label">故障类型：</span>
          <span class="value highlight">压缩机出口温度过高</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">航班号：</span>
          <span class="value">XXX2535</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">飞机号：</span>
          <span class="value">B-1234</span>
        </div>
        <el-divider direction="vertical" />
        <div class="item">
          <span class="label">发生时间：</span>
          <span class="value">2026-01-08 15:16</span>
        </div>
      </div>
    </el-card>

    <div class="charts-wrapper">
      <el-card class="chart-card">
        <template #header>
          <div class="card-header-title">
            <span class="dot red"></span> 起飞 - 异常参数趋势 (温度异常 > 80℃)
          </div>
        </template>
        <TrendChart
          :x-axis-data="timeData"
          :series-data="takeoffData"
          :threshold="33"
          unit="℃"
          color="#F56C6C"
        />
      </el-card>

      <el-card class="chart-card">
        <template #header>
          <div class="card-header-title">
            <span class="dot red"></span> 下降 - 异常参数趋势 (压力波动)
          </div>
        </template>
        <TrendChart
          :x-axis-data="timeData"
          :series-data="descentData"
          :threshold="33"
          unit="PSI"
          color="#F56C6C"
        />
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import TrendChart from '../components/TrendChart.vue'

const timeData = ['00:00', '00:10', '00:20', '00:30', '00:40', '00:50', '01:00', '01:10', '01:20', '01:30', '01:40', '01:50']
const takeoffData = [25, 26, 26, 58, 40, 52, 58, 54, 58, 45, 42, 50]
const descentData = [25, 18, 18, 56, 55, 55, 54, 38, 48, 45, 58, 60]
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
