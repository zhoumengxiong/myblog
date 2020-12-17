### 安装步骤

- 创建python3虚拟环境（本地python版本：3.8.5）：
```
python3 -m venv venv  
```
- 激活虚拟环境
```
source venv/bin/activate
```
- 安装blog程序依赖包
```
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt
```
- 创建数据库（默认使用sqlite数据库）

```angular2html
flask initdb
```
- 创建数据库迁移
```angular2html
flask db init
flask db migrate
flask db upgrade
```
- blog初始化
```
flask initblog
```
- 生成虚拟数据（可选）
```
flask forge
```
- 运行
```
flask run
```
---

---
- 后台管理账号、密码
```
帐号：heypython@example.com
密码：heypython777
```