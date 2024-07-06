import aiohttp
from aiohttp import web


async def sqli_vul(request):
    if request.method == 'POST':
        id = await request.post()
        if id.get('id') == '0\' union select 1,2,3,db_name()-- ':
            return web.Response(text="sqli success")
        else:
            return web.Response(text="sqli fail")
    elif request.method == 'GET':
        id = request.query.get('id')
        if id == '0\' union select 1,2,3,db_name()-- ':
            return web.Response(text="sqli success")
        else:
            return web.Response(text="sqli fail")
    else:
        return web.Response(text="Invalid request method")


async def xss_vul(request):
    if request.method == 'GET':
        url = request.query.get('url')
        if url == '<script>alert(1)</script>':
            return web.Response(text="xss success")
        else:
            return web.Response(text="xss fail")
    elif request.method == 'POST':
        url = await request.post()
        if url.get('url') == '<script>alert(1)</script>':
            return web.Response(text="xss success")
        else:
            return web.Response(text="xss fail")
    else:
        return web.Response(text="Invalid request method")


app = web.Application()
app.add_routes([web.get('/sqli_vul', sqli_vul), web.post('/sqli_vul', sqli_vul)])
app.add_routes([web.get('/xss_vul', xss_vul), web.post('/xss_vul', xss_vul)])

if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=8000)
