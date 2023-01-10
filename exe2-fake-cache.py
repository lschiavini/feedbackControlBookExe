import sys
import math

r = 0.6 # setpoint, reference value
k = float(sys.argv[1]) # gain factor : 50..175

print("r=%f\tk=%f\n" % (r, k)) # t=0
print(r, 0, 0, 0, 0)


def cache(size):
    if(size < 0):
        hit_rate=0
    elif size > 100:
        hit_rate=1
    else:
        hit_rate=size/100.0
    return hit_rate

y, c = 0,0
for _ in range(200):
    e = r - y # tracking error
    c += e # cumulative error
    u = k*c # control action: cache size
    # u = k*e
    y = cache(u) #process output: hit_rate
    
    print(r, e, c, u, y)