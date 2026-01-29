import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../components/MainLayout.vue'
import FleetMonitor from '../views/FleetMonitor.vue'
import FaultQuery from '../views/FaultQuery.vue'
import FaultDetail from '../views/FaultDetail.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      redirect: '/monitor',
      children: [
        {
          path: 'monitor',
          name: 'FleetMonitor',
          component: FleetMonitor,
          meta: { title: '机队监控' }
        },
        {
          path: 'fault-query',
          name: 'FaultQuery',
          component: FaultQuery,
          meta: { title: '故障查询' }
        },
        {
          path: 'fault-detail/:id',
          name: 'FaultDetail',
          component: FaultDetail,
          meta: { title: '故障详情' }
        }
      ]
    }
  ]
})

export default router
