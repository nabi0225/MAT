# MAT

顯示 api 應正常回應之結果

## 安裝

>使用 [pip](https://pip.pypa.io/en/stable/) 從 git 安裝 mat.

```bash
pip install git+https://github.com/nabi0225/MAT.git
```

## 使用方法

>初始化 mat，產生 config.yaml 與 Data 檔
```python
mat init
```
>啟動 mat
```python
mat server
```
>查看 server port 和 host
```python
mat conf
```
>更改 server port 和 host
```python
mat conf --port xxxx --host xxxx
```

>config.yaml
```yaml
server:
  host: 0.0.0.0   #server host
  port: 8000      #server port
  origin_proxy_url: http://xunya-apis.dev-ttmj.svc.cluster.local:8000   #代理的路由
routes:
  - listen_path: v2/showrooms/home/categories   #監聽的路由
    file_path: data/v2_showrooms_home_categories.json   #路由對應的 json 檔案
    status_code: 200    #http 狀態碼

  - listen_path: v1/products/category     #監聽的路由
    file_path: data/v1_products_category.json   #路由對應的 json 檔案
    query_params:
      categorycode: lottery   #路由 params 名稱 : params key
    status_code: 200    #http 狀態碼
```