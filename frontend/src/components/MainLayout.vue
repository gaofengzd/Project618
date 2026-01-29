<template>
  <div class="common-layout">
    <el-container>
      <el-aside width="220px" class="aside-menu">
        <div class="logo">
          <el-icon class="logo-icon"><Promotion /></el-icon>
          <span>飞机故障检测平台</span>
        </div>
        <el-menu
          active-text-color="#409EFF"
          background-color="#1d2b36"
          text-color="#fff"
          :default-active="activeMenu"
          router
        >
          <el-sub-menu index="1">
            <template #title>
              <el-icon><Monitor /></el-icon>
              <span>健康监测</span>
            </template>
            <el-menu-item index="/monitor">机队监控</el-menu-item>
            <el-menu-item index="/fault-query">故障查询</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header class="main-header">
          <div class="breadcrumb">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item>健康监测</el-breadcrumb-item>
              <el-breadcrumb-item>{{ currentRouteName }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="user-info">
            <el-avatar :size="30" icon="UserFilled" />
            <span style="margin-left: 10px">系统管理员</span>
          </div>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
// 处理详情页高亮问题：如果我们在详情页，保持“故障查询”菜单高亮
const activeMenu = computed(() => {
  if (route.path.includes('/fault-detail')) {
    return '/fault-query'
  }
  return route.path
})
const currentRouteName = computed(() => route.meta.title || '首页')
</script>

<style scoped lang="scss">
.common-layout, .el-container { height: 100vh; }
.aside-menu { background-color: #1d2b36; display: flex; flex-direction: column; }
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  background: #152028;
  font-weight: bold;
  gap: 10px;
}
.main-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #eee;
  background: #fff;
  height: 60px;
}
.main-content { background-color: #f5f7fa; padding: 20px; }
.user-info { display: flex; align-items: center; cursor: pointer; }
</style>
