// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import Axios from 'axios';
import 'jquery'

//全局使用axios
Vue.prototype.$axios = Axios;
//配置请求头，非常重要，有了这个才可以正常使用POST等请求后台数据
Axios.defaults.headers.post['Content-Type'] = 'application/x-www-fromurlencodeed'
Axios.defaults.withCredentials = true
Vue.config.productionTip = false
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
