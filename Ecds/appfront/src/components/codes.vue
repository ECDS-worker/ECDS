<template>
  <div class="codes">
    <div id="yzm_code"></div>
    <button @click="button">按钮</button>
  </div>
    
</template>

<script>
    export default {
        name: "codes",
      data(){
           return{
        }
      },
     methods:{
       button:function(){
        this.$axios.get('api/v1/registcode').then(function(response){
           console.log(response)
         }).catch(function (error) {
          alert("请求错误")
         })
       }
     }

    }
</script>

<style scoped>

</style>
