# SchwiCV

## Installation

You can install the SchwiCV Tools from [PyPI](https://pypi.org/project/schwicv/):

    pip install schwicv

The package is supported on Python 3.6 and above.

# How to use
## Timer Lib
    from schwicv import Timer
    
    tmr = Timer(100) # Makes Instance of Timer class with 100ms init time
    tmr.remaining_time_ms   # Output of remaining time, 0 if over
    tmr.execution_time_ms   # Output of execution time from last start
    tmr.remaining_percent   # Output of remaining time in percent
    tmr.time_over           # True if code needed more or equal 100 ms

    tmr.start_ms(1000)      # Restart timer with 1000ms init time, if re-use instance 
