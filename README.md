# Markov Chain Queueing Sim

## Introduction 

The script simulates a $M/M/s/K$ queue.

- $M$: Memoryless arrival times of new elements to the queue. Memoryless here
refering to exponentially distributed with, i.e. arrival times are separated
by distribution $f(t) = e^{-\lambda t}$
- $M$: Memoryless departure times of leaving elements. Same idea as previous
point
- $s$: Number of servers of the queue
- $K$: Capacity of the buffer

## Implementation

I decided for now to implement a $M/M/1/1000$ queue. I.e. one server and a 
maximum buffer size of 1000. The buffer isn't actually implemented - just a 
counter that is incremented when an element arrives and decremented when an
element leaves.

All queue logic is implemented by class `MM1K_Queue()` which is initialized in
`main()`.

### `MM1K_Queue()`

Class parameter `K` is the buffer size, `in_scale` and `out_scale` are the 
$\lambda$ parameters of the arrival exponential distribution and departure
exponential distribution respectively.

`_simulate_in()` and `_simulate_out()` are run by two different threads 
concurrently. Every iteration of the unbounded `while` loop, the thread
generates a waiting time (`wait_time`) following an exponential distribution
as discussed above. The thread then sleeps for that amount of time before
updating the queue counter `curr_capacity`.

An additional thread runs `_disp_avg_wait_times()` which displays the average
time between arriving threads, and time between departing threads.

## Results

Running the program for a few minutes shows that the average interval between
arriving elements and the average interval between departing elements
converges to scale factor values `in_scale` and `out_scale`.

