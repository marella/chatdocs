import json
import secrets
from queue import Queue
from threading import Thread
from typing import Any, Dict

from quart import Quart, render_template, websocket
from rich import print
from rich.panel import Panel

from .chains import get_retrieval_qa


async def receive():
    data = await websocket.receive()
    return json.loads(data)


async def send(data: Any):
    data = json.dumps(data)
    await websocket.send(data)


def ui(config: Dict[str, Any]) -> None:
    q = Queue()

    def callback(token: str) -> None:
        q.put(token)

    qa = get_retrieval_qa(config, callback=callback)

    def worker(query: str) -> None:
        res = qa(query)
        q.put(res)

    app = Quart(__name__, template_folder="data")
    auth = secrets.token_hex() if config["auth"] else None

    @app.get("/")
    async def index():
        return await render_template("index.html")

    @app.websocket("/ws")
    async def ws() -> None:
        while True:
            req = await receive()
            id, query = req["id"], req["query"]
            if auth and auth != req.get("auth"):
                print("Authentication error.")
                return
            Thread(target=worker, daemon=True, args=(query,)).start()

            done = False
            while not done:
                data = q.get()
                res = {"id": id}
                if isinstance(data, str):
                    res["chunk"] = data
                else:
                    res["result"] = data["result"]
                    res["sources"] = sources = []
                    for doc in data["source_documents"]:
                        source, content = doc.metadata["source"], doc.page_content
                        sources.append({"source": source, "content": content})
                    done = True

                await send(res)
                q.task_done()

    host, port = config["host"], config["port"]
    if auth:
        print(Panel(f"Visit [bright_blue]http://localhost:{port}?auth={auth}"))
    app.run(host=host, port=port, use_reloader=False)
