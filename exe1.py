import matplotlib.pyplot as plt
import random

class Buffer:
    def __init__(self, max_wip, max_flow):
        self.queued = 0
        self.wip = 0 # work-in-progress ("ready pool")
        
        self.max_wip = max_wip # number of items is limited
        self.max_flow = max_flow #avg outflow is max_flow/2
        
    def work(self, unit):
        # Add to ready pool
        unit = max(0, int(round(unit)))
        unit = min(unit, self.max_wip)
        self.wip += unit
        
        # Transfer from ready pool to queue
        r = int(round(random.uniform(0, self.wip)))
        self.wip -= r
        self.queued += r
        
        # Release from queue to downstream process
        r = int(round(random.uniform(0, self.max_flow)))
        r = min(r, self.queued)
        self.queued -= r
        return self.queued
    
class Controller: 
    def __init__(self, kp, ki):
        self.kp, self.ki = kp, ki
        self.i = 0 # Cumulative error of integral
        
    def work(self, e):
        self.i += e
        return self.kp*e + self.ki *self.i
    
def open_loop(process, tm=5000):
    x_axis = []
    target_y_axis = []
    output_y_axis = []

    def target(t):
        return 5.0 # 5.1
    
    for t in range(tm):
        u = target(t)
        y = process.work(u)
        # print (t, u, 0, u, y)
        target_y_axis.append(u)
        output_y_axis.append(y)
        x_axis.append(t)


    plt.plot(x_axis, target_y_axis, label = "target")
    plt.plot(x_axis, output_y_axis, label = "output")
    plt.show()
    
def closed_loop(controller, process, tm=5000):
    units_y_axis = []
    target_y_axis = []
    errors_y_axis = []
    output_y_axis = []
    x_axis = []
    def setpoint(t):
        if t < 100: return 0
        if t < 300 : return 50
        return 10
    
    y = 0
    for t in range (tm):
        r = setpoint(t)
        e = r - y
        u = controller.work(e)
        y = process.work(u)

        # print(t, r, e, u, y)
        target_y_axis.append(r)
        units_y_axis.append(u)
        errors_y_axis.append(e)
        output_y_axis.append(y)
        x_axis.append(t)
    
    # plt.plot(x_axis, units_y_axis, label = "units - controller output", linestyle=":")
    # plt.plot(x_axis, units_y_axis, label = "units - controller output", linestyle=":")
    # plt.plot(x_axis, errors_y_axis, label = "errors")
    plt.plot(x_axis, output_y_axis, label = "output")
    plt.plot(x_axis, target_y_axis, label = "target")
    plt.legend()
    plt.show()
    
    
    
c = Controller(kp = 1, ki = 0.01)                
p = Buffer(max_wip = 50, max_flow = 100)

# open_loop(p, 3000)

closed_loop(c, p, 3000)

c = Controller(kp = 2, ki = 0.01)     

closed_loop(c, p, 3000)