import tkinter as tk
import textwrap as tw
from DatabaseManagement.Who_DML import acquired
from DatabaseManagement.DataLookUp import look_up
# from Interface.interface_config import *



def apply_dml():
    print(last_action_value)
    if last_action_value[0] == 0:
        print(f'Acquired : {dml_name} {dml_aired}')
        acquired(aired=dml_aired, title=dml_name, change=0)
    elif last_action_value[0] == 1:
        print('Partial')
        acquired(aired=dml_aired, title=dml_name, change=1)
    elif last_action_value[0] == 2:
        print('On Order')
        acquired(aired=dml_aired, title=dml_name, change=2)
    elif last_action_value[0] == 3:
        print('Remove')
        acquired(aired=dml_aired, title=dml_name, change=3)
    else:
        print('Not Working')


def last_action(evt):
    act =  evt.widget
    global last_action_value
    last_action_value = act.curselection()


def episode_mgr(name, aired):
    global dml_name, dml_aired
    dml_name = name
    dml_aired = aired
    global dml
    dml = tk.Tk()
    dml.geometry('640x480')
    dml.config(border=6, relief='sunken', background='navy')
    dml.wm_title("Update Story")

    # Configure Column within grid for each object
    dml.columnconfigure(0, weight=1)
    dml.columnconfigure(1, weight=0)

    dml.rowconfigure(0, weight=0)
    dml.rowconfigure(1, weight=1)
    dml.rowconfigure(2, weight=0)

    label = tk.Label(dml, text=f'{name}', font="FiraCode 12",foreground='white', background='blue4')
    label.grid(row=0, column=0, columnspan=2, sticky='we')

    ep_summary = tk.Listbox(dml)
    ep_summary.grid(row=1, column=0, columnspan=2, sticky='nsew')
    ep_summary.config(border=4, relief='sunken', selectbackground='grey20',foreground='white',
                      background='DodgerBlue4',font="FiraCode 10")

    for saga in look_up(title=name, aired=aired):  # Insert output into window
        print(saga)
        ep_summary.insert(tk.END, f"{saga[3]}) {saga[0]} ")
        ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}{saga[1]} : Doctor: {saga[6]} -- Season: {saga[2]}")
        ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Setting: {saga[10]}")
        ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Companions: {saga[8]}")
        ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Monster or Alien: {saga[9]}")

        ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Acquired: {saga[-1]}")
        ep_summary.insert(tk.END, '-' * 85)

        # wrap to 70 characters
        synposis = [x for x in tw.fill(text=saga[-2], width=70).split('\n')]
        for x in synposis:
            ep_summary.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}{x}")

    # Scroll box of Actions to take
    change_list = tk.Listbox(dml)
    change_list.grid(row=1, column=1 ,  sticky='sew')
    change_list.config(border=6, relief='sunken', selectbackground='snow', background='blue4',
                       foreground='white',font="FiraCode 12")

    for opt in ['Acquired' , 'Partial Acquisition' , 'On Order', 'Removed']:
        change_list.insert(tk.END, opt)  # Append each item to the end of the list as iterated.
    change_list.bind('<<ListboxSelect>>', last_action)  # bind the list box to a function

    b1 = tk.Button(dml, text='Apply', activebackground='green', highlightbackground='white', relief='raised',border=4,
                   font="FiraCode 9" ,command=apply_dml)
    b1.grid(row=2, column=1, columnspan=1, sticky='sw')

    b2 = tk.Button(dml, text="Exit", activebackground='maroon', highlightbackground='white',relief='raised',border=4,
                   font="FiraCode  9" , command=dml.destroy)
    b2.grid(row=2, column=1, columnspan=1 , sticky='se')

    dml.mainloop()
