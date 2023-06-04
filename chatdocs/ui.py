import json
from queue import Queue
from threading import Thread
from typing import Any, Dict

from quart import Quart, render_template, websocket

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

    @app.get("/")
    async def index():
        return await render_template("index.html")

    @app.websocket("/ws")
    async def ws() -> None:
        while True:
            req = await receive()
            id, query = req["id"], req["query"]
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

    app.run(host="localhost", port=config["port"], use_reloader=False)
