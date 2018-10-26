<script src="../../../../vue学习.js"></script>
<template>
  <div>
    <div class="login">
      <div class="from">
        <p><label></label><input type="text" name="username" v-model="username" placeholder="请输入用户名"></p>
        <p><input type="password" name="password" v-model="password" placeholder="请输入密码"></p>
        <div class="error err-show" v-show="errorTip">用户名或密码错误</div>
        <div>
          <a href="javascript:;" class="login_btn" @click="login">登陆</a>
        </div>
        <div>
          <p><input type="radio" name="radio" v-model="permission_code" value=1>首页</p>
          <p><input type="radio" name="radio" v-model="permission_code" value=2>首页2</p>
          <p><input type="radio" name="radio" v-model="permission_code" value=3>首页3</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "login",
    data() {
      return {
        username: '',
        password: '',
        errorTip: false,
        permission_code: ""
      }
    },
    methods: {
      login() {
        let Base64 = require("js-base64").Base64
               var result = [];
        for(var i=0;i<8;i++){
           var ranNum = Math.ceil(Math.random() * 25);
            result.push(String.fromCharCode(97+ranNum));
        }
         var rederom=[];
         for(var i=0;i<8;i++){
           var ranNum = Math.ceil(Math.random() * 25);
            rederom.push(String.fromCharCode(97+ranNum));
        }

        if (!this.username || !this.password) {
          this.errorTip = true;
          return
        } else {
          this.$axios.post('api/v1/session', {
            username:Base64.encode(result.join('')+this.username),
            password:Base64.encode(rederom.join('')+this.password),
            permission_code: this.permission_code
          }).then((json_response) => {
            let res = json_response.data;
            console.log(res);
            if (res.status == "200") {
              this.errorTip = false
              if (this.permission_code == 1) {
                this.$router.push({name: "index"})
              } else if (this.permission_code == 2) {
                this.$router.push({name: "index2"})
              } else {
                this.$router.push({name: "index3"})
              }

            } else {
              this.errorTip = true
            }
          })
        }


      }

    }

  }
</script>

<style scoped>

</style>
