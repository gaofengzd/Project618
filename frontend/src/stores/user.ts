import { defineStore } from 'pinia'
import { ref } from 'vue'
// import { useRouter } from 'vue-router' // 引入 router

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(JSON.parse(localStorage.getItem('user_info') || 'null'))
  const token = ref(localStorage.getItem('user_token') || '')

  // 注意：在 Store 内部直接使用 router 可能会在某些极端情况下报错
  // 更安全的做法是在组件层调用 router.push，但这里为了简便我们只处理数据

  const login = (form: any) => {
    if (form.username === 'admin' && form.password === '123456') {
      userInfo.value = { username: 'Admin', role: '系统管理员' }
      token.value = 'mock-token-12345'
      localStorage.setItem('user_info', JSON.stringify(userInfo.value))
      localStorage.setItem('user_token', token.value)
      return true
    }
    return false
  }

  const logout = () => {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('user_info')
    localStorage.removeItem('user_token')
    // 退出后，路由守卫会自动拦截并跳转到 Login，或者由组件显式跳转
  }

  return { userInfo, token, login, logout }
})
