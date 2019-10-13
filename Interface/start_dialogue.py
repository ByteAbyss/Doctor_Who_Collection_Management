import tkinter as tk
import tkinter.font as tkf
import os 
from PIL import ImageTk, Image
from DatabaseManagement.DataLookUp import doctors
from DatabaseManagement.DataLookUp import look_up
from WebParse.get_episodes import get_episodes
from Interface.episode_manager import episode_mgr

#TODO
#  Post Git Hub

mw = tk.Tk()
mw.title("Whovian Collection Management")
mw.geometry('1920x1080')
mw.config(border=4, relief='raised',  background='navy')
# '640x480+8+200 : resolution  --> offset + x Pixels from left edge of screen & y pixels down from the top ( - flips )

# Configuration - Fonts
button_font = tkf.Font(family="FiraCode Nerd Font Mono Italic", size=9, weight="bold")
label_font = tkf.Font(family="FiraCode", size=10, weight="bold")
header_font = tkf.Font(family="FiraCode Nerd Font Mono Italic", size=12, weight="bold")

# Configure Column within grid for each object
mw.columnconfigure(0, weight=3)  # Button Holder - Doctor Listing
mw.columnconfigure(1, weight=20)  # Listing of Sagas - OutPut

mw.rowconfigure(0, weight=0)  # Title
mw.rowconfigure(1, weight=1)  # List All Episodes Button
mw.rowconfigure(2, weight=1)  # Label - Filter By Doctor
mw.rowconfigure(3, weight=2)  # Tardis - rowspan=2
mw.rowconfigure(4, weight=1)
mw.rowconfigure(5, weight=1)  # Label -- Search by name
mw.rowconfigure(6, weight=1)  # Search Box
mw.rowconfigure(7, weight=1)  # Submit Button for search
mw.rowconfigure(8, weight=1)
mw.rowconfigure(9, weight=1)   # Update Database Button
mw.rowconfigure(10, weight=1)  # Image --  Tardis
mw.rowconfigure(11, weight=1)  # Quit Button
mw.rowconfigure(12, weight=0)  # Y -Scroll


# Functions
def exit_who():
    mw.destroy()


def select_one_doctor(evt):
    # Note here that Tkinter passes an event object to function.
    time_lord = evt.widget
    index = int(time_lord.curselection()[0])+1
    if index:
        listing(num=index, all=0)


def last_action(evt):
    act =  evt.widget
    global last_action_value
    last_action_value = act.curselection()


def get_story(evt):
    story = evt.widget
    s_out = story.curselection()    # Store in variable the selection from the list box
    value = story.get(s_out)        # Extract Data
    global aired, title
    try:
        aired = int(value.split(')')[0])
        title = value.split(')')[1].strip()
        print(aired, title)
        episode_mgr(name=title, aired=aired)
    except:
        print('No Dice')

