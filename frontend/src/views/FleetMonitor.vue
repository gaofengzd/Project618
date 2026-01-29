<template>
  <div class="fleet-monitor">
    <el-card class="filter-card">
      <el-form :inline="true">
        <el-form-item label="飞机注册号">
          <el-input placeholder="请输入" />
        </el-form-item>
        <el-form-item label="机型">
          <el-select placeholder="请选择" style="width: 120px">
            <el-option label="A320" value="A320"/>
            <el-option label="B737" value="B737"/>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search">搜索</el-button>
          <el-button icon="Refresh">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="card-grid">
      <el-card
        v-for="(plane, index) in planeList"
        :key="index"
        class="plane-card"
        :class="getStatusClass(plane.status)"
        shadow="hover"
      >
        <div class="card-header">
          <span class="plane-id">{{ plane.id }}</span>
          <span class="flight-no">{{ plane.flightNo }}</span>
          <span class="model">{{ plane.model }}</span>
        </div>
        <div class="card-status-bar">
          <span class="status-badge" :class="`bg-${plane.status}`">{{ plane.status }}</span>
        </div>
        <div class="card-body">
          <div class="info-row">
            <el-tag size="small" type="danger" effect="dark" v-if="plane.status === 'H'">参数1</el-tag>
            <el-tag size="small" type="warning" effect="dark" v-if="plane.status !== 'G'">参数2</el-tag>
            <el-tag size="small" type="success" effect="dark" v-if="plane.status === 'G'">正常</el-tag>
          </div>
          <div class="route-info">
            {{ plane.routeFrom }} <el-icon style="vertical-align: middle"><d-arrow-right /></el-icon> {{ plane.routeTo }}
          </div>
          <div class="time-info">{{ plane.time }}</div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const planeList = ref([
  { id: 'B-1234', flightNo: 'XXX2535', model: 'A320', status: 'H', routeFrom: 'LHD', routeTo: 'LAX', time: '2023-07-20 09:22' },
  { id: 'B-1235', flightNo: 'XXX3863', model: 'A320', status: 'M', routeFrom: 'CAN', routeTo: 'HGH', time: '2023-07-14 12:36' },
  { id: 'B-1236', flightNo: 'XXX405', model: 'A320', status: 'G', routeFrom: 'SZX', routeTo: 'FRA', time: '2023-02-06 17:33' },
  { id: 'B-1237', flightNo: 'XXX406', model: 'A320', status: 'G', routeFrom: 'SZX', routeTo: 'FRA', time: '2023-02-06 17:33' },
  { id: 'B-1238', flightNo: 'XXX407', model: 'A320', status: 'G', routeFrom: 'PEK', routeTo: 'SHA', time: '2023-02-06 18:00' },
])

const getStatusClass = (status: string) => {
  if (status === 'H') return 'border-h'
  if (status === 'M') return 'border-m'
  return 'border-g'
}
</script>

<style scoped lang="scss">
.filter-card { margin-bottom: 20px; }
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.plane-card {
  border-left: 6px solid transparent;
  cursor: pointer;
  &.border-h { border-left-color: #f56c6c; }
  &.border-m { border-left-color: #e6a23c; }
  &.border-g { border-left-color: #67c23a; }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 18px;
  margin-bottom: 10px;
  color: #303133;
}
.model { color: #909399; font-size: 14px; }
.card-status-bar { text-align: right; margin-bottom: 15px; }
.status-badge {
  padding: 4px 12px;
  border-radius: 4px;
  color: white;
  font-weight: bold;
  &.bg-H { background: #f56c6c; }
  &.bg-M { background: #e6a23c; }
  &.bg-G { background: #67c23a; }
}
.info-row { display: flex; gap: 5px; margin-bottom: 15px; min-height: 24px; }
.route-info { font-weight: bold; margin-bottom: 8px; font-size: 16px; }
.time-info { color: #999; font-size: 12px; }
</style>
