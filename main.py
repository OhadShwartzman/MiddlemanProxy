#!/bin/python3
import MiddleMan
import HTTPSMiddleMan

def main():
    try:
        proxy = MiddleMan.MiddleMan(8080, '0.0.0.0')
        https_proxy = HTTPSMiddleMan.HTTPS_MiddleMan(4443, '0.0.0.0')
        proxy.start()
        https_proxy.start()
        while True:
            pass
    except KeyboardInterrupt:
        proxy.stop_thread()
        https_proxy.stop_thread()
        print("Program ended")

main()