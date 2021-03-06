import json
import shutil

import confuse as confuse
import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import click
import yaml
import os

app = Flask(__name__)
CORS(app)

config = confuse.Configuration('mat', __name__)
filepath_conf = 'config.yaml'
filepath_data = 'data'


@click.group()
@click.option('-mat/-', default=False)
def cli(mat):
    """
    Hello ~ 我是 mat，不是 matt，但你也可以把我當成 matt，有問題請找他。

    MAT 的用途是顯示特定 api 應正常回應之結果，將回應的結果 (json檔案) 放入 ./Data，並在 config 檔設定 server 與 router 即可使用!

    輸入 mat init 初始化
    """
    pass


@cli.command('init', short_help='初始化，建立 config file 和 data file')
def init():
    cur_dir = os.path.dirname(os.path.realpath(__file__))

    if os.path.exists(filepath_conf) == False:

        shutil.copyfile(cur_dir + '/config.yaml', './config.yaml')
        click.echo(f"""
    ---建立 config file 為範例
    ---mat : {cur_dir}
        """
                   )

    if os.path.exists(filepath_data) == False:

        shutil.copytree(cur_dir + '/data', './data')
        click.echo(f"""
    ---建立 data file 為範例
    ---mat : {cur_dir}
        """
                    )

    click.echo("""
    ---使用 mat server 來啟動 mat
    """
               )


@cli.command('server', short_help='啟動 mat')
def server():


    if os.path.exists(filepath_conf) == False:

        click.echo(f"""
    ---尚未建立 config file ， 使用 mat init 建立
        """
                   )


    config.set_file('./config.yaml')
    click.echo('server...')
    app.run(
        host=config['server']['host'].get(),
        port=config['server']['port'].get(int),
    )


@cli.command('conf', short_help='查看、更改設定檔')
@click.option('--port', help='更改設定檔的 port')
@click.option('--host', help='更改設定檔的 host')
def conf(port, host):

    if os.path.exists(filepath_conf) == False:

        click.echo("""
    ---尚未建立 config file ， 使用 mat init 建立
        """
                   )
        return

    with open("./config.yaml", 'r', encoding="utf-8") as fr:
        doc = yaml.load(fr,Loader=yaml.FullLoader)

    temp_port = doc['server']['port']
    temp_host = doc['server']['host']

    click.echo(f"""
    ------server------
    port : {temp_port}
    host : {temp_host}
    ------------------
    """)

    if port:
        doc['server']['port'] = int(port)
    if host:
        doc['server']['host'] = host
    if not (port or host):
        return

    with open("./config.yaml", 'w', encoding="utf-8") as fw:
        yaml.dump(doc, fw)

    new_port = doc['server']['port']
    new_host = doc['server']['host']

    click.echo(f"""
    ------Change------
    port : {new_port}
    host : {new_host}
    ------------------
    """)

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
    config.set_file('./config.yaml')
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
    config.set_file('./config.yaml')
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
    cli()
