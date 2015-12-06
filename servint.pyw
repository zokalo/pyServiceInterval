#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Main script.
"""
__author__ = 'Don D.S.'

import tkinter as tk
from tk_gui import MainFrame

if __name__ == "__main__":
    root = tk.Tk()
    app = MainFrame(master=root)
    app.pack()
    root.mainloop()
