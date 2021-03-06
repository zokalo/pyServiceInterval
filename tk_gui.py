#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application interface classes.
"""
from collections import Iterable
from datetime import date, datetime, timedelta
from numbers import Number
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
    extension_imp_exp = ".txt"
    extensions_imp_exp = [("Text files", ".txt"),
                          ("All files", ".*")]

    def __init__(self, master=None, **options):
        super().__init__(master, **options)

        self.filetypes = [(self.master_title + " files",
                           siu.VehicleLogBook.get_extension()),
                          ("All files", ".*")]

        # Create images
        #   Where I can find icons:
        #   https://www.iconfinder.com/search/?q=exit&price=free
        self.img_exit = tk.PhotoImage(file=os.path.join(_DIR_IMG, "exit.png"))
        self.img_new = tk.PhotoImage(file=os.path.join(_DIR_IMG, "new.png"))
        self.img_open = tk.PhotoImage(file=os.path.join(_DIR_IMG, "open.png"))
        self.img_save = tk.PhotoImage(file=os.path.join(_DIR_IMG, "save.png"))
        # self.img_print = tk.PhotoImage(file=os.path.join(_DIR_IMG, "print.png"))
        self.img_add = tk.PhotoImage(file=os.path.join(_DIR_IMG, "add.png"))
        self.img_edit = tk.PhotoImage(file=os.path.join(_DIR_IMG, "edit.png"))
        self.img_delete = tk.PhotoImage(
            file=os.path.join(_DIR_IMG, "delete.png"))
        self.img_vehicle = tk.PhotoImage(
            file=os.path.join(_DIR_IMG, "vehicle.png"))

        # Setup master window
        # -------------------
        self.master.minsize(width=640, height=480)
        self._center()
        self.bind("<<refresh>>", self.update_title)
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

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
        # # File > Operations history > Print...
        # menu_log.add_command(label="Print...", command=self.print_log,
        #                      underline=0)           # underline character
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
        # # File > Periodic op. catalogue > Print...
        # menu_cat.add_command(label="Print...", command=self.print_cat,
        #                      underline=0)           # underline character
        # File > Maintenance plan SUB_MENU
        menu_plan = tk.Menu(menu_file, tearoff=0)
        menu_file.add_cascade(label='Maintenance plan',
                              menu=menu_plan, underline=12)
        # File > Maintenance plan > Export...
        menu_plan.add_command(label="Export...", command=self.export_plan,
                             underline=0)           # underline character
        # # File > Maintenance plan > Print...
        # menu_plan.add_command(label="Print...", command=self.print_plan,
        #                      underline=0)           # underline character
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
        # # Print (active tab)
        # self.btn_print = tk.Button(self.toolbar, image=self.img_print,
        #                           relief=tk.FLAT,
        #                           command=self.print_active_tab)
        # self.btn_print.pack(side=tk.LEFT, padx=2, pady=2)
        # ToolTip(self.btn_print, msg="Print active tab content",
        #         follow=False, delay=self.tooltip_delay)
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
        self.tabs = TabPanel(self.master)
        # 1) Tab Operations Log
        #     adding Frames as pages for the ttk.Notebook
        #     first page, which would get widgets gridded into it
        self.tab_log = ttk.Frame(self.tabs)
        # collapse/expand all buttons,
        # copy/paste/cut
        # ToDo: context menu add/edit/remove/ + cut/copy/paste
        # ... content
        self.table_log = OperationsTable(parent=self.tab_log)
        self.table_log.pack(expand=1, fill="both")
        self.table_log.bind("<Double-1>", self.operation_edit)
        # 2) Tab Periodic Operations Catalogue
        self.tab_cat = ttk.Frame(self.tabs)
        # ... content
        self.table_cat = PeriodicOperationsTable(parent=self.tab_cat)
        self.table_cat.pack(expand=1, fill="both")
        self.table_cat.bind("<Double-1>", self.operation_edit)
        # 3) Tab Maintenance plan
        self.tab_plan = ttk.Frame(self.tabs)
        # ... content
        # ToDo: Add haul panel and switcher to absolute / relative
        self.table_plan = MaintenancePlanTable(parent=self.tab_plan)
        self.table_plan.pack(expand=1, fill="both")
        self.table_plan.bind('<Double-1>', lambda e: 'break')
        # Push our tabs to tabs-widget
        self.tabs.add(self.tab_log, text='Operations history')
        self.tabs.add(self.tab_cat, text='Periodic operations catalogue')
        self.tabs.add(self.tab_plan, text='Maintenance plan')
        self.tabs.pack(expand=1, fill="both")

        # Additional elements place here
        # ------------------------------
        # ...
        # ToDo: status bar with tooltips

        # Document
        self._doc = None  # Create field for document
        self.log_new()    # Initialize document

    @property
    def doc(self):
        return self._doc

    @doc.setter
    def doc(self, new_doc):
        self._doc = new_doc
        self.update_title()

    def update_title(self, event=None):
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
            self.doc = TkVehicleLogBook(
                parent=self,
                label="New Vehicle",
                production_date=date.today(),
                tab_log=self.table_log,
                tab_cat=self.table_cat,
                tab_plan=self.table_plan)

    def log_open(self, event=None):
        not_cancelled = self.ask_save()
        if not_cancelled:
            filename = tk.filedialog.askopenfilename(
                parent=self.master,
                title="Open vehicle log book",
                defaultextension=self.doc.extension,
                filetypes=self.filetypes,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
            if not filename:
                return
            try:
                self.doc.load(filename)
                self.update_title()
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
            filetypes=self.filetypes,
            initialfile=self.doc.label,
            initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        self.doc.save(filename)

    def import_log(self, event=None):
        filename = tk.filedialog.askopenfilename(
                parent=self.master,
                title="Import vehicle operations log",
                defaultextension=self.extension_imp_exp,
                filetypes=self.extensions_imp_exp,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        # Add extension (if missed).
        ext = os.path.splitext(filename)[-1]
        if not ext or ext != self.extension_imp_exp:
            filename += self.extension_imp_exp
        self.doc.import_log(filename)

    def import_cat(self, event=None):
        filename = tk.filedialog.askopenfilename(
                parent=self.master,
                title="Import vehicle periodic operations catalogue",
                defaultextension=self.extension_imp_exp,
                filetypes=self.extensions_imp_exp,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        # Add extension (if missed).
        ext = os.path.splitext(filename)[-1]
        if not ext or ext != self.extension_imp_exp:
            filename += self.extension_imp_exp
        self.doc.import_cat(filename)

    def export_log(self, event=None):
        filename = tk.filedialog.asksaveasfilename(
                parent=self.master,
                title="Export vehicle operations log",
                defaultextension=self.extension_imp_exp,
                filetypes=self.extensions_imp_exp,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        # Add extension (if missed).
        ext = os.path.splitext(filename)[-1]
        if not ext or ext != self.extension_imp_exp:
            filename += self.extension_imp_exp
        self.doc.export_log(filename)

    def export_cat(self, event=None):
        filename = tk.filedialog.asksaveasfilename(
                parent=self.master,
                title="Export vehicle periodic operations catalogue",
                defaultextension=self.extension_imp_exp,
                filetypes=self.extensions_imp_exp,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        # Add extension (if missed).
        ext = os.path.splitext(filename)[-1]
        if not ext or ext != self.extension_imp_exp:
            filename += self.extension_imp_exp
        self.doc.export_cat(filename)

    def export_plan(self, event=None):
        filename = tk.filedialog.asksaveasfilename(
                parent=self.master,
                title="Export vehicle maintenance plan",
                defaultextension=self.extension_imp_exp,
                filetypes=self.extensions_imp_exp,
                initialfile=self.doc.label,
                initialdir=os.path.dirname(self.doc.filename))
        if not filename:
            return
        # Add extension (if missed).
        ext = os.path.splitext(filename)[-1]
        if not ext or ext != self.extension_imp_exp:
            filename += self.extension_imp_exp
        self.doc.export_plan(filename)

    # def print_log(self, event=None):
    #     print('print_log')
    #
    # def print_cat(self, event=None):
    #     print('print_cat')
    #
    # def print_plan(self, event=None):
    #     print('print_plan')
    #
    # def print_active_tab(self, event=None):
    #     print('print_active_tab')

    def quit(self, event=None):
        not_cancelled = self.ask_save()
        if not_cancelled:
            self.master.quit()

    def vehicle_setup(self, event=None):
        VehicleSetupWindow(master=self, vehicle=self.doc)
        self.update_title()

    def operation_add(self, event=None):
        AddOperationWindow(master=self, vehicle=self.doc)

    def get_selected_operations(self):
        # get active tab
        tab = self.tabs.get_active_tab()
        # get treeview-table in active tab
        tree = tab.winfo_children()[0]
        # get operation by selection in treeview-table
        operations = self.doc.get_ops_by_selection(tree)
        return operations

    def operation_edit(self, event=None):
        try:
            operations = self.get_selected_operations()
        except ValueError as err:
            tk.messagebox.showwarning(parent=self.master,
                                      title="Edit item warning",
                                      message="Unable to edit selection",
                                      detail=err)
        else:
            if len(operations) == 1:
                AddOperationWindow(master=self.master,
                                   vehicle=self.doc,
                                   operation=operations[0])
            elif len(operations) > 1:
                tk.messagebox.showwarning(
                    parent=self.master,
                    title="Edit item warning",
                    message="Unable to edit multiple items",
                    detail="Select one item and retry.")
            else:
                tk.messagebox.showwarning(
                    parent=self.master,
                    title="Edit item warning",
                    message="No selected item in active tab to edit ",
                    detail="Select item and retry.")
        # To prevent propagation of signal to other bindings
        # (do not expand items)
        return "break"

    def operation_delete(self, event=None):
        try:
            operations = self.get_selected_operations()
        except ValueError as err:
            tk.messagebox.showwarning(parent=self.master,
                                      title="Delete item warning",
                                      message="Unable to delete selection",
                                      detail=err)
        else:
            if len(operations) > 0:
                ans = tk.messagebox.askquestion(
                    parent=self.master,
                    title="Question",
                    message="Are you sure want to delete selected item(s)?",
                    detail="Attention! If you delete periodic operation, "
                           "all operations with the same label will be removed",
                    icon="question",
                    type="yesno")
                if ans == 'no':
                    return
                table = self.tabs.get_active_tab()
                if table == self.tab_log:
                    self.doc.remove_from_log(operations)
                elif table == self.tab_cat:
                    self.doc.remove_from_cat(operations)
                else:
                    tk.messagebox.showwarning(
                        parent=self.master,
                        title="Delete item warning",
                        message="Unable to edit maintenance plan.\n"
                                "It is generated automatically.",
                        detail="Select item in another tab and retry.")
            else:
                tk.messagebox.showwarning(
                    parent=self.master,
                    title="Delete item warning",
                    message="No selected item in active tab to remove it ",
                    detail="Select item and retry.")

    def dlg_help(self):
        tk.messagebox.showinfo(
            parent=self.master,
            title="About {0} v{1}".format(
                self.master_title, siu.VERSION),
            message=
            "This application designed to simplify car maintenance planning.",
            detail=
            "You need to customize default service operations list and entry "
            "data about all previous service operations with your car. After "
            "that this application can advice when does your car needs in the "
            "next preventive maintenance.\n\n"
            "I hope it will be helpful for you. So I followed the idea of "
            "application that was:\n"
            "1. lightweight: no site-packages and no installation needed\n"
            "2. provides easy way to keep and manage data\n"
            "3. allow reliable data import/export\n"
            "4. opensource: it released under GPL v3.0 license\n"
            "5. crossplatform\n\n\n"
            "Source (see for updates):\n"
            "www.github.com/zokalo/pyServiceInterval\n\n"
            "Author:\tDon Dmitriy Sergeevich\n\n"
            "Send your feedback to dondmitriys@gmail.com")

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
        self.update_idletasks()

        # Add widgets
        # -----------
        # Container 1: LABEL
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

        # Container 2: PRODUCED
        # -----------
        frame = tk.Frame(master=self, bd=10)
        frame.pack(side=tk.TOP, fill=tk.X)
        # Entry Vehicle production date
        vcmd = (self.register(date_validate),
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
        self.txt_date.pack(side=tk.RIGHT)
        # Label "Enter vehicle production date (YYYY-MM-DD):"
        lbl_prod = tk.Label(master=frame,
                            text="Enter vehicle production date (YYYY-MM-DD):",
                            anchor=tk.E, justify=tk.RIGHT)
        lbl_prod.pack(side=tk.RIGHT)
        # ToDo: Add calendar widget

        # Container 2: HAUL
        # -----------
        frame = tk.Frame(master=self, bd=10)
        frame.pack(side=tk.TOP, fill=tk.X)
        # Entry Vehicle production date
        vcmd_num = (self.register(num_validate), '%S')
        self.txt_haul = tk.Entry(master=frame,
                                 validate="key", validatecommand=vcmd_num)
        self.txt_haul.insert(0, self.vehicle.haul)
        self.txt_haul.pack(side=tk.RIGHT)
        lbl_haul = tk.Label(master=frame,
                            text="Vehicle haul for today, km:",
                            anchor=tk.E, justify=tk.RIGHT)
        lbl_haul.pack(side=tk.RIGHT)

        # Container 3: BUTTONS
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

    def btn_ok(self, event=None):
        new_date = self.txt_date.get()
        new_label = self.txt_label.get()
        new_haul = self.txt_haul.get()
        try:
            new_date = new_date.replace('.', '-')
            new_date = datetime.strptime(new_date, '%Y-%m-%d').date()
            new_haul = float(new_haul)
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
            self.vehicle.haul = new_haul
            self.destroy()


def num_validate(insert_char):
    # only numbers and . , allowed
    allowed = "0123456789.,"
    if len(insert_char) == 1 and insert_char not in allowed:
        return False
    return True


def date_validate(insert_index, new_value, insert_char):
    # Return True if new_value is valid
    # Allowed symbols for differenet position indexes.
    allowed = ('12', '0123456789', '0123456789', '0123456789',
               r'-.',
               '01', '0123456789',
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

    def bind(self, *args, **kwargs):
        self.tree.bind(*args, **kwargs)

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
        iid = self.tree.insert(parent,
                               index=index,
                               iid=item_id,
                               values=values)
        return iid

    def clear(self):
        # Remove all items from Table
        for i in self.tree.get_children():
            self.tree.delete(i)


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
        super().insert(parent=iid,
                       values=("", "", operation.comment))


class PeriodicOperationsTable(Table):
    """ Periodic operations table widget.
    """
    # Position indexes of content in item values
    ind_interval_time = 0
    ind_interval_haul = 1
    ind_label = 2
    # example:
    # values = tree.item(item_id, option="values")
    # label = values[self.tab_cat.ind_label]

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
        # ATTENTION ! Place items with respect to class-fields ind_* :
        item = [None]*3
        item[self.ind_interval_time] = interval_time
        item[self.ind_interval_haul] = operation.interval_km
        item[self.ind_label] = operation.label
        item = tuple(item)
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
    """  Modal window for adding/editing operation
    """
    new_op_label = "New operation"
    title_edit = "Edit operation"
    title_new = "Add new operation"

    def __init__(self, vehicle, master=None, operation=None, **options):

        # Initialize data fields
        # ----------------------
        # Vehicle Log Book object
        self.vehicle = vehicle
        if not operation:
            operation = siu.Operation(self.new_op_label)
            self.window_title = self.title_new
            self.operation_action = self.operation_new
            self.mode_new = True
            self.mode_edit = False
        else:
            self.window_title = self.title_edit
            self.operation_action = self.operation_edit
            self.mode_new = False
            self.mode_edit = True
        # Operation object
        self.operation = operation
        # Selected operation label
        self.op_label = tk.StringVar()
        self.op_label.set(self.operation.label)
        # All known operation labels
        # --------
        # if self.mode_edit:
        #     # Select another label forbidden. Only edit.
        #     self.op_list = [self.operation.label]
        # --------
        # else:
        # mode_new
        # First position allow to enter new operation label
        self.op_list = self.vehicle.get_all_oper_labels()
        if self.new_op_label in self.op_list:
            # delete current operation label...
            self.op_list.remove(self.new_op_label)
        # ...and insert it first
        self.op_list.insert(0, self.new_op_label)
        # --------
        # end {if self.mode_edit: ... else: ...}

        # Checkbox variable - is operation periodic
        self.is_periodic = tk.IntVar()
        self.is_periodic.set(self.operation.is_periodic)
        # Operation period
        self.period_year = tk.StringVar()
        self.period_year.set(round(self.operation.interval_time.days/365, 1))
        self.period_km = tk.StringVar()
        self.period_km.set(self.operation.interval_km)
        # Checkbox variable - is operation done
        self.is_done = tk.IntVar()
        self.is_done.set(self.operation.is_done)
        # Done date/km
        self.done_date = tk.StringVar()
        self.done_km = tk.StringVar()
        if self.operation.is_done:
            self.done_date.set(str(self.operation.done_at_date))
            self.done_km.set(self.operation.done_at_km)
        else:
            self.done_date.set(str(date.today()))
            self.done_km.set(self.vehicle.haul)
        # Comment
        # Comment must be fetched from comment text widget using get() method

        # Initialize window
        # -----------------
        super().__init__(master, **options)
        self.title(self.window_title)
        self.minsize(width=350, height=400)
        self.update_idletasks()
        # self.resizable(width=tk.FALSE, height=tk.FALSE)

        # Add widgets
        # -----------
        frm_lbl = tk.Frame(master=self, bd=10)
        frm_lbl.pack(fill=tk.X)
        # Label "Enter operation label:"
        lbl_oper = tk.Label(
            master=frm_lbl,
            text="Enter new operation label or select exist:",
            anchor=tk.W, justify=tk.LEFT)
        lbl_oper.pack(side=tk.TOP, fill=tk.X)

        # Combobox - select Operation Label
        self.cmb_label = ttk.Combobox(
            master=frm_lbl,
            textvariable=self.op_label)
        self.cmb_label.bind('<Return>', self.cmb_changed)
        self.cmb_label.bind("<<ComboboxSelected>>", self.label_selected)
        self.cmb_label['values'] = self.op_list
        self.cmb_label.pack(side=tk.TOP, fill=tk.X)

        # Checkbox - periodic
        frm_prd = tk.Frame(master=self, bd=10)
        frm_prd.pack(fill=tk.X, side=tk.TOP)
        frm_prd_cb = tk.Frame(master=frm_prd, bd=0)
        frm_prd_cb.pack(fill=tk.X, side=tk.TOP)
        self.chk_period = tk.Checkbutton(master=frm_prd_cb,
                                         text="Periodic operation",
                                         variable=self.is_periodic,
                                         onvalue=True,
                                         command=self.period_chk_update)
        self.chk_period.pack(side=tk.LEFT)
        # Entry - Period year
        frm_prd_yr = tk.Frame(master=frm_prd, bd=0)
        frm_prd_yr.pack(side=tk.TOP, fill=tk.X)
        vcmd_num = (self.register(num_validate), '%S')
        self.txt_per_year = tk.Entry(master=frm_prd_yr,
                                     validate="key", validatecommand=vcmd_num,
                                     textvariable=self.period_year,
                                     width=10)
        self.txt_per_year.pack(side=tk.RIGHT)
        # Label - period year
        lbl_prd_yr = tk.Label(
            master=frm_prd_yr,
            text="Interval, years:",
            anchor=tk.E, justify=tk.RIGHT)
        lbl_prd_yr.pack(side=tk.RIGHT)
        # Entry - Period km
        frm_prd_km = tk.Frame(master=frm_prd, bd=0)
        frm_prd_km.pack(side=tk.TOP, fill=tk.X)
        self.txt_per_km = tk.Entry(master=frm_prd_km,
                                   validate="key", validatecommand=vcmd_num,
                                   textvariable=self.period_km,
                                   width=10)
        self.txt_per_km.pack(side=tk.RIGHT)
        # Label - period km
        lbl_prd_km = tk.Label(
            master=frm_prd_km,
            text="Interval, km:",
            anchor=tk.E, justify=tk.RIGHT)
        lbl_prd_km.pack(side=tk.RIGHT)
        # Update entry states
        self.period_chk_update()

        # Checkbox - done
        frm_done = tk.Frame(master=self, bd=10)
        frm_done.pack(fill=tk.X, side=tk.TOP)
        frm_done_cb = tk.Frame(master=frm_done, bd=0)
        frm_done_cb.pack(fill=tk.X, side=tk.TOP)
        self.chk_done = tk.Checkbutton(master=frm_done_cb,
                                       text="Operation done",
                                       variable=self.is_done,
                                       onvalue=True,
                                       command=self.done_chk_update)
        self.chk_done.pack(side=tk.LEFT)
        # Entry - done date
        frm_done_date = tk.Frame(master=frm_done, bd=0)
        frm_done_date.pack(side=tk.TOP, fill=tk.X)
        vcmd_date = (self.register(date_validate),
                     '%i', '%P', '%S')
        self.txt_done_date = tk.Entry(master=frm_done_date,
                                      validate="key",
                                      validatecommand=vcmd_date,
                                      textvariable=self.done_date,
                                      width=10)
        self.txt_done_date.pack(side=tk.RIGHT)
        # Label - done date
        lbl_done_date = tk.Label(
            master=frm_done_date,
            text="Date (YYYY-MM-DD):",
            anchor=tk.E, justify=tk.RIGHT)
        lbl_done_date.pack(side=tk.RIGHT)
        # Entry - done km
        frm_done_km = tk.Frame(master=frm_done, bd=0)
        frm_done_km.pack(side=tk.TOP, fill=tk.X)
        self.txt_done_km = tk.Entry(master=frm_done_km,
                                   validate="key", validatecommand=vcmd_num,
                                   textvariable=self.done_km,
                                   width=10)
        self.txt_done_km.pack(side=tk.RIGHT)
        # Label - done km
        lbl_done_km = tk.Label(
            master=frm_done_km,
            text="Haul, km:",
            anchor=tk.E, justify=tk.RIGHT)
        lbl_done_km.pack(side=tk.RIGHT)
        # Update entry states
        self.done_chk_update()

        # Comment
        # Label Comment:
        frm_cmt = tk.Frame(master=self, bd=10)
        frm_cmt.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        lbl_cmt = tk.Label(
            master=frm_cmt,
            text="Comment:",
            anchor=tk.W, justify=tk.LEFT)
        lbl_cmt.pack(side=tk.TOP, fill=tk.X)
        # Comment Text
        self.txt_cmt = tk.Text(master=frm_cmt)
        self.txt_cmt.insert("1.0", self.operation.comment)
        self.txt_cmt.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        # Add vertical scrollbar
        vsbar = tk.Scrollbar(self.txt_cmt)
        vsbar.config(command=self.txt_cmt.yview)
        self.txt_cmt.config(yscrollcommand=vsbar.set)
        vsbar.pack(side=tk.RIGHT, fill=tk.Y)

        # # Disable done-controls for periodic operation if mode_edit
        # if self.mode_edit
        #     and self.operation.is_periodic \
        #         and not self.operation.is_done:

        # Buttons OK/CANCEL
        frm_btns = tk.Frame(master=self, bd=10)
        frm_btns.pack(side=tk.BOTTOM)
        # Button OK
        btn_ok = tk.Button(master=frm_btns,
                           text="Ok",
                           command=self.btn_ok,
                           height=1, width=10)
        btn_ok.pack(side=tk.LEFT)
        # btn_ok.bind("<Return>", self.btn_ok)  # Not used to allow pressing
        # enter while writing comment text
        # Button Cancel
        btn_cancel = tk.Button(master=frm_btns,
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

    def cmb_changed(self, event=None):
        """ Update labels list
        Called when user edited operation label
        """
        new_label = self.op_label.get()
        if new_label in self.op_list:
            # If label already exist - user select exist label
            # from list of combobutton
            self.label_selected()
        # Update labels list
        self.op_list = self.vehicle.get_all_oper_labels()
        self.op_list = list(self.op_list)
        if self.new_op_label in self.op_list:
            # delete current operation label...
            self.op_list.remove(self.new_op_label)
        # ...and insert it first
        self.op_list.insert(0, new_label)
        # Update combobox list
        self.cmb_label['values'] = self.op_list
        # print("cmb_changed" + self.op_label.get())

    def btn_ok(self, event=None):
        """Add new or edit exist operation for vehicle
        """
        success = self.operation_action()
        # Close window if success
        if success:
            self.destroy()

    def operation_edit(self, testmode=False):
        """ Update operation data from GUI
        :param testmode:  if True - run in test mode.
                          Data will be added to a test operation instance
                          to validate all values
                          if False - run at test mode, than run in work mode to
                          modify real operation object
        :return:          True if success, else False
        """
        if not testmode:
            # At first run in test mode
            success = self.operation_edit(testmode=True)
            if not success:
                return False
            # If we reach this line - all is ok. Modify real object
            operation = self.operation
        elif testmode:
            # Run in test mode
            operation = siu.Operation("Test")
        else:
            raise TypeError(
                "Argument testmode must be <bool>, not " + str(type(testmode)))
        # Verify GUI fields by trying to use it
        try:
            # keep old label to reAdd operations to catalogue if it is periodic
            old_label = operation.label
            operation.label = self.op_label.get()
            if self.is_periodic.get():
                operation.interval_time = \
                    timedelta(days=365 * float(self.period_year.get()))
                operation.interval_km = float(self.period_km.get())
                if float(self.period_km.get()) == 0:
                    raise ValueError(
                        "For periodic operation interval (km) must be non-zero")

            if self.is_done.get():
                done_km = float(self.done_km.get())
                done_date = self.done_date.get()
                done_date = done_date.replace('.', '-')
                done_date = datetime.strptime(done_date, '%Y-%m-%d').date()
                done_comment = self.txt_cmt.get("1.0", tk.END + "-1c")
                if self.mode_edit:
                    self.operation._is_done = True
                    self.operation.done_at_km = done_km
                    self.operation.done_at_date = done_date
                    self.operation.comment = done_comment
                else:
                    self.operation = self.operation.done(done_km,
                                                         done_date,
                                                         done_comment)

            if not self.is_done.get() and not self.is_periodic.get():
                raise ValueError("Unable to create operation that is not "
                                 "periodic and have never been done.")
            if not testmode:
                # reAdd periodic operation to catalogue with new label
                # and rename old operations in log with label same as old label
                self.vehicle.op_label_replace(old=old_label,
                                              new=operation.label)
        except Exception as err:
            tk.messagebox.showerror(parent=self,
                                    title="Error",
                                    message="Wrong operation data format",
                                    detail=err)
            return False
        else:
            return True

    def operation_new(self):
        # Edit self.operation and put it into vehicle log book
        success = self.operation_edit()
        if not success:
            return False
        if self.operation.is_done:
            self.vehicle.add_operation_to_log(self.operation)
            # If operation is periodic it will be also automatically pushed to
            # periodic operations catalogue
        elif self.operation.is_periodic:
            self.vehicle.add_operation_to_cat(self.operation)
        return True

    def label_selected(self, event=None):
        # Called if user select label from combobox's list
        label = self.op_label.get()
        # Get periods for this operation
        operation = self.vehicle.get_periodic(label)
        # (None if not exist)
        if operation:
            self.is_periodic.set(True)
            self.period_chk_update()
            self.period_year.set(round(operation.interval_time.days/365, 1))
            self.period_km.set(operation.interval_km)
        else:
            # It seems that operations is not periodic
            self.is_periodic.set(False)
            self.period_chk_update()

    def period_chk_update(self):
        # Set enabled/disabled controls to setup period for operation
        state = "normal" if self.is_periodic.get() else "disabled"
        self.txt_per_km.config(state=state)
        self.txt_per_year.config(state=state)

    def done_chk_update(self):
        # Set enabled/disabled controls
        state = "normal" if self.is_done.get() else "disabled"
        self.txt_done_km.config(state=state)
        self.txt_done_date.config(state=state)


class TkVehicleLogBook(object):
    """ Represents storage of service operations .
    Wrapper for VehicleLogBook that can be used in Tk-GUI.
    It linked with tkinter Table widgets based on TreeView.
    """
    def __init__(self, tab_log, tab_cat, tab_plan,
                 *args, parent=None, **kwargs):
        super().__init__()
        self.parent = parent
        self.tab_log = tab_log
        self.tab_cat = tab_cat
        self.tab_plan = tab_plan
        self.log_book = siu.VehicleLogBook(*args, **kwargs)
        self.tabs_update()

    def remove_from_log(self, operations):
        self.log_book.remove_from_log(operations)
        self.tab_log_update()

    def remove_from_cat(self, operations):
        # If you delete periodic operation,
        # all operations with the same label becames on-periodic.
        self.log_book.remove_from_cat(operations)
        self.tabs_update()

    def op_label_replace(self, old, new):
        """
        - reAdd periodic operation to catalogue with new label
        - and rename old operations in log with label same as old label
        - [added] update tables
         """
        self.log_book.op_label_replace(old, new)
        self.tabs_update()

    def make_maintenance_plan(self, *args, **kwargs):
        return self.log_book.make_maintenance_plan(*args, **kwargs)

    def get_all_oper_labels(self):
        return self.log_book.get_all_oper_labels()

    def get_periodic(self, *args, **kwargs):
        return self.log_book.get_periodic(*args, **kwargs)

    def get_ops_by_selection(self, tree):
        """ Get operations by selection in table widget, based on treeview
        :param tree: Tree widget based on ttk.Treeview
        :return: list of <Operation> class instance's
        """
        if not isinstance(tree, ttk.Treeview):
            raise TypeError(
                "Argument <tree> must be a <ttk.Treeview> type, not " +
                str(type(tree)))
        item_ids = tree.selection()

        operations = list()

        if isinstance(item_ids, tuple):
            # Selected more than one item
            pass
        else:
            item_ids = (item_ids,)

        for item_id in item_ids:
            if tree == self.tab_log.tree:
                # Selection by index of item selected in tab_log
                index = tree.index(item_id)
                # Check is item in the top list
                # if item has no parent - it is placed in the top
                parent_id = tree.parent(item_id)
                if parent_id:
                    # if item has parent, get parent index
                    index = tree.index(parent_id)
                if len(self.log_book.operations_log) == 0:
                    raise ValueError("Nothing to select")
                operations.append(self.log_book.operations_log[index])
            elif tree == self.tab_cat.tree:
                # selection by label of selected item in tab_cat
                values = tree.item(item_id, option="values")
                try:
                    label = values[self.tab_cat.ind_label]
                except IndexError:
                    label = None
                if not label:
                    raise ValueError("No selected item")
                operations.append(self.log_book.operations_cat[label])
            elif tree == self.tab_plan.tree:
                raise ValueError(
                    "Unable to edit maintenance plan.\n"
                    "It is generated automatically.")
            else:
                raise ValueError(
                    "Unknown ttk.Treeview widget in argument tree.")
        return operations

    def event_generate_update(self):
        if self.parent:
            self.parent.event_generate(
                "<<refresh>>", when="tail", state=int(self.is_modified))

    def tabs_update(self):
        self.tab_log_update()
        self.tab_cat_update()
        self.tab_plan_update()

    def tab_log_update(self):
        # Remove all items from table and add all items again
        self.tab_log.clear()
        for op in self.log_book.operations_log:
            self.tab_log.insert(op)
            if op.is_periodic and op.label not in self.log_book.operations_cat:
                # check if operation became periodic
                self.add_operation_to_cat(op)
        self.event_generate_update()

    def tab_cat_update(self):
        # Remove all items from table and add all items again
        self.tab_cat.clear()
        ops = list()
        for op in self.log_book.operations_cat.values():
            ops.append(op)
        ops.sort(key=lambda x: x.interval_km)
        for op in ops:
            self.tab_cat.insert(op)
        self.event_generate_update()

    def tab_plan_update(self):
        # Remove all items from table and add all items again
        self.tab_plan.clear()
        plan = self.log_book.make_maintenance_plan()
        for op in plan:
            self.tab_plan.insert(op)
        self.event_generate_update()

    def add_operation_to_log(self, *args, **kwargs):
        self.log_book.add_operation_to_log(*args, **kwargs)
        self.tabs_update()

    def add_operation_to_cat(self, *args, **kwargs):
        self.log_book.add_operation_to_cat(*args, **kwargs)
        # We don't need to update tab_log
        self.tab_cat_update()
        self.tab_plan_update()

    def clear_log(self):
        self.log_book.clear_log()
        # We don't need to update tab_cat
        self.tab_log_update()
        self.tab_plan_update()

    def clear_all(self):
        self.log_book.clear_all()
        self.tabs_update()

    def import_log(self, *args, **kwargs):
        self.log_book.import_log(*args, **kwargs)
        self.tabs_update()

    def import_cat(self, *args, **kwargs):
        self.log_book.import_cat(*args, **kwargs)
        # We don't need to update tab_log
        self.tab_cat_update()
        self.tab_plan_update()

    def export_log(self, *args, **kwargs):
        self.log_book.export_log(*args, **kwargs)

    def export_cat(self, *args, **kwargs):
        self.log_book.export_cat(*args, **kwargs)

    def export_plan(self, *args, **kwargs):
        self.log_book.export_plan(*args, **kwargs)

    def load(self, *args, **kwargs):
        self.log_book = siu.VehicleLogBook.load(*args, **kwargs)
        self.tabs_update()

    def save(self, *args, **kwargs):
        self.log_book.save(*args, **kwargs)
        self.event_generate_update()

    def __str__(self):
        return self.log_book.operations_log.__str__()

    @property
    def haul(self):
        return self.log_book.haul

    @haul.setter
    def haul(self, new_haul):
        self.log_book.haul = new_haul
        self.tab_plan_update()

    @property
    def production_date(self):
        return self.log_book.production_date

    @production_date.setter
    def production_date(self, new_prod_date):
        self.log_book.production_date = new_prod_date
        self.tab_plan_update()

    @property
    def is_modified(self):
        return self.log_book.is_modified

    @property
    def extension(self):
        return self.log_book.extension

    @property
    def filename(self):
        return self.log_book.filename

    @property
    def label(self):
        return self.log_book.label

    @label.setter
    def label(self, new_label):
        self.log_book.label = new_label


class TabPanel(ttk.Notebook):
    """Added fields for linked data
    Linkage implemented not in all class interface functions:
    - add()             [override]
    - get_active_tab()  [new]
    """
    def __init__(self, *args, **kwargs):
        self.tabs_storage = list()
        super().__init__(*args, **kwargs)

    def add(self, child, **kw):
        super().add(child, **kw)
        self.tabs_storage.append(child)

    def get_active_tab(self):
        ind = self.index("current")
        return self.tabs_storage[ind]


if __name__ == "__main__":
    # table = Table(["Haul", "Date", "Operation"])
    # Run doctests.
    import doctest
    doctest.testmod()