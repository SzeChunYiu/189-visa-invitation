import asyncio, json, websockets

APP="aaac76b5-ad30-477e-9ca0-472f8ab57fc8"
URL=f"wss://api.dynamic.reports.employment.gov.au/anonap/app/{APP}"
HDR={"Origin":"https://api.dynamic.reports.employment.gov.au"}

class Q:
    def __init__(self, ws): self.ws=ws; self.n=0
    async def call(self, method, handle, params):
        self.n+=1; i=self.n
        await self.ws.send(json.dumps({"jsonrpc":"2.0","id":i,"method":method,"handle":handle,"params":params}))
        while True:
            m=json.loads(await asyncio.wait_for(self.ws.recv(), 600))
            if m.get("id")==i:
                if "error" in m: raise RuntimeError(f"{method}: {m['error']}")
                return m["result"]

async def session(fn, retries=4):
    last=None
    for a in range(retries):
        try:
            async with websockets.connect(URL, additional_headers=HDR, max_size=None,
                                          open_timeout=60, ping_interval=None, close_timeout=10) as ws:
                await asyncio.wait_for(ws.recv(),60)
                q=Q(ws)
                doc=await q.call("OpenDoc",-1,[APP])
                return await fn(q, doc["qReturn"]["qHandle"])
        except Exception as e:
            last=e; print(f"  [retry {a+1}/{retries}] {type(e).__name__}: {str(e)[:120]}")
            await asyncio.sleep(5*(a+1))
    raise last
