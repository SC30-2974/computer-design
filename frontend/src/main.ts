import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles.css'

const app = createApp(App)

// Register router to enable SPA navigation.
app.use(router)
app.mount('#app')
