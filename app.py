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
config.set_file('./config.yaml')
# config.set_file('config.yaml')


@click.group()
@click.option('-mat/-', default=False)  # /- 後面接其他command
def cli(mat):
    """
    Hello ~ 我是 mat，不是 matt，但你也可以把我當成 matt，有問題請找他。 \n
    use 'mat init' first to init, please. \n
    MAT 的用途是顯示特定 api 應正常回應之結果，將回應的結果 (json檔案) 放入 ./Data，並在 config 檔設定 server 與 router 即可使用!
    """
    pass


# @cli, not @click!
@cli.command('init', short_help='Create example_config file and show explain config file')
def init():
    filepath = r'.\config.yaml'
    if os.path.isfile(filepath):
        click.echo("***config file existence***")
        click.echo('--------------------------')
        click.echo('config.yaml :')
        pass
    else:
        click.echo('--------------------------')
        click.echo("config file not existence")
        click.echo('creat "config.yaml" and "data" for example')
        click.echo('--------------------------')
        click.echo('config.yaml :')

        # filename = os.path.realpath(__file__)
        # head_tail = os.path.split(filename)

        # click.echo(str(head_tail[0]))

        # with open(head_tail[0]+'/config.yaml', 'r') as f_config:
        #     doc = yaml.load(f_config)

        # click.echo(ruamel.yaml.round_trip_dump(doc, indent=2))

        with open('./config.yaml', 'w') as f:
            f.write(ruamel.yaml.round_trip_dump(
                config, default_flow_style=False))


    '''
    explanation = {
        'server': {
            'host': 'Your server host',
            'port': 'Your server port',
            'origin_proxy_url': 'Your origin_proxy_url',
        },
        'routes': [
            {
                'listen_path': 'One of server router',
                'file_path': 'call correspond json response according to the router',
                'status_code': 'just http status code',
            },
            {
                'listen_path': 'The other One of server router',
                'file_path': 'call correspond json response according to the router',
                'query_params': {
                    'params name ': 'params key'
                },
                'status_code': 'just http status code'
            }
        ]
    }

    explain_json = json.dumps(explanation, indent=2)
    click.echo(explain_json)
    '''
    path = "./data"
    if os.path.exists(path):
        click.echo('--------------------------')
        click.echo("***Data folder existence***")
        pass
    else:
        os.makedirs(path)

    data1 = [
        {
            "id": "home_hot",
            "title": "热门游戏",
            "connectionlinkcode": "hot",
            "images": {
                "general": "http://squirrel-dev.paradise-soft.com.tw/p/shark/ttmj/showroom_gamelobby/category/hot.png"
            },
            "subcategories": [

            ]
        },
        {
            "id": "home_recent",
            "title": "最近游玩",
            "connectionlinkcode": "recent",
            "images": {
                "general": "http://squirrel-dev.paradise-soft.com.tw/p/shark/ttmj/showroom_gamelobby/category/rcnt.png"
            },
            "subcategories": [
            ]
        }
    ]

    data2 = [
        {
            "name": "lottery",
            "category": [
                "fctc",
                "hk",
                "ssc",
                "wf",
                "js",
                "sf"
            ]
        }
    ]

    with open(r'.\data\v2_showrooms_home_categories.json', 'w', encoding='utf-8') as f:
        json.dump(data1, f, ensure_ascii=False, indent=4)

    with open(r'.\data\v1_products_category.json', 'w', encoding='utf-8') as f:
        json.dump(data2, f, ensure_ascii=False, indent=4)

    click.echo('--------------------------')
    click.echo('use "mat server" for next step')
    click.echo('use "mat conf" for more about config')

    click.echo('--------------------------')


@cli.command('server', short_help='start MAT')
def server():

    config = confuse.Configuration('mat', __name__)
    config.set_file('./config.yaml')
    temp_port = config['server']['port'].get(int)
    temp_host = config['server']['host'].get()

    click.echo('server...')
    app.run(
        # host=config['server']['host'].get(),
        # port=config['server']['port'].get(int),
        port=temp_port,
        host=temp_host,
    )


@cli.command('conf', short_help='about config file')
@click.option('--routes', nargs=3, help='input [listen path] [file path] [status code] to add a new router')
@click.option('--check', help='Check your port or host')
@click.option('--port', type=int, help='Change your port or host')
@click.option('--host', help='Change your host')
def conf(routes, check, port, host):
    '''
        It's about config file!
    '''

    config = confuse.Configuration('mat', __name__)
    config.set_file('./config.yaml')
    temp_port = config['server']['port'].get(int)
    temp_host = config['server']['host'].get()

    with open("./config.yaml") as f:
        doc = yaml.load(f)

    if routes:

        data_dict = [
            {
                'listen_path': routes[0],
                'file_path': routes[1],
                'status_code': routes[2],
            }
        ]

        with open("./config.yaml", 'a')as f:
            f.write(ruamel.yaml.round_trip_dump(
                data_dict, default_flow_style=False))

        click.echo('add' + str(data_dict))

    elif check == 'port':
        # conf_port = str(temp_port)
        click.echo('Ur port is : ' + str(temp_port))

    elif check == 'host':
        # conf_host = str(temp_host)
        click.echo('Ur host is : ' + str(temp_host))

    elif port:
        # with open("./config.yaml") as f:
        #     doc = yaml.load(f)
        doc['server']['port'] = port

        with open("./config.yaml", 'w') as fw:
            yaml.dump(doc, fw)

        # with open('./config.yaml', 'r') as fr:
        #     doc = yaml.load(fr)
            new_port = doc['server']['port']

        click.echo('Ur port is changed !' + str(new_port))

    elif host:
        # with open("./config.yaml") as f:
        #     doc = yaml.load(f)
        doc['server']['host'] = host

        with open("./config.yaml", 'w') as fw:
            yaml.dump(doc, fw)

        with open('./config.yaml', 'r') as fr:
            doc = yaml.load(fr)
            new_host = doc['server']['host']

        click.echo('Ur host is changed !' + new_host)
    else:
        # with open('./config.yaml', 'r') as fr:
        #     doc = yaml.load(fr)
        click.echo(ruamel.yaml.round_trip_dump(doc, indent=2))
        click.echo('--------------------------')
        click.echo('"--help" for more detail')
        click.echo('--------------------------')


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
