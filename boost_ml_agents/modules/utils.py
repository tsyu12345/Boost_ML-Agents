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
            #TODO;keybordInterruptで止める

        else:
            self._run()

    def stop(self, msg: str="Done"):
        self.running = False
        
        print(f"\n\r{msg} \r\n")

    def _run(self):
        while self.running:
            try:
                for char in "|/-\\":
                    print(f"\r{self.message} {char}", end="")
                    sleep(self.interval)
            except KeyboardInterrupt:
                break
        print("\r", end="\n")

if __name__ == "__main__":
    spinner = LoadingSpinner("Loading...")
    spinner.start(p_async=True)
    sleep(3)
    spinner.stop()
    print("Done!")