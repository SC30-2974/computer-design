import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'
import './styles.css'

const app = createApp(App)

// 注册路由系统，让应用成为多页面 SPA。
app.use(router)
app.mount('#app')
