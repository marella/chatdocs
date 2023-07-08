from watchdog.observers import Observer
from watchdog.events import FileSystemHandler
from .add import add

class AddHandler(FileSystemHandler):
    def on_modified(self, event):
        add(config: Dict[str])

def watchandadd(source_directory: str) -> None:
   observer = Observer()
   
