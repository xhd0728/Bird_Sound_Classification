<template>
  <div class="login flex items-center justify-center">
    <div class="rounded-md py-8 px-16 bg-white w-1/4 shadow-md" style="width:445px">
      <div class="text-center font-semibold text-xl">{{ isReg ? '注册' : '登录' }}</div>
      <div class="mt-4">
        <div class="text-xs my-1">用户名</div>
        <div class="border-b-2 px-2 flex items-center py-1">
          <i class="el-icon-user" />
          <input type="text" class="ml-2 w-full" placeholder="请输入用户名" v-model="username" />
        </div>
      </div>
      <div class="mt-4">
        <div class="text-xs my-1">密码</div>
        <div class="border-b-2 px-2 flex items-center py-1">
          <i class="el-icon-lock" />
          <input type="password" class="ml-2 w-full" placeholder="请输入密码" @keyup.enter="login" v-model="password" />
        </div>
      </div>
      <el-collapse-transition>
        <div v-show="isReg">
          <div class="mt-4">
            <div class="text-xs my-1">邮箱</div>
            <div class="border-b-2 px-2 flex items-center py-1 justify-between">
              <i class="el-icon-message" />
              <input type="text" class="ml-2 w-full" placeholder="请输入邮箱" v-model="email" />
              <div
                class="text-xs w-28 text-center text-gray-400"
                @click="verify"
              >{{ time == 0 ? '获取验证码' : time + 's后再获取' }}</div>
            </div>
          </div>
          <div class="mt-4">
            <div class="text-xs my-1">验证码</div>
            <div class="border-b-2 px-2 flex items-center py-1">
              <i class="el-icon-key" />
              <input type="text" class="ml-2 w-full" placeholder="请输入验证码" v-model="code" />
            </div>
          </div>
        </div>
      </el-collapse-transition>
      <div class="text-right underline">
        <el-link type="primary" @click="isReg = !isReg">{{ isReg ? '去登录' : '去注册' }}</el-link>
      </div>
      <div class="my-8">
        <button class="mybtn" @click="go">{{ isReg ? '注册' : '登录' }}</button>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      isReg: false,
      username: '',
      password: '',
      email: '',
      code: '',
      time: 0,
      timer: null,
    }
  },
  methods: {
    login() {
      this.request.normal
        .post('/api/v1/user/login', {
          username: this.username,
          password: this.password,
        })
        .then((res) => {
          this.$message({
            showClose: true,
            message: '登录成功',
            type: 'success'
          });
          // localStorage.setItem("access", res.data.token.access);
          // localStorage.setItem("refresh", res.data.token.refresh);
          localStorage.setItem("id", res.data.user.id);
          this.$router.push('/main');
          // console.log(123456);
        })
    },
    register() {
      if (this.username.length * this.password.length * this.email.length * this.code.length == 0) {
        this.$message({
          showClose: true,
          message: '请将信息填写完整',
          type: 'error'
        });
      } else {
        this.request.normal
          .post('/api/v1/user/register', {
            username: this.username,
            password: this.password,
            email: this.email,
            code: this.code,
          })
          .then(() => {
            this.$message({
              showClose: true,
              message: '注册成功',
              type: 'success'
            });
            this.isReg = false;
          })
      }
    },
    verify() {
      if (this.time > 0) return;
      else if (!/^[A-Za-z\d]+([-_.][A-Za-z\d]+)*@([A-Za-z\d]+[-.])+[A-Za-z\d]{2,5}$/.test(this.email)) {
        this.$message({
          showClose: true,
          message: '邮箱格式不正确',
          type: 'error'
        });
      }
      else {
        this.request.normal
          .post('/api/v1/user/email', {
            email: this.email
          })
          .then(() => {
            this.$message({
              showClose: true,
              message: '验证码邮件已发送',
              type: 'success'
            });

            this.time = 60;
            this.timer = setInterval(() => {
              this.time--;
              if (this.time <= 0) {
                clearInterval(this.timer)
              }
            }, 1000);
          })
      }

    },
    go() {
      if (this.isReg) {
        this.register();
      } else {
        this.login();
      }
    }
  }
}
</script>
<style scoped>
.login {
  height: 100vh;
  /* background: linear-gradient(45deg, #587578, #2f39c4); */
  background-image: url(../../public/images/bgc7.png);
  background-repeat: no-repeat;
  /* background-size: 1200px 1000px; */
  /* background-position-x: center; */
  /* background-position-y:center ; */
  background-size: cover;
}
input {
  border-width: 0;
  outline: 0px;
  color: #666;
  font-weight: 600;
  font-size: 0.875rem;
}
input::placeholder {
  color: #ddd;
}


</style>