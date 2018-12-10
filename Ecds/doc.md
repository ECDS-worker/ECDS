## 主页接口

#### 主页显示接口
* method: GET

* api: api/v1/index

* body: None

* response: 
```json
    {
      "username": "",
      "notice": [{
        "title": "",
        "time": ""
      }],
      "index_file": [{
        "title": ""
      }]
    }
```

#### 主页公告内容显示接口

* method: GET

* api: api/v1/notice

* body: 
- filename: 选中的文件名称

* response:
```json
    {
      "title": ""
    }
```


#### 更多公告内容

* menthod: GET

* api: api/v1/notice

* body: None

* response:
```json
    {
      "title": []
    }
```

#### 技术支持文件下载

* method: GET

* api: api/v1/filedownload

* body: 
- filename : 文件名称
- filetype: 不同页面对应不同下载的功能，以字符区分

* response:
- response


#### 申请信息页面

* method: post

* api: api/v1/applyinfo

* body: 
- 

* response
```json

```

#### 时间窗口查询

* method: post

* api: api/v1/serchtime

* body: 
- 

* response
```json

```






#### 机构基础信息
* method: post

* api: api/v1/ApplyInfomation

* body: 
- 1、
- id: 1
- ins_nm: "单位名称"
- contact: "单位联系人"
- phone: "联系电话"
- email: "邮箱"
- fax: "传真"

- 2、
- id: 2
- system: "系统选择"

- 3、
- id: 3
- start_time: "开始时间"
- end_time: "结束时间"

- 4、
- id: 4
- soft_nm: "接口软件信息"
- soft_ty: "软件版本"
- mid_nm_ty: "中间件及版本"
- operate_type: "操作系统及版本"

- 5、
- id: 5
- net_ty: "0或1"
- first_access: "0或1 是否首次接入"

- 6、
- id: 6
- access_obj: "接入目的"

- 7、
- id: 7
- ins_nm: "参与机构名称"
- ins_cd: "行号"
- mid_ty: "中间件类型"
- port: "端口"
- access_port: "接入点号"

- 8、
- id: 8
- user_nm: "用户名称"
- role: "角色"
- phone: 
- email:



* response
```json
    {
      "msg": "200"
    }
```

