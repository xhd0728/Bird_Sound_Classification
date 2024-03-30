import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import "tailwindcss/tailwind.css"
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import request from '@/axiosconfig.js'
import './assets/css/main.css'
import * as echarts from 'echarts'
Vue.prototype.$echarts = echarts
Vue.use(ElementUI)
Vue.prototype.request = request;

Vue.config.productionTip = false

new Vue({
  router,
  store,
  // echarts,
  render: h => h(App)
}).$mount('#app')
