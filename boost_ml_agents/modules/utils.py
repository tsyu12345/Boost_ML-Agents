import os
from time import sleep
from threading import Thread

class LoadingSpinner:
    def __init__(self, message: str, interval: float = 0.1):
        self.message = message
        self.interval = interval
        self.running = False

    def start(self, p_async=False):
        if p_async:
            self.running = True
            Thread(target=self._run).start()
        else:
            self._run()
            
    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            for char in "|/-\\":
                print(f"\r{self.message} {char}", end="")
                sleep(self.interval)
        print("\r", end="")