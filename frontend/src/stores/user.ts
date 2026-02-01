import { defineStore } from 'pinia'
import { ref } from 'vue'
// import { useRouter } from 'vue-router' // 引入 router
import axios from 'axios' // 引入 axios

export const useUserStore = defineStore('user', () => {
  const userInfo = ref(JSON.parse(localStorage.getItem('user_info') || 'null'))
  const token = ref(localStorage.getItem('user_token') || '')

  // 注意：在 Store 内部直接使用 router 可能会在某些极端情况下报错
  // 更安全的做法是在组件层调用 router.push，但这里为了简便我们只处理数据

  const login = async (form: any) => {
    try {
      // 发送请求给 Flask 后端
      const res = await axios.post('http://127.0.0.1:5000/login', {
        username: form.username,
        password: form.password
      })

      // 判断后端返回的状态码 (根据 app.py 定义，成功是 200)
      if (res.data.code === 200) {
        const data = res.data.data

        // 更新状态
        userInfo.value = data.userInfo
        token.value = data.token

        // 持久化存储
        localStorage.setItem('user_info', JSON.stringify(userInfo.value))
        localStorage.setItem('user_token', token.value)

        return true
      } else {
        return false
      }
    } catch (error) {
      console.error('登录请求失败:', error)
      return false
    }
  }

  const logout = () => {
    userInfo.value = null
    token.value = ''
    localStorage.removeItem('user_info')
    localStorage.removeItem('user_token')
  }

  return { userInfo, token, login, logout }
})
