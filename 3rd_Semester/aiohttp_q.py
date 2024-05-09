from aiohttp import web


async def test(request):
    return web.Response(text='hello')


app = web.Application()
app.router.add_get('/', test)

web.run_app(app)