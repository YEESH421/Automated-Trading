from concurrent.futures import ThreadPoolExecutor, as_completed
from sandbox import *
from trade import *

c = authenticate()
def function(param):
    return "function result for param: %s" % param

with ThreadPoolExecutor(max_workers=2) as executor:
    future1 = executor.submit(a, c)
    future2 = executor.submit(b, c)

print(future1.result())
print(future2.result())