#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application interface classes.
"""
from collections import Iterable
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
        self.img_new = tk.PhotoImage(file=os.path.join(_DIR_IMG, "new.png"))
        self.img_open = tk.PhotoImage(file=os.path.join(_DIR_IMG, "open.png"))
        self.img_save = tk.PhotoImage(file=os.path.join(_DIR_IMG, "save.png"))
        self.img_print = tk.PhotoImage(file=os.path.join(_DIR_IMG, "print.png"))

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
        menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=menu_file, underline=0)
        # File > New
        menu_file.add_command(label="New log book...", command=self.act_new,
                              accelerator="Ctrl+N",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-n>", self.act_new)  # bind hotkey with action
        # File > Open
        menu_file.add_command(label="Open...", command=self.act_open,
                              accelerator="Ctrl+O",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-o>", self.act_open)  # bind hotkey with action
        # File > Save
        menu_file.add_command(label="Save", command=self.act_save,
                              accelerator="Ctrl+S",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-s>", self.act_save)  # bind hotkey with action
        # File > Save As...
        menu_file.add_command(label="Save As...", command=self.act_save_as,
                              accelerator="Shift+Ctrl+S")  # hotkey
        self.bind_all("<Control-S>", self.act_save_as)
        # File > Operations history SUB_MENU
        menu_log = tk.Menu(menu_file, tearoff=0)
        menu_file.add_separator()
        menu_file.add_cascade(label='Operations history',
                              menu=menu_log, underline=11)
        # File > Operations history > Import...
        menu_log.add_command(label="Import...", command=self.import_log,
                             underline=0)           # underline character
        # File > Operations history > Export...
        menu_log.add_command(label="Export...", command=self.export_log,
                             underline=0)           # underline character
        # File > Operations history > Print...
        menu_log.add_command(label="Print...", command=self.print_log,
                             underline=0)           # underline character
        # File > Periodic op. catalogue SUB_MENU
        menu_cat = tk.Menu(menu_file, tearoff=0)
        menu_file.add_cascade(label='Periodic operations catalogue',
                              menu=menu_cat, underline=20)
        # File > Periodic op. catalogue > Import...
        menu_cat.add_command(label="Import...", command=self.import_cat,
                             underline=0)           # underline character
        # File > Periodic op. catalogue > Export...
        menu_cat.add_command(label="Export...", command=self.export_cat,
                             underline=0)           # underline character
        # File > Periodic op. catalogue > Print...
        menu_cat.add_command(label="Print...", command=self.print_cat,
                             underline=0)           # underline character
        # File > Maintenance plan SUB_MENU
        menu_plan = tk.Menu(menu_file, tearoff=0)
        menu_file.add_cascade(label='Maintenance plan',
                              menu=menu_plan, underline=12)
        # File > Maintenance plan > Export...
        menu_plan.add_command(label="Export...", command=self.export_plan,
                             underline=0)           # underline character
        # File > Maintenance plan > Print...
        menu_plan.add_command(label="Print...", command=self.print_plan,
                             underline=0)           # underline character
        # File > Exit
        menu_file.add_separator()
        menu_file.add_command(label="Exit", command=self.act_quit,
                              accelerator="Ctrl+Q",  # hotkey
                              underline=1)           # underline character
        self.bind_all("<Control-q>", self.act_quit)  # bind hotkey with action
        # ToDo: add 5 last files
        # ToDo: edit menu with operations new/edit/delete/clear
        # Help
        menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=menu_help, underline=0)
        menu_help.add_command(label="About", command=self.dlg_help,
                              underline=0)           # underline character

        # Create toolbar
        # --------------
        self.toolbar = tk.Frame(self.master, bd=1, relief=tk.RAISED)
        # New
        self.btn_new = tk.Button(self.toolbar, image=self.img_new,
                                  relief=tk.FLAT,
                                  command=self.act_new)
        self.btn_new.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_new, msg="Create new vehicle log book",
                follow=False, delay=self.tooltip_delay)
        # Open
        self.btn_open = tk.Button(self.toolbar, image=self.img_open,
                                  relief=tk.FLAT,
                                  command=self.act_open)
        self.btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_open, msg="Open another log book",
                follow=False, delay=self.tooltip_delay)
        # Save
        self.btn_save = tk.Button(self.toolbar, image=self.img_save,
                                  relief=tk.FLAT,
                                  command=self.act_open)
        self.btn_save.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_save, msg="Save",
                follow=False, delay=self.tooltip_delay)
        # Print (active tab)
        self.btn_print = tk.Button(self.toolbar, image=self.img_print,
                                  relief=tk.FLAT,
                                  command=self.print_active_tab)
        self.btn_print.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_print, msg="Print active tab content",
                follow=False, delay=self.tooltip_delay)
        # Exit
        self.btn_exit = tk.Button(self.toolbar, image=self.img_exit,
                                  relief=tk.FLAT,
                                  command=self.act_quit)
        self.btn_exit.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_exit, msg="Exit",
                follow=False, delay=self.tooltip_delay)  # Add tooltip
        # Pack toolbar to master frame
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Create tabs
        # -----------
        self.tabs = ttk.Notebook(self.master)
        # 1) Tab Operations Log
        #     adding Frames as pages for the ttk.Notebook
        #     first page, which would get widgets gridded into it
        tab_log = ttk.Frame(self.tabs)
        # ToDo: add toolbar into the tab: add/edit/remove operation/clear + | + import/export/print
        # collapse/expand all buttons,
        # copy/paste/cut
        # ToDo: context menu add/edit/remove/ + cut/copy/paste
        self.table_log = Table(parent=tab_log,
                               headers=["Date","Haul, km", "Operation"],
                               widths=(100, 100, None),
                               stretch=(0, 0, 1))
        iid = self.table_log.insert(("42000", "09.12.2015", "Changing the oil: engine"))
        self.table_log.insert(parent=iid, values=(
            "", "", "Test operation record. "
                    "Here can be placed some additional information: price, "
                    "parts, comments..."))
        # self.table_log.test()
        self.table_log.pack(expand=1, fill="both")
        # self.grid(sticky = (tk.N, tk.S, tk.W, tk.E))
        # self.master.grid_rowconfigure(0, weight = 1)
        # self.master.grid_columnconfigure(0, weight = 1)

        # 2) Tab Periodic Operations Catalogue
        tab_cat = ttk.Frame(self.tabs)
        # ... content example ...
        from tkinter.scrolledtext import ScrolledText
        text = ScrolledText(tab_cat)
        text.pack(expand=1, fill="both")

        # 3) Tab Maintenance plan
        tab_plan = ttk.Frame(self.tabs)
        # Push our tabs to tabs-widget
        self.tabs.add(tab_log, text='Operations history')
        self.tabs.add(tab_cat, text='Periodic operations catalogue')
        self.tabs.add(tab_plan, text='Maintenance plan')
        self.tabs.pack(expand=1, fill="both")

        # Additional elements place here
        # ------------------------------
        # ...
        # ToDo: status bar with tooltips

    def act_new(self, event=None):
        print('new')

    def act_open(self, event=None):
        print('open')

    def act_save(self, event=None):
        print('save')

    def act_save_as(self, event=None):
        print('save_as')

    def import_log(self, event=None):
        print('import_log')

    def import_cat(self, event=None):
        print('import_cat')

    def export_log(self, event=None):
        print('export_log')

    def export_cat(self, event=None):
        print('export_cat')

    def export_plan(self, event=None):
        print('export_plan')

    def print_log(self, event=None):
        print('print_log')

    def print_cat(self, event=None):
        print('print_cat')

    def print_plan(self, event=None):
        print('print_plan')

    def print_active_tab(self, event=None):
        print('print_active_tab')

    def act_quit(self, event=None):
        # sys.exit(0)
        # ToDo: check unsaved
        self.master.quit()

    def dlg_help(self):
        print('Help: link to source page, version, description, author contacts')

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


class Table(object):
    """ Table widget for Tkinter.
    Based on TreeView

    # Examples of unsing:
    # Create table
    >>> table = Table(headers=["Haul", "Date","Operation"],
    ...               widths=(100, 100, None),
    ...               stretch=(0, 0, 1),
    ...               show_tree=True)

    >>> table.pack(expand=1, fill="both")

    # Add item to the table
    >>> iid = table.insert(("42000", "19.10", "Oil change"))

    # Add some subitems (comments)
    >>> iid_sub = table.insert(parent=iid, values=("", "", "Oil change"))

    >>> tk.mainloop()
    """
    def __init__(self, headers,
                 widths=None, stretch=None,  parent=None, show_tree=True,
                 **kwargs):
        """
        :param headers:  columns headers text labels vector
        :param widths:   columns widths in pixels vector.
                         Use None for unspecified width.
        :param stretch:  Is column stretchable? True/False
        :param parent:   master widget for this TreeView-based table
        :param show_tree: show if True (default) column with triangles for
                         expanding items with subitems
        :param kwargs:   other keyword arguments for TreeView base class initialization
        :return:
        """
        super().__init__()
        # tuple of default None values (for unspecified arguments)
        tuple_none = tuple([None] * len(headers))
        # Declare / initialize fields
        self._col_headers = headers
        self._col_names = make_var_name(headers)
        self._col_widths = widths if widths else tuple_none
        self._col_is_stretch = stretch if stretch else tuple_none
        self._show_tree = show_tree
        self.tree = None
        # Create GUI widget and setup columns
        self._setup_widgets(parent)

        # Editable rows:
        # http://stackoverflow.com/questions/18562123/how-to-make-ttk-treeviews-rows-editable
        # Same class example:
        # https://www.daniweb.com/programming/software-development/threads/445871/multiple-treeviews-formatting-in-tkinter

    def _setup_widgets(self, parent=None):
        # Create a treeview
        if self._show_tree:
            self.tree = ttk.Treeview(master=parent)
            self.tree.column("#0", width=20, stretch=tk.NO)
        else:
            self.tree = ttk.Treeview(master=parent, show="headings")
        # Create columns
        self.tree['columns'] = self._col_names
        # Setup column params
        for i in range(0, len(self._col_headers)):
            name = self._col_names[i]
            header = self._col_headers[i]
            width = self._col_widths[i]
            stretch =self._col_is_stretch[i]
            self.tree.heading(name, text=header)
            if width:
                self.tree.column(name, width=width)
            self.tree.column(name, stretch=stretch)

    def pack(self, *args, **kwargs):
        self.tree.pack(*args, **kwargs)

    def insert(self, values, parent="", index="end", item_id=None):
        """ Insert item

        :param parent:  parent is the item ID of the parent item, or the empty
                        string "" to create a new top-level item
        :param index:   index is an integer, or the value "end",
                        specifying where in the list of parent's children to
                        insert the new item. If index is less than or equal to
                        zero, the new node is inserted at the beginning, if
                        index is greater than or equal to the current number of
                        children, it is inserted at the end.
        :param item_id: If iid is specified, it is used as the item identifier,
                        iid must not already exist in the tree.
                        Otherwise, a new unique identifier is generated.
        :param values:  Column values.
                        i.e. ("col1 value", "col2 value")
        :return:        inserted item ID. Equal to item_id, if specified.
                        (can be used to add child for this record)
        """
        # ToDo: make multiline subitems and other ?
        return self.tree.insert(parent,
                                index=index,
                                iid=item_id,
                                values=values)


def make_var_name(label):
    """ Generate correct variable name from text label (or iterable array of labels)

    >>> make_var_name("Test text ji*((i_i")
    'var_testtextjiii'

    >>> make_var_name(['Haul', 'Date', 'Operation'])
    ['var_haul', 'var_date', 'var_operation']
    """
    if isinstance(label, str):
        return "var_" + "".join(c.lower() for c in label if c.isalnum())
    elif isinstance(label, Iterable):
        labels = label
        return [make_var_name(label) for label in labels]


if __name__ == "__main__":
    # table = Table(["Haul", "Date", "Operation"])
    # Run doctests.
    import doctest
    doctest.testmod()