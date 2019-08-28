#!/bin/python3
import MiddleMan
import socket

def main():
    try:
        proxy = MiddleMan.MiddleMan(8080, '0.0.0.0')
        proxy.start()
        while True:
            pass
    except KeyboardInterrupt:
        proxy.stop_thread()
        proxy.join()
        print("Program ended")

main()