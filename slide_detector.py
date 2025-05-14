import asyncio
from aiohttp import web

current_slide_id = None
slide_queue      = asyncio.Queue()

async def slide_change(request):
    global current_slide_id
    raw = request.query.get("hash", "")
    if raw.startswith("#slide="):
        new = raw.split("#slide=", 1)[1]
        print(f"[DETECTOR] {raw!r} → {new!r}")
        current_slide_id = new
        await slide_queue.put(new)
    return web.Response(text="ok", headers={
        "Access-Control-Allow-Origin": "*"
    })

async def slide_options(request):
    return web.Response(status=200, headers={
        "Access-Control-Allow-Origin": "*"
    })

async def healthz(request):
    return web.Response(text="ok")

def create_app():
    app = web.Application()
    app.add_routes([
        web.get ("/slide-change", slide_change),
        web.options("/slide-change", slide_options),
        web.get ("/healthz",       healthz),
    ])
    return app

if __name__ == "__main__":
    # Blocks until you press Ctrl+C
    web.run_app(create_app(), host="0.0.0.0", port=8765)