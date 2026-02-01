<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <el-icon class="logo-icon"><Promotion /></el-icon>
        <h2>飞机故障检测平台</h2>
      </div>

      <el-form :model="loginForm" @submit.prevent :rules="rules" ref="loginFormRef" size="large">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="管理员账号 (admin)"
            prefix-icon="User"
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码 (123456)"
            show-password
            prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-btn" :loading="loading" @click.prevent="handleLogin">
            立即登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage, type FormInstance } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref<FormInstance>()
const loading = ref(false)

const loginForm = reactive({
  username: 'admin', // 默认填好方便测试
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async(valid) => {
    if (valid) {
      loading.value = true
      // 模拟登录延迟
      const success = await userStore.login(loginForm)
      loading.value = false

      if (success) {
        ElMessage.success('登录成功')
        router.push('/')
      } else {
        ElMessage.error('账号或密码错误')
      }
    }
  })
}
</script>

<style scoped lang="scss">
.login-container {
  height: 100vh;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #2d3a4b; /* 深色背景 */
  background-image: linear-gradient(135deg, #2d3a4b 0%, #1d2b36 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);

  .login-header {
    text-align: center;
    margin-bottom: 30px;
    color: #303133;

    .logo-icon {
      font-size: 40px;
      color: #409EFF;
      margin-bottom: 10px;
    }
    h2 { margin: 0; font-size: 22px; }
  }
}

.login-btn { width: 100%; }
</style>
