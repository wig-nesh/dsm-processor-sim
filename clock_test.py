import threading
import time

class GlobalClock:
    def __init__(self, interval, callback):
        self.interval = interval  # Interval in seconds
        self.callback = callback  # Function to call on each tick
        self.running = False
        self.thread = None

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()

    def _run(self):
        while self.running:
            time.sleep(self.interval)
            self.callback()

    def stop(self):
        if self.running:
            self.running = False
            self.thread.join()

# Example callback function
def my_task():
    print("Clock ticked at", time.ctime())

freq = 10e2
clock = GlobalClock(1/freq, my_task)

# Start the clock
clock.start()

time.sleep(5)

# Stop the clock
clock.stop()
