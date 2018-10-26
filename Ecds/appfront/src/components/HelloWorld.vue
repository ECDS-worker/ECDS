<template>
  <div class="hello">
    <form>
      <input type="file" name="fileup" id="uploadEventFile" v-on:change="fileChange($event)" style="display:none"/>
    </form>
    <button v-on:click="importData($event)" class="imptbtn">导入excel</button>
    <button v-on:click="download()" class="imptbtn">下载</button>
  </div>
</template>

<script>
  export default {
    name: 'HelloWorld',
    data() {
      return {
        msg: 'Welcome to Your Vue.js App'
      }
    },
    methods: {
      // 导入excel文件
      importData: function (event) {
        event.preventDefault();
        $("#uploadEventFile").trigger("click")
      },
      fileChange: function (el) {
        el.preventDefault();//取消默认行为
        let vm = this
        let uploadEventFile = $("#uploadEventFile").val()
        this.file = el.target.files[0]
        if (uploadEventFile == '') {
          alert("请择excel,再上传");
        } else if (uploadEventFile.indexOf(".xls") > 0 || uploadEventFile.indexOf(".XLS") > 0) {

          let formData = new window.FormData();
          // 向 formData 对象中添加文件
          formData.append('file', this.file);
          let config = {
            // 一定要定义头
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          };
          // url为对应的后端接口
         //this.$axios.post('/api/v1/uploadfile', formData, config).then(function (response) {
          this.$axios.get('/api/question/', formData, config).then(function (response) {
            alert('上传成功')
            console.log(response)
          }).catch(function (error) {
          });
        } else {
          alert("只能上传excel,docx文件");
        }
      },
      // 下载文件
      download: function () {
        var data = {
          file: "asdasd",
          asdasd: "dfsds"

        };
        this.$axios({method: 'get', url: "/api/question/", data: data, responseType: 'blob',}).then((data) => {
            if (!data) {
              return
            }ii9
            let url = window.URL.createObjectURL(data.data);
            let link = document.createElement('a');
            link.style.display = 'none';
            link.href = url;
            link.setAttribute('download', 'excel.xls');
            document.body.appendChild(link);
            link.click()
          }).catch(function (error) {

        })
      }

    }
  }

</script>
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }
</style>
