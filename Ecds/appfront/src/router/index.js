import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import codes from '@/components/codes'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
       {
      path: '/codes',
      name: 'codes',
      component: codes
    }
  ]
})
