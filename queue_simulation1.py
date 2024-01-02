import numpy as np
import threading
import time
from colorama import Fore, Style

class MM1K_Queue():
    """
    M/Ms/K queue: memoryless in, memoryless out, 1 server, K queue capacity
    """
    curr_capacity: int = 0      # curr elements in buffer
    wait_time_in: float = 0.0   # total waiting time for arrivals
    wait_time_out: float = 0.0  # total service time for departures
    in_elements: int = 0        # total incoming elements
    out_elements: int = 0       # total departing elements

    K: int
    in_scale: float
    out_scale: float

    def __init__(self, K: int=1000, in_scale: float=2, out_scale: float=2):
        self.K = K
        self.in_scale = in_scale
        self.out_scale = out_scale

    def _simulate_in(self):
        """
        simulates elements arriving at queue with exponentially distributed
        times between arrivals...
        """
        while (True):
            if (self.curr_capacity < self.K):
                wait_time: float = np.random.exponential(scale=self.in_scale)

                # update state
                self.wait_time_in += wait_time
                self.in_elements+= 1

                time.sleep(wait_time)
                self.curr_capacity += 1
                print(Fore.GREEN)
                print(f'\t-> arrival   - waiting = {self.curr_capacity}', \
                        f'waited {wait_time} secs.{Fore.RESET}')

    def _simulate_out(self):
        """
        simulates the server removing an element from the queue with 
        exponentially distributed times between removals
        """
        while (True):
            if (self.curr_capacity > 0):
                wait_time: float = np.random.exponential(scale=self.out_scale)

                # update state
                self.wait_time_out += wait_time
                self.out_elements += 1

                time.sleep(wait_time)
                self.curr_capacity -= 1
                print(Fore.RED)
                print(f'\t-> departure - waiting = {self.curr_capacity}', \
                        f'waited {wait_time} secs.{Fore.RESET}')

    def _disp_avg_wait_times(self):
        while (True):
            time.sleep(5)
            print(Style.DIM)
            print(f'avg. wait time in : {self.wait_time_in/self.in_elements}')
            print(f'avg. wait time out: {self.wait_time_out/self.out_elements}'\
                    , Style.RESET_ALL)


    def simulate_queue(self):
        """
        simulates queue traffic, both in an out. One thread handles the 
        input traffic, and one thread handles the output
        """
        # init threads
        in_thread: threading.Thread = \
                threading.Thread(target=self._simulate_in)
        server_thread: threading.Thread = \
                threading.Thread(target=self._simulate_out)
        info_thread: threading.Thread = \
                threading.Thread(target=self._disp_avg_wait_times)

        # launch the threads
        in_thread.start()
        server_thread.start()
        info_thread.start()

        # return threads so that they can be joined by main()
        return in_thread, server_thread, info_thread

def main():
    # more threads come in than out
    queue = MM1K_Queue(K=1000, in_scale=1, out_scale=2)
    in_thread, server_thread, info_thread = queue.simulate_queue()

    # runs for 100 seconds in total before halting
    time.sleep(100)

    in_thread.join()
    server_thread.join()
    info_thread.join()

if __name__ == '__main__':
    main()

