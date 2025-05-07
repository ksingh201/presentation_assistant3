# slide_detector.py

import asyncio
from aiohttp import web
from slide_mapping import mapping

# Holds the last slide's objectId (e.g. "g12345")
current_slide_id: str | None = None
current_slide_index: int = 1

async def slide_change(request):
    """
    Handle GET /slide-change?hash=… from the browser.
    Extract the fragment ID, log it, and update current_slide_id.
    Return CORS‐enabled response so Chrome won't block the request.
    """
    raw_hash = request.query.get("hash", "")  # e.g. "#slide=id.g12345"

    if raw_hash.startswith("#slide=id."):
        new_id = raw_hash.split("#slide=id.", 1)[1]
        print(f"[DETECTOR] Received hash: {raw_hash!r} → parsed ID: {new_id!r}")
        index = mapping.update_current_slide(new_id)
        print(f"[DETECTOR] Mapped to slide index: {index}")
    else:
        print(f"[DETECTOR] Received non-slide hash: {raw_hash!r}")

    return web.Response(
        text="ok",
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

async def slide_options(request):
    """
    Handle preflight OPTIONS requests for CORS.
    """
    return web.Response(
        status=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )

async def run_detector():
    """
    Spin up an aiohttp server on port 8765 to receive slide-change callbacks.
    """
    app = web.Application()
    app.router.add_route("GET",     "/slide-change", slide_change)
    app.router.add_route("OPTIONS", "/slide-change", slide_options)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8765)
    await site.start()

    print("▶ Slide detector listening on http://localhost:8765/slide-change")

if __name__ == "__main__":
    asyncio.run(run_detector())