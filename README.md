### Aibee数据平台 - 数仓手册

### 使用前准备
- 本机环境 python 3.6.10 或以上。 （因为需要使用 python3 -m venv venv 生成 virtualenv)

### 环境准备
```bash
# 创建 venv
python3 -m venv venv
source venv/bin/activate
# 安装依赖
pip install --upgrade pip && pip install -r requirements.txt
```

### 创建 html 并预览
```bash
# 确定在虚拟环境中
source venv/bin/activate
# 清空上次创建
make clean
# 创建 html
make html
# 预览
open build/html/index.html

```

### 部署至 k8s
1. 创建 html. make html
2. 使用 upload_docker.sh, build docker 并上传 registry.aibee.cn/data_platform/dw-manual:0.0.1。
3. 部署在北京 idc 集群： bj-k8s-idc,  project: OpenFaas, namespace: openfass
4. 提交工单，申请域名 https://dw-manual.aibee.cn/
4. 参照文档 https://aibee.feishu.cn/docs/doccnQGJYV9DZgvraWvYMtEsXqf#94KO6C， 分别使用 deploy目录下的3个文件 dw-manual-deployment.yaml, dw-manual-service.yaml, dw-manual-ingress.yaml 进行 workload, service 和 load balancing 的部署。

### 升级 dw-manual
1. 创建 html. make html
2. 升级 docker image 版本。 使用 upload_docker.sh, build docker 并上传 registry.aibee.cn/data_platform/dw-manual:0.0.x。
3. 登录 rancher。 https://rancher.aibee.cn/， 找到 workload：  dw-manual-deployment， Edit， 然后修改 Docker image 版本并 Save 即可。 

### 如何手工添加新表?
- 以添加 dw_staging.ods_track_v1 为例说明。 
1. 首先确定添加至哪层目录(ods, dwd, dim, ads)？ dw_staging.ods_track_v1需要添加至 ods 目录
2. 打开 table/ods.rst, 加入数据表一览 ods/dw_staging.ods_track_v1
3. 打开 table/ods.csv, 加入表名和用途。 dw_staging.ods_track_v1, "Mall 客流上游数据，轨迹数据"
4. 根据目录下 rst 文件模板， 添加 ods/dw_staging.ods_track_v1.rst
5. 根据目录下 csv 文件模板， 添加 ods/dw_staging.ods_track_v1.csv
6. 创建 html 并预览。