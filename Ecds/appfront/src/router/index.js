import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import codes from '@/components/codes'
import login from '@/views/login'
import index from '@/views/index'
import index2 from '@/views/index2'
import index3 from '@/views/index3'
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
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
        {
      path: '/index',
      name: 'index',
      meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
      component: index
    },
            {
      path: '/index2',
      name: 'index2',
      meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
      component: index2
    },
            {
      path: '/index3',
      name: 'index3',
      meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
      component: index3
    },

  ]
})
