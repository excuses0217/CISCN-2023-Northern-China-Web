from scanner.scan import scan
from aiohttp import web
from urllib.parse import urlparse
import uuid


routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    with open('/app/front/index.html', 'r') as f:
        html_content = f.read()
    response = web.Response(text=html_content, content_type='text/html')
    return response


@routes.post('/scan_submit')
async def scan_submit(request):
    try:
        data = await request.json()
    except Exception as e:
        return web.Response(status=400, text="json struct error")

    if "url" in data and "module" in data and "pos" in data and "param_name" in data:
        url = data['url']
        module = data['module']
        pos = data['pos']
        param_name = data['param_name']

        if not is_valid_url(url):
            return web.Response(status=400, text="url is invalid")
        scan_result = await scan(url, module, pos, param_name)
        name = generate_log(module, scan_result)
        scan_result = {"report": name}

        return web.json_response(scan_result)

    else:
        return web.Response(text="need param")


def is_valid_url(url: str):
    if not url.startswith('http://'):
        return False
    if urlparse(url).netloc != '127.0.0.1:8000':
        return False
    return True


def generate_log(module, scan_result):
    file_name = '/app/views/' + str(uuid.uuid4()) + '.log'
    f = open(file_name, 'w')
    f.write(f'''{module} scan result:\n''')
    f.write('-' * 40 + '\n')
    for result in scan_result:
        f.write(result)
        f.write('\n'+'-'*40+'\n')
    f.close()
    return file_name.strip('/app/')


routes.static('/views', '/app/views')
app = web.Application()
app.add_routes(routes)
web.run_app(app, port=80)


