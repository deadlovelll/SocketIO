import time
import asyncio

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    
    def __init__ (
        self, 
        restart_callback
    ) -> None:
        
        self.restart_callback = restart_callback

    def on_modified (
        self, 
        event
    ):
        if event.src_path.endswith(".py"):  # Restart only if Python files change
            print("Restarting server...")
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.restart_callback())  
            except RuntimeError:
                asyncio.run(self.restart_callback())  

class FileWatcher:
    
    def __init__ (
        self, 
        paths, 
        restart_callback
    ) -> None:
        
        self.paths = paths
        self.restart_callback = restart_callback
        self.observer = Observer()

    def start (
        self
    ) -> None:
        
        event_handler = FileChangeHandler(self.restart_callback)
        
        for path in self.paths:
            self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()