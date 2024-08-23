import {
    createRouter,
    createWebHashHistory
} from 'vue-router'
import { useCookies } from '@vueuse/integrations/useCookies';

import NotFound from '~/views/404.vue'
import Login from '~/views/login/login.vue'
import Home from '~/views/home/home.vue'
import Statistics from '~/views/statistics/statistics.vue'
import userList from '~/views/users/userList.vue'
import userForm from '~/views/users/userForm.vue'

// WEB 自动化的对应的路由
import WebProjectList from '~/views/webtest/project/WebProjectList.vue'
import WebProjectForm from '~/views/webtest/project/WebProjectForm.vue'
import WebBrowserForm from '~/views/webtest/browserRemote/WebBrowserForm.vue'
import WebBrowserList from '~/views/webtest/browserRemote/WebBrowserList.vue'
import WebKeyWordList from '~/views/webtest/keyword/WebKeyWordList.vue'
import WebKeyWordForm from '~/views/webtest/keyword/WebKeyWordForm.vue'
import WebInfoList from '~/views/webtest/webinfo/WebInfoList.vue'
import WebInfoForm from '~/views/webtest/webinfo/WebInfoForm.vue'

import WebCollectionInfoList from '~/views/webtest/collection/WebCollectionInfoList.vue'
import WebCollectionInfoForm from '~/views/webtest/collection/WebCollectionInfoForm.vue'

import WebPageList from '~/views/webtest/pagemanage/WebPageList.vue'
import WebPageForm from '~/views/webtest/pagemanage/WebPageForm.vue'

import WebPageEleManageList from '~/views/webtest/pageelemanage/WebPageEleManageList.vue'
import WebPageEleManageForm from '~/views/webtest/pageelemanage/WebPageEleManageForm.vue'

const cookies = useCookies()
const routes = [
    {
        path: '/',
        redirect: '/login'
    }, {
        path: "/login",
        component: Login
    }, {
        path: "/home",
        component: Home,
        //子路由概念，后续所有的子页面都要放在这里
        children: [{
            path: "/Statistics",
            component: Statistics,
            meta: {
                title: "主页信息"
            }
        }, {
            path: "/userList",
            component: userList,
            meta: {
                title: "用户管理"
            }
        }, {
            path: "/userForm",
            component: userForm,
            meta: {
                title: "用户表单"
            }
        },        {
            path: "/WebProjectList",
            component: WebProjectList,
            meta: {
                title: "项目列表"
            }
        }, {
            path: "/WebProjectForm",
            component: WebProjectForm,
            meta: {
                title: "项目操作"
            }
        },{
            path: "/WebBrowserList",
            component: WebBrowserList,
            meta: {
                title: "浏览器列表页面"
            }
        },{
            path: "/WebBrowserForm",
            component: WebBrowserForm,
            meta: {
                title: "浏览器编辑页面"
            }
        }, {
            path: "/WebKeyWordList",
            component: WebKeyWordList,
            meta: {
                title: "关键字方法管理"
            }
        },{
            path: "/WebKeyWordForm",
            component: WebKeyWordForm,
            meta: {
                title: "关键字方法编辑"
            }
        },{
            path: "/WebInfoList",
            component: WebInfoList,
            meta: {
                title: "用例信息列表"
            }
        },{
            path: "/WebInfoForm",
            component: WebInfoForm,
            meta: {
                title: "用例信息管理"
            }
        },{
            path: "/WebCollectionInfoList",
            component: WebCollectionInfoList,
            meta: {
                title: "测试计划列表"
            }
        },{
            path: "/WebCollectionInfoForm",
            component: WebCollectionInfoForm,
            meta: {
                title: "测试计划管理"
            }
        },      {
            path: "/WebPageList",
            component: WebPageList,
            meta: {
                title: "页面列表页面"
            }
        }, 
         {
            path: "/WebPageForm",
            component: WebPageForm,
            meta: {
                title: "页面管理编辑"
            }
        }, {
            path: "/WebPageEleManageList",
            component: WebPageEleManageList,
            meta: {
                title: "页面元素列表"
            }
        }, {
            path: "/WebPageEleManageForm",
            component: WebPageEleManageForm,
            meta: {
                title: "页面元素编辑"
            }
        },
        ]
    },
    // 最后匹配不到的 都返回 404 !!!
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: NotFound
    }]

/** */
const router = createRouter({
    history: createWebHashHistory(),
    routes
})

//导航判断逻辑
router.beforeEach((to,from,next)=>{
    const token = cookies.get("l-token");
    if (to.path === '/login') {
        // 如果要前往登录页面，无需检查 token，直接跳转
        next();
    } else {
        // 如果不是前往登录页面，检查 token 是否存在
        if (token) {
            // 如果 token 存在，允许继续导航
            next();
        } else {
            // 如果 token 不存在，重定向到登录页面
            next('/login');
        }
    }
})

export default router