#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application interface classes.
"""
from collections import Iterable
from datetime import date, datetime
import os
from time import time
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import tkinter.filedialog
import servint_utils as siu

# ToDo: Add context menu to edit tables
# http://zetcode.com/gui/tkinter/menustoolbars/

__author__ = 'Don D.S.'

# Private constants
_DIR_IMG = 'icons'  # images directory

# Test data
oil_change = siu.Operation("Changing the oil: engine",
                           interval_km=10000,
                           interval_year=1)
# Create done-operation copy from current operation type.
oil_changed = oil_change.done(km=98421,
                              date=date(2015, 12, 5),
                              comment="Price: 4000 RUR")


class MainFrame(tk.Frame):
    master_title = "Service Interval"
    tooltip_delay = 0.5

    def __init__(self, master=None, **options):
        tk.Frame.__init__(self, master, **options)

        # Initialize document
        self._doc = None  # Create class field
        self.log_new()    # Initialize field

        # Create images
        #   Where I can find icons:
        #   https://www.iconfinder.com/search/?q=exit&price=free
        self.img_exit = tk.PhotoImage(file=os.path.join(_DIR_IMG, "exit.png"))
        self.img_new = tk.PhotoImage(file=os.path.join(_DIR_IMG, "new.png"))
        self.img_open = tk.PhotoImage(file=os.path.join(_DIR_IMG, "open.png"))
        self.img_save = tk.PhotoImage(file=os.path.join(_DIR_IMG, "save.png"))
        self.img_print = tk.PhotoImage(file=os.path.join(_DIR_IMG, "print.png"))
        self.img_add = tk.PhotoImage(file=os.path.join(_DIR_IMG, "add.png"))
        self.img_edit = tk.PhotoImage(file=os.path.join(_DIR_IMG, "edit.png"))
        self.img_delete = tk.PhotoImage(
            file=os.path.join(_DIR_IMG, "delete.png"))
        self.img_vehicle = tk.PhotoImage(
            file=os.path.join(_DIR_IMG, "vehicle.png"))

        # Setup master window
        # -------------------
        self.update_title()
        self.master.minsize(width=640, height=480)
        self._center()

        # Create menu bar
        # ---------------
        self.menu = tk.Menu(self.master, relief=tk.GROOVE)
        self.master.config(menu=self.menu)
        # File
        menu_file = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=menu_file, underline=0)
        # File > New
        menu_file.add_command(label="New log book...", command=self.log_new,
                              accelerator="Ctrl+N",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-n>", self.log_new)  # bind hotkey with action
        # File > Open
        menu_file.add_command(label="Open...", command=self.log_open,
                              accelerator="Ctrl+O",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-o>", self.log_open)  # bind hotkey with action
        # File > Save
        menu_file.add_command(label="Save", command=self.log_save,
                              accelerator="Ctrl+S",  # hotkey
                              underline=0)           # underline character
        self.bind_all("<Control-s>", self.log_save)  # bind hotkey with action
        # File > Save As...
        menu_file.add_command(label="Save As...", command=self.log_save_as,
                              accelerator="Shift+Ctrl+S")  # hotkey
        self.bind_all("<Control-S>", self.log_save_as)
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
        menu_file.add_command(label="Exit", command=self.quit,
                              accelerator="Ctrl+Q",  # hotkey
                              underline=1)           # underline character
        self.bind_all("<Control-q>", self.quit)  # bind hotkey with action
        # ToDo: add 5 last files
        # Edit
        menu_edit = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=menu_edit, underline=0)
        # Edit > Add operation
        menu_edit.add_command(label="Add operation",
                              command=self.operation_add,
                              underline=0)
        # Edit > Edit operation
        menu_edit.add_command(label="Edit selected operation",
                              command=self.operation_edit,
                              underline=0)
        # Edit > Delete operation
        menu_edit.add_command(label="Delete selected operation",
                              command=self.operation_delete,
                              underline=0)
        # Edit > Edit vehicle properties
        menu_edit.add_separator()
        menu_edit.add_command(label="Edit vehicle properties",
                              command=self.vehicle_setup,
                              underline=5)
        # Help
        menu_help = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=menu_help, underline=0)
        menu_help.add_command(label="About", command=self.dlg_help,
                              underline=0)           # underline character

        # Create toolbar
        # --------------
        self.toolbar = tk.Frame(self.master, bd=1, relief=tk.GROOVE)
        # New
        self.btn_new = tk.Button(self.toolbar, image=self.img_new,
                                  relief=tk.FLAT,
                                  command=self.log_new)
        self.btn_new.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_new, msg="Create new vehicle log book",
                follow=False, delay=self.tooltip_delay)
        # Open
        self.btn_open = tk.Button(self.toolbar, image=self.img_open,
                                  relief=tk.FLAT,
                                  command=self.log_open)
        self.btn_open.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_open, msg="Open another log book",
                follow=False, delay=self.tooltip_delay)
        # Save
        self.btn_save = tk.Button(self.toolbar, image=self.img_save,
                                  relief=tk.FLAT,
                                  command=self.log_save)
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
        # Separator 1
        sep = ttk.Separator(self.toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        # Vehicle properties
        self.btn_vehicle = tk.Button(self.toolbar, image=self.img_vehicle,
                                  relief=tk.FLAT,
                                  command=self.vehicle_setup)
        self.btn_vehicle.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_vehicle, msg="Edit vehicle properties",
                follow=False, delay=self.tooltip_delay)
        # Separator 2
        sep = ttk.Separator(self.toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        # Add operation
        self.btn_add = tk.Button(self.toolbar, image=self.img_add,
                                  relief=tk.FLAT,
                                  command=self.operation_add)
        self.btn_add.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_add, msg="Add new operation",
                follow=False, delay=self.tooltip_delay)
        # Edit operation
        self.btn_edit = tk.Button(self.toolbar, image=self.img_edit,
                                  relief=tk.FLAT,
                                  command=self.operation_edit)
        self.btn_edit.pack(side=tk.LEFT, padx=2, pady=2)
        ToolTip(self.btn_edit, msg="Edit selected operation",
                follow=False, delay=self.tooltip_delay)
        # Delete operation
        self.btn_delete = tk.Button(self.toolbar, image=self.img_delete,
                                  relief=tk.FLAT,
                                  command=self.operation_delete)
        ToolTip(self.btn_delete, msg="Delete selected operation",
                follow=False, delay=self.tooltip_delay)
        self.btn_delete.pack(side=tk.LEFT, padx=2, pady=2)
        # Separator 3
        sep = ttk.Separator(self.toolbar, orient=tk.VERTICAL)
        sep.pack(side=tk.LEFT, padx=2, pady=2, fill="both")
        # Exit
        self.btn_exit = tk.Button(self.toolbar, image=self.img_exit,
                                  relief=tk.FLAT,
                                  command=self.quit)
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
        # ... content
        self.table_log = OperationsTable(parent=tab_log)
        self.table_log.pack(expand=1, fill="both")
        # TEST DATA
        for i in range(10):
            oil_changed.done_at_km = i
            self.table_log.insert(oil_changed)
        # 2) Tab Periodic Operations Catalogue
        tab_cat = ttk.Frame(self.tabs)
        # ... content
        self.table_cat = PeriodicOperationsTable(parent=tab_cat)
        self.table_cat.pack(expand=1, fill="both")
        # TEST DATA
        self.table_cat.insert(oil_change)
        # 3) Tab Maintenance plan
        tab_plan = ttk.Frame(self.tabs)
        # ... content
        self.table_plan = MaintenancePlanTable(parent=tab_plan)
        self.table_plan.pack(expand=1, fill="both")
        # Push our tabs to tabs-widget
        self.tabs.add(tab_log, text='Operations history')
        self.tabs.add(tab_cat, text='Periodic operations catalogue')
        self.tabs.add(tab_plan, text='Maintenance plan')
        self.tabs.pack(expand=1, fill="both")

        # Additional elements place here
        # ------------------------------
        # ...
        # ToDo: status bar with tooltips

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, new_doc):
        print('Tables must be cleared!')
        self._doc = new_doc
        self.update_title()

    def update_title(self):
        # Update main window title
        status = "*" if self.doc.is_modified else ""
        self.master.title(status + self.doc.label + " - " + self.master_title)

    def ask_save(self):
        """ Ask user to save if document modified
        :return:  False if user select CANCEL, else True.
        """
        if self.doc.is_modified:
            ans = tk.messagebox.askquestion(
                parent=self.master,
                title="Question",
                message=self.doc.label,
                detail="Data has been changed. Do you want to save changes?",
                icon="question",
                type="yesnocancel")
            if ans == "yes":
                self.log_save()
            elif ans == "cancel":
                return False
        return True

    def log_new(self, event=None):
        if self.doc:
            # Creating new instead old
            not_cancelled = self.ask_save()
        else:
            # Creating at first time
            not_cancelled = True  # anyway
        if not_cancelled:
            self.doc = TkVehicleLogBook(label="Unknown Vehicle",
                                        production_date=date.today())

    def log_open(self, event=None):
        not_cancelled = self.ask_save()
        if not_cancelled:
            filename = tk.filedialog.askopenfilename(
                parent=self.master,
                title="Open vehicle log book",
                defaultextension=self.doc.extension,
                filetypes=((self.master_title + " files",
                            "*" + self.doc.extension),),
                initialfile=self.doc.label,
                initialdir=self.doc.filename)
            if not filename:
                return
            try:
                self.doc = self.doc.load(filename)
                self.file = filename
            except OSError as err:
                tk.messagebox.showerror(
                    parent=self.master,
                    title="Error",
                    message="Error occurred while opening file\n" + filename,
                    detail=err)

    def log_save(self, event=None):
        if self.doc.filename:
            self.doc.save()
        else:
            self.log_save_as()

    def log_save_as(self, event=None):
        filename = tk.filedialog.asksaveasfilename(
            parent=self.master,
            title="Save vehicle log book as",
            defaultextension=self.doc.extension,
            filetypes=((self.master_title + " files",
                        "*" + self.doc.extension),
                       ("All files", "*.*")),
            initialfile=self.doc.label,
            initialdir=self.doc.filename)
        if not filename:
            return
        self.doc.save(filename)

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

    def quit(self, event=None):
        not_cancelled = self.ask_save()
        if not_cancelled:
            self.master.quit()

    def vehicle_setup(self, event=None):
        # Don't forget to update self.master.title()
        # after changing vehicle properties
        VehicleSetupWindow(master=self, vehicle=self.doc)
        self.update_title()
        print('vehicle_setup')

    def operation_add(self, event=None):
        AddOperationWindow(master=self, vehicle=self.doc)
        print('operation_add')

    def operation_edit(self, event=None):
        print('operation_edit')

    def operation_delete(self, event=None):
        print('operation_delete')

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


class VehicleSetupWindow(tk.Toplevel):
    # Modal window for vehicle properties setup

    def __init__(self, vehicle, master=None, **options):

        self.vehicle = vehicle

        # Initialize window
        # -----------------
        super().__init__(master, **options)
        self.title("Vehicle properties")
        self.minsize(width=500, height=150)
        self.resizable(width=tk.FALSE, height=tk.FALSE)

        # Add widgets
        # -----------
        # Container 1
        # -----------
        frame = tk.Frame(master=self, bd=10)
        frame.pack(fill=tk.X)
        # Label "Enter vehicle label:"
        lbl_vehicle = tk.Label(master=frame,
                               text="Enter vehicle label:",
                               anchor=tk.W, justify=tk.LEFT)
        lbl_vehicle.pack(side=tk.TOP, fill=tk.X)
        # Entry Vehicle Label
        self.txt_label = tk.Entry(master=frame)
        self.txt_label.insert(0, self.vehicle.label)
        self.txt_label.pack(side=tk.TOP, fill=tk.X)

        # Container 2
        # -----------
        frame = tk.Frame(master=self, bd=10)
        frame.pack(fill=tk.X)
        # Label "Enter vehicle production date (YYYY-MM-DD):"
        lbl_prod = tk.Label(master=frame,
                            text="Enter vehicle production date (YYYY-MM-DD or YYYY.MM.DD):",
                            anchor=tk.W, justify=tk.LEFT)
        lbl_prod.pack(side=tk.TOP, fill=tk.X)
        # Entry Vehicle production date
        vcmd = (self.register(self.prod_date_validate),
                '%i', '%P', '%S')
        # valid percent substitutions (from the Tk entry man page)
        # %d = Type of action (1=insert, 0=delete, -1 for others)
        # %i = index of char string to be inserted/deleted, or -1
        # %P = value of the entry if the edit is allowed
        # %s = value of entry prior to editing
        # %S = the text string being inserted or deleted, if any
        # %v = the type of validation that is currently set
        # %V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # %W = the tk name of the widget
        self.txt_date = tk.Entry(master=frame,
                                 validate="key", validatecommand=vcmd)
        self.txt_date.insert(0, self.vehicle.production_date)
        self.txt_date.pack(side=tk.TOP, fill=tk.X)
        # ToDo: Add calendar widget

        # Container 2
        # -----------
        frame = tk.Frame(master=self, bd=10)
        frame.pack(side=tk.BOTTOM)
        # Button OK
        btn_ok = tk.Button(master=frame,
                           text="Ok",
                           command=self.btn_ok,
                           height=1, width=10)
        btn_ok.pack(side=tk.LEFT)
        self.bind("<Return>", self.btn_ok)

        # Button Cancel
        btn_cancel = tk.Button(master=frame,
                               text="Cancel",
                               command=self.destroy,
                               height=1, width=10)
        self.bind("<Escape>", lambda event: self.destroy())
        btn_cancel.pack(side=tk.RIGHT)

        # Make modal
        self.focus_force()
        self.grab_set()
        self.transient(self.master)
        self.master.wait_window(self)

    def prod_date_validate(self, insert_index, new_value, insert_char):
        # Return True if new_value is valid
        # Allowed symbols for differenet position indexes.
        allowed = ('12', '0123456789', '0123456789', '0123456789',
                   r'-.',
                   '01','0123456789',
                   r'-.',
                   '0123',
                   '0123456789')
        # Check.
        insert_index = int(insert_index)
        if not (0 <= insert_index < len(allowed)):
            return False
        if len(insert_char) == 1 and \
                        insert_char not in allowed[insert_index]:
            return False
        elif len(insert_char) == len(allowed):
            try:
                insert_char = new_value.replace('.', '-')
                datetime.strptime(insert_char, '%Y-%m-%d').date()
            except ValueError:
                return False
        return True


    def btn_ok(self, event=None):
        new_date = self.txt_date.get()
        new_label = self.txt_label.get()
        try:
            new_date = new_date.replace('.', '-')
            new_date = datetime.strptime(new_date, '%Y-%m-%d').date()
        except ValueError:
            tk.messagebox.showerror(parent=self,
                                    title="Error",
                                    message="Wrong date format",
                                    detail=
                                    "It must be YYYY-MM-DD or YYYY.MM.DD.\n"
                                    "I.e. 1984-01-23, not " +  new_date)
        else:
            self.vehicle.label = new_label
            self.vehicle.production_date = new_date
            self.destroy()


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
                 widths=None, stretch=None,  parent=None, show_tree=True):
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
            stretch = self._col_is_stretch[i]
            self.tree.heading(name, text=header)
            if width:
                self.tree.column(name, width=width)
            self.tree.column(name, stretch=stretch)
        # Add vertical scrollbar
        vsbar = tk.Scrollbar(self.tree)
        vsbar.config(command=self.tree.yview)
        self.tree.config(yscrollcommand=vsbar.set)
        vsbar.pack(side=tk.RIGHT, fill=tk.Y)

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


class OperationsTable(Table):
    """ Operations table widget.
    """
    def __init__(self, parent):
        super().__init__(headers=["Date", "Haul, km", "Operation"],
                         parent=parent,
                         widths=(100, 100, None),
                         stretch=(0, 0, 1),
                         show_tree=True)

    def insert(self, operation):
        # Check type
        if not isinstance(operation, siu.Operation):
            raise TypeError(
                "Argument must have <class 'Operation'>, not " +
                str(type(operation)))
        # Check state
        if not siu.Operation.is_done:
            raise ValueError("Operation must be done for this widget."
                             "Use Operation.done() method before.")
        item = (operation.done_at_date, operation.done_at_km, operation.label)
        iid = super().insert(item)
        super().insert(parent=iid, values=("", "", operation.comment))


class PeriodicOperationsTable(Table):
    """ Periodic operations table widget.
    """
    def __init__(self, parent):
        super().__init__(headers=["Interval, year", "Interval, km", "Operation"],
                         parent=parent,
                         widths=(100, 100, None),
                         stretch=(0, 0, 1),
                         show_tree=False)

    def insert(self, operation):
        # Check type
        if not isinstance(operation, siu.Operation):
            raise TypeError(
                "Argument must have <class 'Operation'>, not " +
                str(type(operation)))
        # Check state
        if not siu.Operation.is_periodic:
            raise ValueError("Operation must be periodic this widget.")
        interval_time = round(operation.interval_time.days/365, 1)
        item = (interval_time, operation.interval_km, operation.label)
        iid = super().insert(item)
        super().insert(parent=iid, values=("", "", operation.comment))


class MaintenancePlanTable(Table):
    """ Maintenance plan widget
    """
    def __init__(self, parent):
        super().__init__(headers=["Date", "Haul, km", "Operation"],
                         parent=parent,
                         widths=(100, 100, None),
                         stretch=(0, 0, 1),
                         show_tree=False)

    def insert(self, operation):
        # Check type
        if not isinstance(operation, str) and isinstance(operation, Iterable):
            for op in operation:
                self.insert(op)
                return
        elif not isinstance(operation, siu.Operation):
            raise TypeError(
                "Argument must have <class 'Operation'>, not " +
                str(type(operation)))
        # Check state
        if not siu.Operation.is_done:
            raise ValueError("Operation must be done for this widget."
                             "Use Operation.done() method before.")
        item = (operation.done_at_date, operation.done_at_km, operation.label)
        iid = super().insert(item)
        super().insert(parent=iid, values=("", "", operation.comment))

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


class AddOperationWindow(tk.Toplevel):
    """  Modal window for adding operation

    """
    def __init__(self, master=None, vehicle=None, **options):
        self.vehicle = vehicle

        # Initialize window
        # -----------------
        super().__init__(master, **options)
        self.title("Add operation")
        self.minsize(width=500, height=400)
        self.resizable(width=tk.FALSE, height=tk.FALSE)

        # Add widgets
        # -----------
        # ...

        # Make modal
        self.focus_force()
        self.grab_set()
        self.transient(self.master)
        self.master.wait_window(self)


class TkVehicleLogBook(siu.VehicleLogBook):
    """ Represents storage of service operations for vehicle
    Subclass that can be linked with tkinter widgets
    """
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
    # ToDo: implement linkage with tables


if __name__ == "__main__":
    # table = Table(["Haul", "Date", "Operation"])
    # Run doctests.
    import doctest
    doctest.testmod()