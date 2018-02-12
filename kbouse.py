#!/usr/bin/env python3
'''
    Move mouse with arrow buttons
    optionally combined with ctrl to
    avoid effects such us browser 
    scrolling, and shift to make cursor
    jump further to speed up usage.
    only Left Mouse button click is
    supported under numpad 0

    requires: linux, X, python-xlib, pymouse
    written in: python3.5
    by: jan-nabot
'''
from pymouse import PyMouse
from Xlib import display, X
from Xlib.ext import record
from Xlib.protocol import rq

def main():
    pym = PyMouse()
    ld = display.Display()
    dist = 15
    ctx = ld.record_create_context(0,[record.AllClients],[{'core_requests': (0,0), 'core_replies' : (0,0), 'ext_requests' : (0,0,0,0), 'ext_replies' : (0,0,0,0), 'delivered_events' : (0,0), 'device_events': (X.KeyPress, X.KeyRelease), 'errors': (0,0), 'client_started': False, 'client_died':False}]) 
    shift, up, down, left, right = (0,0,0,0,0)
    # ld.change_pointer_control((0x4fff,0x7fff),0)

    def handlerr(reply): 
        nonlocal shift, dist, up, down, left, right
        dat = reply.data
        if dat:
            ev, dat = rq.EventField(None).parse_binary_value(dat, ld.display, None, None)
            print(ev)
            if ev.detail in (50,62):
                if ev.type == 2:
                    dist = 200 # quicker cursor movement while ALT is pressed
                elif ev.type == 3:
                    dist = 15 
            if ev.detail in (111,113,114,116):
                if ev.detail == 111: 
                    if ev.type == 2:
                        up = 1
                        x,y = pym.position()
                        if left == 0 and right == 0:
                            pym.move(x,y-dist)
                        elif left == 1:
                            pym.move(x-dist,y-dist)
                        elif right == 1:
                            pym.move(x+dist,y-dist)
                    elif ev.type == 3:
                        up = 0
                
                elif ev.detail == 116: 
                    if ev.type == 2:
                        down = 1
                        x,y = pym.position()
                        if left == 0 and right == 0:
                            pym.move(x,y+dist)
                        elif left == 1: 
                            pym.move(x-dist,y+dist)
                        elif right == 1:
                            # print('k')
                            pym.move(x+dist,y+dist)
                    elif ev.type == 3:
                        down = 0

                elif ev.detail == 113: 
                    if ev.type == 2:
                        left = 1
                        x,y = pym.position()
                        if up == 0 and down == 0:
                            pym.move(x-dist,y)
                        elif up == 1: 
                            pym.move(x-dist,y-dist)
                        elif down == 1:
                            pym.move(x-dist,y+dist)
                    elif ev.type == 3:
                        left = 0

                elif ev.detail == 114: 
                    if ev.type == 2:
                        right = 1
                        x,y = pym.position()
                        if up == 0 and down == 0:
                            pym.move(x+dist,y)
                        elif up == 1: 
                            pym.move(x+dist,y-dist)
                        elif down == 1: 
                            pym.move(x+dist,y+dist)
                    elif ev.type == 3:
                        right = 0
            if ev.detail in (90,):
                pym.click(*pym.position())

    def loop():
        while 1:
            return ld.next_event()

    ld.record_enable_context(ctx, handlerr)
    loop()
    ld.record_free_context(ctx)

main()
