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
            <el-dropdown v-if="userStore.userInfo" trigger="click" @command="handleCommand">
              <span class="el-dropdown-link">
                <el-avatar :size="30" icon="UserFilled" style="margin-right: 8px; vertical-align: middle;" />
                {{ userStore.userInfo.username }} ({{ userStore.userInfo.role }})
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>

            <div v-else class="login-link" @click="showLoginDialog">
              <el-avatar :size="30" icon="User" />
              <span style="margin-left: 8px">点击登录</span>
            </div>
          </div>
        </el-header>

        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>

    <el-dialog v-model="loginVisible" title="用户登录" width="400px" center>
      <el-form :model="loginForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="loginForm.username" placeholder="请输入 (admin)" prefix-icon="User" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入 (123456)"
            show-password
            prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="loginVisible = false">取消</el-button>
          <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user' // 引入 User Store
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

// 路由逻辑
const activeMenu = computed(() => {
  if (route.path.includes('/fault-detail')) return '/fault-query'
  return route.path
})
const currentRouteName = computed(() => route.meta.title || '首页')

// ==== 登录逻辑 ====
const loginVisible = ref(false)
const loading = ref(false)
const loginForm = reactive({
  username: '',
  password: ''
})

const showLoginDialog = () => {
  loginVisible.value = true
  // 重置表单
  loginForm.username = ''
  loginForm.password = ''
}

const handleLogin = () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  // 模拟网络延迟
  setTimeout(() => {
    const success = userStore.login(loginForm)
    loading.value = false

    if (success) {
      ElMessage.success('登录成功')
      loginVisible.value = false
    } else {
      ElMessage.error('账号或密码错误 (试用 admin / 123456)')
    }
  }, 500)
}

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.info('已退出登录')
    router.push('/login') // 显式跳转回登录页
  }
}
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

/* 登录区域样式 */
.user-info {
  cursor: pointer;
  user-select: none;
}
.el-dropdown-link {
  display: flex;
  align-items: center;
  color: #606266;
  &:hover { color: #409EFF; }
}
.login-link {
  display: flex;
  align-items: center;
  color: #909399;
  &:hover { color: #409EFF; }
}
</style>
