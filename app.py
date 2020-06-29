import json
import shutil

import confuse as confuse
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import click
import yaml
import config_with_yaml as configyaml
import os

import ruamel.yaml

app = Flask(__name__)
CORS(app)

config = confuse.Configuration('mat', __name__)

@click.group()
@click.option('-mat/-', default=False)
def cli(mat):
    """
    Hello ~ 我是 mat，不是 matt，但你也可以把我當成 matt，有問題請找他。

    MAT 的用途是顯示特定 api 應正常回應之結果，將回應的結果 (json檔案) 放入 ./Data，並在 config 檔設定 server 與 router 即可使用!

    輸入 mat init 初始化
    """
    pass


@cli.command('init', short_help='建立 config file 和 data file')
def init():
    filepath = 'config.yaml'
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(filepath):

        click.echo(
            """
    ---config file 已存在
        """
        )
        pass

    else:
        click.echo(
            f"""
    ---建立 "config.yaml" 和 "data" 為範例
    ---mat : {cur_dir}
    """
        )

        shutil.copytree(cur_dir + '/data', './data')
        shutil.copyfile(cur_dir + '/config.yaml', './config.yaml')

    explanation = {
        'server': {
            'host': 'server host',
            'port': 'server port',
            'origin_proxy_url': '代理的路由',
        },
        'routes': [
            {
                'listen_path': '監聽的路由',
                'file_path': '路由對應的 json 檔案',
                'status_code': 'http status code',
            },
            {
                'listen_path': '監聽的路由',
                'file_path': '路由對應的 json 檔案',
                'query_params': {
                    ' 路由 params 名稱': 'params key'
                },
                'status_code': 'http status code'
            }
        ]
    }

    explain_json = json.dumps(explanation, ensure_ascii=False, indent=2)
    click.echo(
        f"""
    ---config file 內容 :
    {explain_json}
    -----------------
        """
    )

    click.echo(
        """
    ---使用 mat server 來啟動 mat
        """
    )


@cli.command('server', short_help='start MAT')
def server():
    config.set_file('./config.yaml')
    click.echo('server...')
    app.run(
        host=config['server']['host'].get(),
        port=config['server']['port'].get(int),
    )


@cli.command('check', short_help='check port and host')
def check():

    with open("./config.yaml", 'r') as fr:
        doc = yaml.load(fr)

    temp_port = doc['server']['port']
    temp_host = doc['server']['host']

    click.echo(
        f"""
    ------server------
    port : {temp_port}
    host : {temp_host}
    ------------------
        """
    )

@cli.command('conf', short_help='about server')
@click.option('--port', '--host', multiple=True, help='更改 server 的 port 和 host')
def conf(port):

    with open("./config.yaml", 'r') as fr:
        doc = yaml.load(fr)

    doc['server']['port'] = int(port[0])
    doc['server']['host'] = port[1]

    with open("./config.yaml", 'w') as fw:
        yaml.dump(doc, fw)

    new_port = doc['server']['port']
    new_host = doc['server']['host']

    click.echo(
        f"""
    ------Change------
    port : {new_port}
    host : {new_host}
    ------------------
        """
    )


'''
@cli.command('routes', short_help='about router')
@click.option('--listen', '--file', '--status', help='input [listen path] [file path] [status code] to add a new router', multiple=True)
def routes(listen):

    data_dict = [
        {
            'listen_path': listen[0],
            'file_path': listen[1],
            'status_code': listen[2],
        }
    ]

    with open("./config.yaml", 'a')as fa:
        fa.write(ruamel.yaml.round_trip_dump(
            data_dict, default_flow_style=False))

    with open("./config.yaml", 'r') as f:
        doc = yaml.load(f)

    click.echo(
        f"""
        add {data_dict}
        {ruamel.yaml.round_trip_dump(doc, indent=2)}
        """)
'''

@app.route('/')
def hello_world():
    config.set_file('./config.yaml')
    route_data = '\n'.join(
        f"<li>{route['listen_path']}</li>" for route in config['routes'].get(list))
    origin_proxy_url = config['server']['origin_proxy_url'].get()

    return f"""
    <p>我是 mat，不是 matt，但你也可以把我當成 matt，有問題請找他。</p>
    
    <p>目前的假 API 有：</p>
    
    <ul>
    {route_data}
    </ul>

    <p>如果不存在假 API 會自動導向： {origin_proxy_url}</p>
    """


@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    res = _get_mock_response(path)
    if not res:
        res = _get_response_from_proxy_server(path)
    return res


def _get_mock_response(path):
    # Fake API 只支援 GET
    if request.method != 'GET':
        return None

    routes = config['routes'].get(list)
    for route in routes:
        if path != route['listen_path']:
            continue

        if 'query_params' in route:
            for key, value in route['query_params'].items():
                if value != request.args.get(key):
                    return None

        with open(route['file_path'], encoding='utf-8') as fp:
            json_data = json.loads(fp.read())
        return jsonify(json_data), route['status_code'], {'Mat': 'This is a mock API'}


def _get_response_from_proxy_server(path):
    origin_proxy_url = config['server']['origin_proxy_url'].get()
    data = request.stream.read()
    req = requests.Request(
        method=request.method,
        url=f'{origin_proxy_url}/{path}?{request.query_string.decode()}',
        headers=request.headers,
        data=data,
    )
    resp = requests.Session().send(req.prepare(), stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


if __name__ == '__main__':
    # app.run(
    #     host=config['server']['host'].get(),
    #     port=config['server']['port'].get(int),
    # )
    cli()