def s_name():
    global s_input
    title = s_input.get()
    OutPut.delete(0, tk.END)  # clear the output text text widget
    OutPut.update()
    for saga in look_up(title=title):  # Insert output into window
        OutPut.insert(tk.END, f"{saga[3]}) {saga[0]} ")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}{saga[1]} : Doctor: {saga[6]} -- Season: {saga[2]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Setting: {saga[10]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Companions: {saga[8]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Monster or Alien: {saga[9]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Acquired: {saga[-1]}")
        OutPut.insert(tk.END, '-' * 85)


def listing(num=0, all=1):
    """Clear Output screen & populate based on Doctor Clicked on """
    OutPut.delete(0,tk.END)  # clear the output text text widget
    OutPut.update()
    for saga in look_up(doctor=num, all=all):  # Insert output into window
        OutPut.insert(tk.END, f"{saga[3]}) {saga[0]} ")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}{saga[1]} : Doctor: {saga[6]} -- Season: {saga[2]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Setting: {saga[10]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Companions: {saga[8]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Monster or Alien: {saga[9]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Acquired: {saga[-1]}")
        OutPut.insert(tk.END, '-'*85)


def not_collected():
    """Clear Output screen & populate stories missing """
    OutPut.delete(0,tk.END)  # clear the output text text widget
    OutPut.update()
    for saga in look_up(acquired='No'):  # Insert output into window
        OutPut.insert(tk.END, f"{saga[3]}) {saga[0]} ")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}{saga[1]} : Doctor: {saga[6]} -- Season: {saga[2]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Setting: {saga[10]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Companions: {saga[8]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Monster or Alien: {saga[9]}")
        OutPut.insert(tk.END, f"{' '*(len(saga[3])+2)}Acquired: {saga[-1]}")
        OutPut.insert(tk.END, '-'*85)


def acquired():
    """Clear Output screen & populate stories collected """
    OutPut.delete(0, tk.END)  # clear the output text text widget
    OutPut.update()
    for saga in look_up(acquired='Yes'):  # Insert output into window
        OutPut.insert(tk.END, f"{saga[3]}) {saga[0]} ")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}{saga[1]} : Doctor: {saga[6]} -- Season: {saga[2]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Setting: {saga[10]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Companions: {saga[8]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Monster or Alien: {saga[9]}")
        OutPut.insert(tk.END, f"{' ' * (len(saga[3]) + 2)}Acquired: {saga[-1]}")
        OutPut.insert(tk.END, '-' * 85)


def web_update():
    OutPut.delete(0,tk.END) # clear the output text text widget
    OutPut.insert(tk.END, ' Scraping the Web Please be Patient '.center(85, '#'))
    OutPut.update()
    who_update = get_episodes()
    if who_update == '--- No New Results -----':
        OutPut.insert(tk.END, '--- No New Results -----')
    else:
        for elem in who_update:
            OutPut.insert(tk.END, 'Record Added'.center(85, '-'))
            OutPut.insert(tk.END, '')
            OutPut.insert(tk.END, f"{elem[0]} | {elem[1]} | {elem[2]}")
            OutPut.insert(tk.END, f"{elem[3]} | {elem[5]} | {elem[6]}")
            OutPut.insert(tk.END, f"{elem[7]} | {elem[8]}")
            OutPut.insert(tk.END, f"{elem[9]} | {elem[10]} ")
            OutPut.insert(tk.END, f"{elem[4]}")
            OutPut.insert(tk.END, '')
        for doc in doctors():  # Refresh list
            DocList.insert(tk.END, doc)  # Append each item to the end of the list as iterated.
        DocList.bind('<<ListboxSelect>>', select_one_doctor)  # bind the list box to a function


# Objects
label = tk.Label(mw, text='Doctor Who Collection Status', font=header_font, background='blue4', foreground='snow')
label.grid(row=0, column=0, columnspan=3, sticky='we')

list_all = tk.Button(mw, text='List All Episodes', activebackground='green',relief='raised',border=4,font=button_font,
                     highlightbackground='white', command=listing).grid(row=1, column=0, sticky='we')

pending = tk.Button(mw, text='Not Acquired', activebackground='maroon', relief='raised',border=4,font=button_font,
                     highlightbackground='red', command=not_collected).grid(row=8, column=0, sticky='e')

collected = tk.Button(mw, text='Acquired', activebackground='green',relief='raised',border=4,font=button_font,
                     highlightbackground='green', command=acquired).grid(row=8, column=0, sticky='w')

# OutPut of Sagas :  ListBox
out_row = 1000
OutPut = tk.Listbox(mw)
OutPut.grid(row=1, rowspan=out_row, column=1, sticky='nsew')
OutPut.config(border=4, relief='sunken', background='DodgerBlue4',foreground='white',
              selectbackground='snow', font="FiraCode 11")
OutPut.bind('<<ListboxSelect>>', get_story)  # bind the list box to a function

#  Output Scrollbar      -- Y & X for Output Listbox
OutScrollY = tk.Scrollbar(mw, orient=tk.VERTICAL, command=OutPut.yview)
OutScrollY.grid(row=1, rowspan=out_row, column=2, sticky='nsew')
OutPut['yscrollcommand'] = OutScrollY.set

OutScrollX = tk.Scrollbar(mw, orient=tk.HORIZONTAL, command=OutPut.xview)
OutScrollX.grid(row=12, rowspan=out_row, column=1, sticky='nsew')
OutPut['xscrollcommand'] = OutScrollX.set

# Doctor Choices Listbox
incarnation = tk.Label(mw, text='Filter by Doctor')
incarnation.grid(row=2, column=0, sticky='we')
incarnation.configure(border=4, relief='raised', background='DodgerBlue4', font=label_font)
# sticky - north , south , east , west of the side ( top, bottom, left , right ) within it cell.

# List of Doctor Box  --
tardis = tk.Frame(mw)
tardis.grid(row=3, column=0, rowspan=2, sticky='nsew')
tardis.config(relief='raised', borderwidth=6, background='gray24')
tardis.columnconfigure(0, weight=1)
tardis.rowconfigure(0, weight=3)

# Scroll box of Doctors to filter by
DocList = tk.Listbox(tardis)
DocList.grid(row=0, column=0 , sticky='nsew' )
DocList.config(border=4, relief='sunken', background='DodgerBlue4',foreground='white',
               selectbackground='snow', font="FiraCode 9")

for doc in doctors():
    DocList.insert(tk.END, doc)  # Append each item to the end of the list as iterated.
DocList.bind('<<ListboxSelect>>', select_one_doctor)  # bind the list box to a function

# Doctor Choices Listbox
incarnation = tk.Label(mw, text='Search by Name')
incarnation.grid(row=5, column=0, sticky='we')
label_font = tkf.Font(family="FiraCode", size=9, weight="bold")
incarnation.configure(border=4, relief='raised', background='DodgerBlue4', font=label_font)

# Search by Name of Episode
s_input = tk.StringVar()
search_name = tk.Entry(mw, textvariable=s_input).grid(row=6, column=0, rowspan=1, columnspan=1, sticky='nswe')
Submit = tk.Button(mw, text='Submit', activebackground='green', highlightbackground='white', font=button_font,
                   relief='raised', border=4, command=s_name).grid(row=7, column=0, sticky='we')

# Update Database Button
up = tk.Button(mw, text='Update Database', activebackground='green', relief='raised',border=4, font=button_font,
               highlightbackground='white', command=web_update).grid(row=9, column=0, sticky='ew')

# Embed Image #
fileDir = os.path.dirname(os.path.realpath(__file__))
tardis_loc = os.path.join(fileDir,'tardis20.png')
img =  ImageTk.PhotoImage(Image.open(tardis_loc))

""" 
Notes -- Convert image via Image magic :
    # convert -resize 50% myfigure.png myfigure.jpg
    # find . -maxdepth 1 -iname "*.jpg" | xargs -L1 -I{} convert -resize 30% "{}" _resized/"{}"
"""

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
tardis_image = tk.Label(mw, image = img, border=6, relief='raised', background='grey56').grid(row=10, rowspan=1,
                                                                                              column=0, sticky='nsew')

killme = tk.Button(mw, text='Quit', activebackground='maroon', highlightbackground='white', relief='raised', border=4,
                   font=button_font, command=exit_who).grid(row=11, column=0, sticky='we')


mw.mainloop()   # Run Loop of Graphics -- Last item
