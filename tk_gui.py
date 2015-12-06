#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application interface classes.
"""
import os
from time import time
import tkinter as tk
from tkinter import ttk
# import servint_utils as si_utils

# ToDo: Add context menu to edit tables
# http://zetcode.com/gui/tkinter/menustoolbars/

__author__ = 'Don D.S.'

# Private constants
_DIR_IMG = 'icons'  # images directory


class MainFrame(tk.Frame):
    master_title = "Service Interval"
    tooltip_delay = 0.5

    def __init__(self, master=None, **options):
        tk.Frame.__init__(self, master, **options)

        # Create images
        #   Where I can find icons:
        #   https://www.iconfinder.com/search/?q=exit&price=free
        self.img_exit = tk.PhotoImage(file=os.path.join(_DIR_IMG, "exit.png"))

        # Setup master window
        # -------------------
        self.master.title(self.master_title)
        self.master.minsize(width=640, height=480)
        self._center()

        # Create menu bar
        # ---------------
        self.menu = tk.Menu(self.master)
        self.master.config(menu=self.menu)
        # File
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        # ToDo: + Edit, Help (with link to source page, version, description, author contacts)
        # File > New
        file_menu.add_command(label="New log book...", command=self.act_new,
                              accelerator="Ctrl+N",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-n>", self.act_new)  # bind hotkey with action
        # File > Open
        file_menu.add_command(label="Open...", command=self.act_open,
                              accelerator="Ctrl+O",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-o>", self.act_open)  # bind hotkey with action
        # File > Save
        file_menu.add_command(label="Save", command=self.act_save,
                              accelerator="Ctrl+S",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-s>", self.act_save)  # bind hotkey with action
        # File > Import history...
        file_menu.add_separator()
        file_menu.add_command(label="Import history...", command=self.import_log,
                              underline=0)           # underline character
        # ToDo: make import/export/print as two submenus for log and for cat
        # File > Print...
        # File > Exit
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.act_quit,
                              accelerator="Ctrl+Q",  # hotkey
                              underline=1)           # underline character
        self.bind_all("<Control-q>", self.act_quit)  # bind hotkey with action

        # Create toolbar
        # --------------
        self.toolbar = tk.Frame(self.master, bd=1, relief=tk.RAISED)
        # EXIT
        self.btn_exit = tk.Button(self.toolbar, image=self.img_exit,
                                  relief=tk.FLAT,
                                  command=self.act_quit)
        self.btn_exit.pack(side=tk.LEFT, padx=2, pady=2)
        # Create tooltip
        ToolTip(self.btn_exit, msg="Exit",
                follow=False, delay=self.tooltip_delay)
        # Pack toolbar to mastr frame
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create tabs
        # -----------
        self.tabs = ttk.Notebook(self.master)
        # Tab Operations Log
        #     adding Frames as pages for the ttk.Notebook
        #     first page, which would get widgets gridded into it
        tab_log = ttk.Frame(self.tabs)
        # Tab Periodic Operations Catalogue
        tab_cat = ttk.Frame(self.tabs)
        # ... content example ...
        from tkinter.scrolledtext import ScrolledText
        text = ScrolledText(tab_cat)
        text.pack(expand=1, fill="both")
        # ToDo: Put tables into the tab
        # Push our tabs to tabs-widget
        self.tabs.add(tab_log, text='Operations history')
        self.tabs.add(tab_cat, text='Periodic operations catalogue')
        self.tabs.pack(expand=1, fill="both")

        # Additional elements place here
        # ------------------------------
        # ...

    def act_new(self, event=None):
        print('new')

    def act_open(self, event=None):
        print('open')

    def act_save(self, event=None):
        print('save')

    def import_log(self, event=None):
        print('import_log')

    def export_log(self, event=None):
        print('export_log')

    def import_cat(self, event=None):
        print('import_cat')

    def export_cat(self, event=None):
        print('export_cat')

    def print_log(self, event=None):
        print('print_log')

    def print_cat(self, event=None):
        print('print_cat')

    def act_quit(self, event=None):
        # sys.exit(0)
        self.master.quit()



    def _center(self):
        # Center window at the screen
        self.update_idletasks()
        # w = self.master.winfo_width()  # width for the Tk root
        # h = self.master.winfo_height()     # height for the Tk root
        #
        # # get screen width and height
        # ws = self.winfo_screenwidth()   # width of the screen
        # hs = self.winfo_screenheight()  # height of the screen
        #
        # # calculate x and y coordinates for the Tk root window
        # x = (ws/2) - (w/2)
        # y = (hs/2) - (h/2)
        #
        # # set the dimensions of the screen
        # # and where it is placed
        # self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))


class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor

    Source:
    http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
    Created by Tucker Beck on Wed, 11 Mar 2009 (MIT)

    Edited by Don D.S.
    """
    def __init__(self, wdgt, msg=None, msgFunc=None, delay=1.0, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set( msg )
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The test of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                   aspect=1000).grid()
        # Add bindings to the widget.  This will NOT override bindings that the
        # widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.

        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the widget will make the
        # ToolTip dissapear
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+10, event.y_root+10))
        try:
            # Try to call the message function.  Will not change the message if
            # the message function is None or the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget

        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()