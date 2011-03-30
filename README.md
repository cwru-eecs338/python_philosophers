Dining Philosophers in Python
=============================

Getting the files:
------------------
On the lab computers, use the command:
<pre><code>git clone git://github.com/cwru-eecs338/python_philosophers.git</code></pre>

Running the code:
-----------------
1. Make sure 'dining-philosophers.py' is executable (e.g. <code>chmod 755 producer-philosophers.py</code>), then just execute the script with <code>./producer-philosophers.py</code>
2. You could also invoke the Python interpreter explicitly to run the code using <code>python producer-philosophers.py</code>

Lessons:
--------
* Using threads and monitor-like constructs (<code>RLock</code> and <code>Condition</code>) in Python; see [threading][1] for details
* The <code>with</code> statement in Python makes it easy to define blocks of code with mutual exclusion with respect to some re-entrant lock (RLock)
* The decorator syntax in Python allows defining synchronized functions with respect to some rlock

  [1]: http://docs.python.org/library/threading.html
