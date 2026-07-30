import time


class WindowTimer:

    def __init__(self, seconds=30):

        self.seconds = seconds

        self.start_time = time.time()

    # ---------------------------------------
    # Elapsed Time
    # ---------------------------------------
    def elapsed(self):

        return int(time.time() - self.start_time)

    # ---------------------------------------
    # Remaining Time
    # ---------------------------------------
    def remaining(self):

        remain = self.seconds - self.elapsed()

        return max(remain, 0)

    # ---------------------------------------
    # Finished
    # ---------------------------------------
    def finished(self):

        return self.elapsed() >= self.seconds

    # ---------------------------------------
    # Reset
    # ---------------------------------------
    def reset(self):

        self.start_time = time.time()