#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
GUI classes
"""
import tkinter as tk
# import servint_utils as si_utils


__author__ = 'Don D.S.'


class MainFrame(tk.Frame):
    def __init__(self, parent=None, **options):
        tk.Frame.__init__(self, parent, **options)
        self.label = tk.Label(text="Hello, world")
        self.label.pack(padx=10, pady=10)