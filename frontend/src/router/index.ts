import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'
import FleetMonitor from '../views/FleetMonitor.vue'
import FaultQuery from '../views/FaultQuery.vue'
import FaultDetail from '../views/FaultDetail.vue'
import FlightAnalysis from '../views/FlightAnalysis.vue'
import UserLogin from '../views/UserLogin.vue' // 1. 引入登录页
import { useUserStore } from '../stores/user' // 2. 引入 Store

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login', // 添加登录路由
      name: 'Login',
      component: UserLogin,
      meta: { title: '用户登录' }
    },
    {
      path: '/',
      component: MainLayout,
      redirect: '/monitor',
      // meta: { requiresAuth: true } 可以加这个标记，或者默认所有子路由都需要
      children: [
        { path: 'monitor', name: 'FleetMonitor', component: FleetMonitor, meta: { title: '机队监控' } },
        { path: 'fault-query', name: 'FaultQuery', component: FaultQuery, meta: { title: '故障查询' } },
        { path: 'fault-detail/:id', name: 'FaultDetail', component: FaultDetail, meta: { title: '故障详情' } },
        { path: 'analysis/:id', name: 'FlightAnalysis', component: FlightAnalysis, meta: { title: '数据分析' } }
      ]
    }
  ]
})

// 3. 全局前置守卫 (Global Guard)
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  // 如果用户已登录，但又想去登录页 -> 强制踢回首页
  if (to.path === '/login' && userStore.token) {
    next('/')
    return
  }

  // 如果用户未登录 (无token)，且去的不是登录页 -> 强制去登录页
  if (to.path !== '/login' && !userStore.token) {
    next('/login')
    return
  }

  // 其他情况放行
  next()
})

export default router
