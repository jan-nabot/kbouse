from Xlib import display, X
from Xlib.ext import record
from Xlib.protocol import rq
from Xlib.ext.xtest import fake_input
import threading
availableevents = (50,62,90,111,113,114,116) 
class Listener(threading.Thread):
    def __init__(self, passto):
        self.passto = passto
        self.dLi = display.Display()
        contex = self.dLi.record_create_context(0,[record.AllClients],[{'core_requests': (0,0), 'core_replies' : (0,0), 'ext_requests' : (0,0,0,0), 'ext_replies' : (0,0,0,0), 'delivered_events' : (0,0), 'device_events': (X.KeyPress, X.KeyRelease, X.MotionNotify), 'errors': (0,0), 'client_started': False, 'client_died':False}]) 
        self.dLi.record_enable_context(contex, self.handlingfunc)
    def cleanup(self):
        self.dLi.record_free_context(contex)
    def run(self):
        while 1:
            return self.dLi.next_event()
    def handlingfunc(self, ur):
        idk = ur.data
        while len(idk):
            aa, bb = rq.EventField(None).parse_binary_value(idk, self.dLi.display, None, None)
            if aa.type in (2,3) and aa.detail in availableevents:
                return self.passto(aa.type, aa.detail) 
            else:
                return

# class Doer(threading.Thread):
class Doer():
    def __init__(self):
        self.dDo = display.Display()
        self.dist = 15
        self.shift = 0
        self.up = 0
        self.down = 0
        self.left = 0
        self.right = 0
                
    def getmousepos(self):
        xy = self.dDo.screen().root.query_pointer()._data
        x = xy['win_x']
        y = xy['win_y']
        return x, y

    def moveit(self, x, y):
        fake_input(self.dDo, X.MotionNotify, x=x, y=y)
        self.dDo.sync()

    def clickit(self, button = 1):
        fake_input(self.dDo, X.ButtonPress, [None, 1,3,2,4,5][button])
        fake_input(self.dDo, X.ButtonRelease, [None, 1, 3, 2, 4, 5][button])
        self.dDo.sync()

    def interact1(self, in0, in1):
        if in0 == 3:
            if in1 in (50,62):
                self.dist = 15
            elif in1 == 111:
                self.up = 0
            elif in1 == 116:
                self.down = 0
            elif in1 == 113:
                self.left = 0
            elif in1 == 114:
                self.right = 0
        
        elif in0 == 2:
            if in1 in (50,62):
                self.dist == 200
                return
            elif in1 in (90,):
                # return
                self.clickit()
            
            x, y = self.getmousepos()
        
            if in1 == 111:
                self.up = 1
                if self.left == 1:
                    self.moveit(x-self.dist, y-self.dist)
                elif self.right == 1:
                    self.moveit(x+self.dist, y-self.dist)
                else:
                    self.moveit(x, y-self.dist)
            
            if in1 == 116:
                self.down = 1
                if self.left == 1:
                    self.moveit(x-self.dist, y+self.dist)
                elif self.right == 1:
                    self.moveit(x+self.dist, y+self.dist)
                else:
                    self.moveit(x, y+self.dist)

            if in1 == 113:
                self.left = 1
                if self.up == 1:
                    self.moveit(x-self.dist, y-self.dist)
                elif self.down == 1:
                    self.moveit(x-self.dist, y+self.dist)
                else:
                    self.moveit(x-self.dist, y)

            if in1 == 114:
                self.right = 1
                if self.up == 1:
                    self.moveit(x+self.dist, y-self.dist)
                elif self.down == 1:
                    self.moveit(x+self.dist, y+self.dist)
                else:
                    self.moveit(x+self.dist, y)

            else:
                pass

ra = Doer()
ma = ra.interact1
Listener(ma).start()
