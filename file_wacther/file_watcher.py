import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, restart_callback):
        self.restart_callback = restart_callback

    def on_modified(self, event):
        if event.src_path.endswith(".py"):  # Restart only if Python files change
            print(f"🔄 File changed: {event.src_path}. Restarting server...")
            self.restart_callback()

class FileWatcher:
    def __init__(self, paths, restart_callback):
        self.paths = paths
        self.restart_callback = restart_callback
        self.observer = Observer()

    def start(self):
        event_handler = FileChangeHandler(self.restart_callback)
        for path in self.paths:
            self.observer.schedule(event_handler, path, recursive=True)
        self.observer.start()
        print("👀 Watching for file changes...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
