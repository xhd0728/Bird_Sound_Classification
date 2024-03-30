import axios from 'axios'
import router from "./router"
import { Message } from 'element-ui'
import store from './store'
// import { Toast } from 'vant'

// const baseURL = 'http://localhost'  //本地
const baseURL = 'http://192.168.31.200:8000'  //远程服务器
let wsURL = `${baseURL.slice(8)}:81`;
//响应拦截器内使用：通过refresh_token刷新accesee_token函数
function getRefreshToken() {
  // 登录时已经获取token储存在localStorage中
  let token = localStorage.getItem('refresh');
  return normal
    .post("/api/user/refreshtoken", { refresh: token })
    .then((res) => {
      //console.log('刷新接口成功调用，等待下一步执行')
      localStorage.setItem("access", res.data.token.access);
      localStorage.setItem("refresh", res.data.token.refresh);
      return Promise.resolve();
    }
    )
}
//todo normal?
function logout() {
  normal.post("/api/user/logout", {
    token: localStorage.access,
    user_id: localStorage.id,
  });
  store.commit("logout");
  //this.toast("退出成功");
  tim.logout();
}

//实例1，不需要验证：
let normal = axios.create({
  baseURL,
  timeout: 20000  // 毫秒
})

normal.interceptors.response.use(
  response => {
    return response;
  },
  err => {
    Message({
      showClose: true,
          message: err.response.data.detail,
          type: 'error'
    })
    return Promise.reject(err)
  })


// 实例2--需要验证：
let instance = axios.create({
  baseURL,
  timeout: 20000,
})

//请求拦截器判断是否存在access_token
/*
instance.interceptors.request.use(
  req => {
    let access_token = localStorage.access;
    // 如果不存在字段，则跳转到登录页面

    if (!access_token) {
      // logout();
      //console.log('没有access字段跳的')
      // Toast("未登录状态请登录")

      // router.push({
      //   path: '/login',
      //   query: { redirect: router.currentRoute.fullPath }
      // });
      // 终止这个请求
      return Promise.reject();
    } else {
      req.headers.token = localStorage.getItem('access');
      req.headers.user_id = localStorage.getItem('id');
    }
    //如果存在，先传再说
    return req
  },
  err => {
    // console.log(112)
    return Promise.reject(err)
  }
)
*/
//响应拦截器做几件事
//0.成功啥也别管
//1.因为accesstoken过期失败，那么刷新重新获取,并重新设置
//2.如果refreshtoken过期失败，那么跳转到login
//3.如果一个接口正在刷新，那么其他接口先不刷新，储存起来到时一起刷新

// 是否正在刷新的标记
let isRefreshing = false;
// 重试队列，每一项将是一个待执行的函数形式
let requests = [];

instance.interceptors.response.use(
  response => {
    return response;
  },
  err => {

    // console.log('错误',err.response.status)
    // access_token过期
    if (err.response.data.detail === '过期') {
      // console.log('至少进来了不是吗')
      let config = err.response.config
      //接口未使用
      if (!isRefreshing) {
        isRefreshing = true
        // console.log('access_token过期，尝试刷新接口，刷新接口未使用，尝试刷新。本次被调用为',config)
        return getRefreshToken()
          //成功刷新
          .then(() => {
            // console.log('access_token刷新成功，现在接口储存着',requests.length,'个待执行，尝试重新发送之前的')
            // 重新请求
            // token = localStorage.access
            const token = localStorage.access
            let newdata = {}
            newdata = config.headers
            newdata.token = token
            config.headers = newdata
            //将requests里面的任务清空
            requests.forEach(cb => {
              // console.log('在这之前，先把开始把储存数据尝试刷新，目前有',requests.length,'个')
              cb(token)
            });
            requests = [];
            return instance(config)
              .then(
                res => {
                  // console.log('尝试重新发送之前发送成功了')
                  return Promise.resolve(res);
                })
              .catch(
                err0 => {
                  if (err0.response.status === 400) {
                    return Promise.reject(err0);
                  }
                  else if (err0.response.status === 401) {
                    //console.log(err0)
                    logout();
                    // router.push({
                    //   path: '/login'
                    // });
                    // Toast("登录状态已过期，请重新登录")
                    return Promise.reject(err0);
                  }
                  else {
                    return Promise.reject(err0);
                  }
                }
              )
          })
          //刷新失败
          .catch(err1 => {
            // console.log('access_token刷新失败，查看是401还是400错误')
            //400错误不跳转，返回报错
            // console.log(err1)
            if (err1.response.status === 400) {
              return Promise.reject(err1);
            }
            else if (err1.response.status === 401) {
              //console.log('401错误')
              logout();
              // router.push({
              //   path: '/login'
              // });
              // Toast("登录状态已过期，请重新登录")
              return Promise.reject(err1);
            }
            else {
              return Promise.reject(err1);
            }
          })
          .finally(() => {
            while (requests.length > 0) {
              requests.forEach(cb => {
                //console.log('运行过程中，又加了新的，目前有',requests.length,'个')
                cb(localStorage.access)
              });
              requests = [];
            }
            isRefreshing = false;
            //判断是否还有在里面的重新运行
          });
      }//接口正在刷新，添加队列
      else {
        // console.log('接口正在刷新,现在接口储存着',requests.length,'个待执行，包括我为',requests.length+1,'个,本次被调用为',config)
        return new Promise(resolve => {
          // 将resolve放进队列，用一个函数形式来保存，等token刷新后直接执行
          requests.push(token => {
            let newdata = {}

            newdata = config.headers
            newdata.token = token
            config.headers = newdata


            //console.log('本次任务解决：',config)
            resolve(instance(config));
          });
        });
      }
    }
    // 其他access_token违规跳转登录
    //console.log('到了这一步的话，说明违规登录和合理的错误没有分开')
    if (err.response.status === 400) {
      Message({
        showClose: true,
        message: err.response.data.detail,
        type: 'error'
      })
      return Promise.reject(err);
    }
    else if (err.response.status === 401) {
      logout();
      // router.push({
      //   path: '/login'
      // });
      // console.log(err.response)
      // Toast("登录状态已过期，请重新登录")
      // console.log(114)
      return Promise.reject(err);
    }
    else {
      // console.log(115)
      return Promise.reject(err);
    }
  }
);



export default {
  normal,
  instance,
  baseURL,
  wsURL,
}
