import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from tabulate import tabulate
from termcolor import colored,cprint

logo = """  _                                        _                          
(_)                                      (_)                         
 _         ___    ____    ____   _   _    _         ___    ___   ___ 
| |       / _ \  / _  |  |    \ | | | |  | |       / _ \  /___) /___)
| |_____ | |_| |( (_| |  | | | || |_| |  | |_____ | |_| ||___ ||___ |
|_______) \___/  \___ |  |_|_|_| \__  |  |_______) \___/ (___/ (___/ 
                (_____|         (____/                               
"""
print(colored(logo,"red"))
class DeletedFileHandler(FileSystemEventHandler):
    def __init__(self, path):
        self.path = path
        self.deleted_files = []

    def on_deleted(self, event):
        if not event.is_directory:
            self.deleted_files.append([event.src_path])

    def display_deleted_files(self):
        if self.deleted_files:
            cprint(f"Deleted files in {self.path}:", "red")
            print(tabulate(self.deleted_files, headers=['Deleted Files']))
            print("")

if __name__ == "__main__":
    paths_to_monitor = input("Enter paths to monitor (Ex: C:\): ").split(",")

    event_handlers = [DeletedFileHandler(path.strip()) for path in paths_to_monitor]
    observers = [Observer() for _ in range(len(paths_to_monitor))]

    for i, observer in enumerate(observers):
        observer.schedule(event_handlers[i], path=paths_to_monitor[i], recursive=True)
        observer.start()

    try:
        while True:
            for handler in event_handlers:
                handler.display_deleted_files()
            time.sleep(1)
    except KeyboardInterrupt:
        for observer in observers:
            observer.stop()
            observer.join()
