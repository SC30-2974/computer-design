import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import AgentRoom from '../views/AgentRoom.vue'
import FinancialAnalysis from '../views/FinancialAnalysis.vue'
import EnterpriseDetail from '../views/EnterpriseDetail.vue'
import DataUpload from '../views/DataUpload.vue'

// 路由主配置：采用主布局 + 子页面的方式。
// 这样左侧导航和顶部 Header 只渲染一次，右侧内容区随路由切换。
const router = createRouter({
  // 与 Vite BASE_URL 对齐，确保 GitHub Pages 子路径下路由可用。
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: MainLayout,
      redirect: '/home',
      children: [
        {
          path: 'home',
          name: 'home',
          component: Home,
          meta: { title: '主界面' },
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: Dashboard,
          meta: { title: '宏观行业大屏' },
        },
        {
          path: 'agent-room',
          name: 'agent-room',
          component: AgentRoom,
          meta: { title: '智能研判室' },
        },
        {
          path: 'financial-analysis',
          name: 'financial-analysis',
          component: FinancialAnalysis,
          meta: { title: '财务指标对比' },
        },
        {
          path: 'enterprise-detail',
          name: 'enterprise-detail',
          component: EnterpriseDetail,
          meta: { title: '企业详情' },
        },
        {
          path: 'data-upload',
          name: 'data-upload',
          component: DataUpload,
          meta: { title: '财报上传' },
        },
      ],
    },
  ],
})

// 根据路由标题动态更新浏览器标签，增强产品化细节。
router.afterEach((to) => {
  const title = to.meta.title || '新能源财报智能分析平台'
  document.title = `${title} - 新能源财报智能分析平台`
})

export default router
