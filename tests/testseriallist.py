#!/usr/bin/python3
import serial.tools.list_ports as ls
l = ls.comports()
print([p.device for p in l])