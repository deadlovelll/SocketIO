"""
This module defines a file watcher that monitors specified directories for changes
and triggers a restart callback when Python files are modified.
"""

import time
import asyncio

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    
    """
    A handler for file system events that triggers a restart callback when a Python file is modified.

    Attributes:
        restart_callback (function): The callback function to invoke when a file modification event is detected.

    Methods:
        on_modified(event):
            Invoked when a file modification event occurs. If the event is a Python file, it triggers the restart callback.
    """
    
    def __init__ (
        self, 
        restart_callback
    ) -> None:
        
        """
        Initializes the FileChangeHandler with a restart callback.

        Args:
            restart_callback (function): The callback function to invoke on file modifications.
        """
        
        self.restart_callback = restart_callback

    def on_modified (
        self, 
        event,
    ) -> None:
        
        """
        Invoked when a file is modified. If the file is a Python file, it triggers the restart callback.

        Args:
            event (FileSystemEvent): The event representing the file system change.
        """
        
        if event.src_path.endswith(".py"):  # Restart only if Python files change
            print("Restarting server...")
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self.restart_callback())  
            except RuntimeError:
                asyncio.run(self.restart_callback())  

class FileWatcher:
    
    """
    A class for monitoring multiple directories for changes and invoking a restart callback
    when Python files are modified.

    Attributes:
        paths (list): A list of directories to monitor for file changes.
        restart_callback (function): The callback function to invoke when a file modification is detected.
        observer (Observer): The watchdog observer instance that tracks file system changes.

    Methods:
        start():
            Starts the file watcher and listens for file modifications in the specified directories.
    """
    
    def __init__ (
        self, 
        paths, 
        restart_callback,
    ) -> None:
        
        """
        Initializes the FileWatcher with directories to monitor and a restart callback.

        Args:
            paths (list): A list of paths (directories) to monitor.
            restart_callback (function): The callback function to invoke on file modifications.
        """
        
        self.paths = paths
        self.restart_callback = restart_callback
        self.observer = Observer()

    def start (
        self,
    ) -> None:
        
        """
        Starts the file watcher and listens for changes in the specified directories. 
        The observer will trigger the restart callback when a Python file is modified.

        This method blocks indefinitely until a KeyboardInterrupt is received.
        """
        
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