import argparse
import math

import re
import threading
import sys

from pythonosc import dispatcher
from pythonosc import osc_server

import config
import learn

import osc

MODE = input("mode > ")
stream = input("is stream > ")
file_type = input("3 input sensors or 4 > ")
config.interval = input("inverval > ")
ver = input("version > ")

def keys():
    while True:
        print("input mode")
        input_word = input(">")
        if input_word == "s":
            sys.exit()
        elif input_word == "o":
            config.is_calibration = True
        elif config.c != input_word:
            config.c = input_word
            print("c =", config.c)
        else:
            print("else")

def osc_loop():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
      default="localhost", help="The ip to listen on")
    parser.add_argument("--port",
      type=int, default=8082, help="The port to listen on")
    args = parser.parse_args()

    learner = learn.Arrange()
    learner.make_dir_train_or_test()

    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.map("/found", osc.set_found)
    _dispatcher.map("/raw", learner.fetch_numbers)

    server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), _dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


if stream == "s":
    th = threading.Thread(target=osc_loop,name="th",args=())
    th.setDaemon(True)
    th.start()

if __name__ == "__main__":
    keys()
