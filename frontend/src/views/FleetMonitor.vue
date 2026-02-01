<template>
  <div class="fleet-monitor">
    <el-card class="filter-card">
      <el-form :inline="true" :model="searchForm">
        <el-form-item label="飞机号">
          <el-input
            v-model="searchForm.id"
            placeholder="请输入 (如 B-1234)"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="机型">
          <el-select
            v-model="searchForm.model"
            placeholder="请选择"
            style="width: 120px"
            clearable
          >
            <el-option label="A320" value="A320"/>
            <el-option label="B737" value="B737"/>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="handleSearch">搜索</el-button>
          <el-button icon="Refresh" @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div class="card-grid">
      <el-card
        v-for="(plane, index) in filteredPlaneList"
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
          <!-- <div class="info-row">
            <el-tag size="small" type="danger" effect="dark" v-if="plane.status === 'H'">参数1</el-tag>
            <el-tag size="small" type="warning" effect="dark" v-if="plane.status !== 'G'">参数2</el-tag>
            <el-tag size="small" type="success" effect="dark" v-if="plane.status === 'G'">正常</el-tag>
          </div> -->
          <div class="route-info">
            {{ plane.routeFrom }} <el-icon style="vertical-align: middle"><d-arrow-right /></el-icon> {{ plane.routeTo }}
          </div>
          <div class="time-info">{{ plane.time }}</div>
        </div>

        <div class="card-footer" style="margin-top: 15px; border-top: 1px solid #f0f0f0; padding-top: 10px; text-align: center;">
          <el-button type="primary" link @click.stop="goToAnalysis(plane.id)">
            <el-icon style="margin-right: 4px"><DataLine /></el-icon>
            <span style="font-size: 14px;">数据分析</span>
          </el-button>
        </div>
      </el-card>

      <el-empty
        v-if="filteredPlaneList.length === 0"
        description="没有找到符合条件的飞机"
        style="width: 100%; grid-column: 1 / -1;"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// === 1. 定义数据源 ===
// 原始数据 (Source of Truth)：这部分数据通常从后端 API 获取，这里写死作为模拟
const allPlanes = [
  { id: 'B-1234', flightNo: 'XXX2535', model: 'A320', status: 'H', routeFrom: 'LHD', routeTo: 'LAX', time: '2023-07-20 09:22' },
  { id: 'B-1235', flightNo: 'XXX3863', model: 'A320', status: 'M', routeFrom: 'CAN', routeTo: 'HGH', time: '2023-07-14 12:36' },
  { id: 'B-1236', flightNo: 'XXX405', model: 'A320', status: 'G', routeFrom: 'SZX', routeTo: 'FRA', time: '2023-02-06 17:33' },
  { id: 'B-1237', flightNo: 'XXX406', model: 'A320', status: 'G', routeFrom: 'SZX', routeTo: 'FRA', time: '2023-02-06 17:33' },
  { id: 'B-1238', flightNo: 'XXX407', model: 'B737', status: 'G', routeFrom: 'PEK', routeTo: 'SHA', time: '2023-02-06 18:00' },
  { id: 'B-9999', flightNo: 'XXX888', model: 'B737', status: 'M', routeFrom: 'CTU', routeTo: 'XIY', time: '2023-02-07 10:00' },
]

// 展示数据 (Display List)：页面 v-for 实际遍历的数组
const filteredPlaneList = ref([...allPlanes])

// === 2. 搜索表单状态 ===
const searchForm = reactive({
  id: '',
  model: ''
})

// === 3. 核心功能逻辑 ===

// 搜索功能
const handleSearch = () => {
  filteredPlaneList.value = allPlanes.filter(plane => {
    // 逻辑：如果输入框有值，就检查是否包含；如果为空，则默认为 true (不过滤)

    // 1. 匹配机号 (支持模糊搜索，忽略大小写)
    const matchId = !searchForm.id || plane.id.toLowerCase().includes(searchForm.id.toLowerCase())

    // 2. 匹配机型 (精确匹配)
    const matchModel = !searchForm.model || plane.model === searchForm.model

    return matchId && matchModel
  })
}

// 重置功能
const handleReset = () => {
  // 清空表单
  searchForm.id = ''
  searchForm.model = ''
  // 恢复列表为所有数据
  filteredPlaneList.value = [...allPlanes]
}

// 获取状态样式类
const getStatusClass = (status: string) => {
  if (status === 'H') return 'border-h'
  if (status === 'M') return 'border-m'
  return 'border-g'
}

// 跳转分析页
const goToAnalysis = (id: string) => {
  router.push(`/analysis/${id}`)
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
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-5px);
  }

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
