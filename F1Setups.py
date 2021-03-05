#from tkinter import *
from tkinter import ttk
from tkinter import Tk, Entry, EW, Scale, HORIZONTAL, DISABLED, Label, NSEW, Button, messagebox, filedialog, StringVar,BooleanVar,N,W,E,S,Listbox
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfile
import struct

import sys
import winreg
import re
import pathlib

import json

F1SetupPath = pathlib.Path(__file__).parent.absolute()

root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(F1SetupPath)+'/pog.ico')

s = ttk.Style() #s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.tk.call('lappend', 'auto_path', str(F1SetupPath)) #'C:/Users//hello/awthemes-10.2.1/awthemes-10.2.1'
root.tk.call('package', 'require', 'awdark')
s.theme_use('awdark')

steamappid = "1080110" #f12020 steam id
WorkshopID = "2403338074" #f2 2404403390
#WorkshopFile = "D:/SteamLibrary/steamapps/workshop/content/1080110/"+ WorkshopID +"/ugcitemcontent.bin"
WorkshopUrl = "https://steamcommunity.com/sharedfiles/filedetails/?id="+ WorkshopID
SetupDir = str(F1SetupPath) + "/Setups/" #"c:\Users\\hello\F1Setups/Setups/
setupStructFormat = '<4s5l1b 11sfb 13sb 20sb 11s3b 12s2b 16sfb 16s2b 13s9b 19s2b 14sfb13sfb15sfb16sfb16sfb15sfb13sfb12sfb20sfb19sfb27sfb26sfb22sfb21sfb18sfb14sfb29sfb28sfb28sfb27sfb11sfb13sfb21sfb21s8B'

bg = "#33393b"
fg = "white"
scale_length = "200" #length of all the sliders
scale_relief = "flat"

with open('tracks.json', encoding='utf-8') as json_file: 
    tracks = json.load(json_file) 

countrynames = list(tracks)

cnames = StringVar(value=countrynames)

raceSettings= {'F1 2020' : ["All Cars",
        "Ferrari",
        "Renault",
        "Red Bull",
        "McLaren",
        "Mercedes",
        "AlphaTauri",
        "Williams",
        "Racing Point",
        "Alfa Romeo",
        "Haas"],
    'F2 2020': ["All Cars", 
        "Dams",
        "Uni-Virtuosi Racing",
        "Art Grand Prix",
        "Carlin",
        "Campos Racing",
        "Charouz Racing System",
        "MP Motorsport",
        "BWT HWA Racelab",
        "Prema Racing",
        "Trident",
        "Hitech Grand Prix"],
    'F2 2019': ["All Cars", 
        "Dams",
        "Uni-Virtuosi Racing",
        "Art Grand Prix",
        "Carlin",
        "Campos Racing",
        "Sauber Junior Team By Charouz"
        "MP Motorsport",
        "BWT Arden",
        "Prema Racing",
        "Trident"],
    'classic': ["ALL Cars",
        "2010 Red Bull",
        "2010 Ferrari",
        "2010 McLaren",
        "2009 Brawn",
        "2008 McLaren",
        "2007 Ferrari",
        "2006 Renault",
        "2004 Ferrari",
        "2003 Williams",
        "1998 McLaren",
        "1996 Williams",
        "1992 Williams",
        "1991 McLaren",
        "1990 Ferrari",
        "1990 McLaren",
        "1988 McLaren",
        "1982 McLaren",
        "1979 Ferrari",
        "1978 Lotus",
        "1976 Ferrari",
        "1976 McLaren",
        "1972 Lotus"]
}

# Names of the weatherType we can send
weatherType = { 'Dry':'Dry setup', 'Wet':'Wet setup', 'Custom':'Custom'}

race = list(raceSettings) #race = ('F1 2020', 'F2 2020', 'F2 2019', 'classic')
weather_ = list(weatherType)

cars = ('All Cars','')

# State variables
weather = StringVar()
statusmsg = StringVar()
autoUse = BooleanVar()

#set row integer used for deciding what role a slider(scale) goes
ri = 0 

# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)

try:    #get steam install dir
    hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") #<PyHKEY:0x0000000000000094>
except:
    hkey = None
    messagebox.showerror("error","Can't find steam registry key")

try:
    steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    steam_path = steam_path[0]
except:
    messagebox.showerror("error","Can't find steam Install directory")
    steam_path = filedialog.askdirectory()

winreg.CloseKey(hkey)

try:    #get WorkshopFile install dir
    libraryfolder = steam_path + r"\steamapps\libraryfolders.vdf"
    with open(libraryfolder) as f: #"C:\Program Files (x86)\Steam\SteamApps\libraryfolders.vdf"
        libraries = [steam_path] #C:\Program Files (x86)\Steam
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
            re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
        for library in libraries:   #in      ['C:\\Program Files (x86)\\Steam', 'D:\\SteamLibrary', 'X:\\SteamLibrary']
            try:
                appmanifest = library + r"\steamapps\appmanifest_" + steamappid + ".ACF"
                with open(appmanifest) as ff: 
                    ff.read()
                    try:
                        WorkshopFile = library+"/steamapps/workshop/content/"+steamappid+"/"+ WorkshopID +"/ugcitemcontent.bin"
                        break
                    except:
                        messagebox.showerror("error", "Not Subscribed to steam workshop, Subscribe to: "+WorkshopUrl)
                ff.close()
            except:
                appmanifest = None
    f.close()
except:
    libraryfolder = None
    messagebox.showerror("error","Can't find steam libraries")


#grid the sliders 
def Scalegrid(scale):
    global ri #row index
    row = ri
    column = 2
    maxrows = 11
    if ri >= maxrows:
        row -= maxrows 
        column = 4
    scale.grid(row=row, column=column, columnspan=2, sticky='NSEW')#needs own line
    ri += 1

#remove ALL the sliders ,required if the race type changes(f1 , f2, etc)
def forgetScales(): 
    front_wing_Scale.grid_forget()
    front_wing_Scale.grid_forget()
    rear_wing_Scale.grid_forget()
    on_throttle_Scale.grid_forget()
    off_throttle_Scale.grid_forget()
    front_camber_Scale.grid_forget()
    rear_camber_Scale.grid_forget()
    front_toe_Scale.grid_forget()
    rear_toe_Scale.grid_forget()
    front_suspension_Scale.grid_forget()
    rear_suspension_Scale.grid_forget()
    front_antiroll_bar_Scale.grid_forget()
    rear_antiroll_bar_Scale.grid_forget()
    front_suspension_height_Scale.grid_forget()
    rear_suspension_height_Scale.grid_forget()
    brake_pressure_Scale.grid_forget()
    brake_bias_Scale.grid_forget()
    front_right_tyre_pressure_Scale.grid_forget()
    front_left_tyre_pressure_Scale.grid_forget()
    rear_right_tyre_pressure_Scale.grid_forget()
    rear_left_tyre_pressure_Scale.grid_forget()
    ballast_Scale.grid_forget()
    fuel_load_Scale.grid_forget()
    ramp_differential_Scale.grid_forget()

#grid the sliders that we can use for this race type (f1, f2, etc)
def gameModeScaleSettings(*args): 
    global ri

    race = raceBox.get()
    ri = 0
    if race == 'F1 2020':
        Scalegrid(front_wing_Scale)
        Scalegrid(rear_wing_Scale)
        Scalegrid(on_throttle_Scale)
        Scalegrid(off_throttle_Scale)

        Scalegrid(brake_pressure_Scale)
        Scalegrid(brake_bias_Scale)

        Scalegrid(fuel_load_Scale)

        Scalegrid(front_camber_Scale)
        Scalegrid(rear_camber_Scale)
        Scalegrid(front_toe_Scale)
        Scalegrid(rear_toe_Scale)

        Scalegrid(front_suspension_Scale)
        Scalegrid(rear_suspension_Scale)
        Scalegrid(front_antiroll_bar_Scale)
        Scalegrid(rear_antiroll_bar_Scale)
        Scalegrid(front_suspension_height_Scale)
        Scalegrid(rear_suspension_height_Scale)
        ri+= 1
        Scalegrid(front_right_tyre_pressure_Scale)
        Scalegrid(front_left_tyre_pressure_Scale)
        Scalegrid(rear_right_tyre_pressure_Scale)
        Scalegrid(rear_left_tyre_pressure_Scale)


    elif race == 'F2 2020' or race == 'F2 2019': #f2 2020 & f2 2019
        
        Scalegrid(front_wing_Scale)
        Scalegrid(rear_wing_Scale)
        ri+= 1
        Scalegrid(ramp_differential_Scale)
        ri+= 1
        Scalegrid(brake_bias_Scale)
        ri+= 1
        
        Scalegrid(front_camber_Scale)
        Scalegrid(rear_camber_Scale)
        Scalegrid(front_toe_Scale)
        Scalegrid(rear_toe_Scale)

        Scalegrid(front_suspension_Scale)
        Scalegrid(rear_suspension_Scale)
        Scalegrid(front_antiroll_bar_Scale)
        Scalegrid(rear_antiroll_bar_Scale)
        Scalegrid(front_suspension_height_Scale)
        Scalegrid(rear_suspension_height_Scale)
        ri+= 1
        Scalegrid(front_right_tyre_pressure_Scale)
        Scalegrid(front_left_tyre_pressure_Scale)
        Scalegrid(rear_right_tyre_pressure_Scale)
        Scalegrid(rear_left_tyre_pressure_Scale)

    elif race == 'classic':  #save to diffrent file location
        Scalegrid(front_wing_Scale)
        Scalegrid(rear_wing_Scale)
        Scalegrid(on_throttle_Scale)
        Scalegrid(off_throttle_Scale)

        Scalegrid(brake_pressure_Scale)
        Scalegrid(brake_bias_Scale)

        Scalegrid(fuel_load_Scale)
        
        Scalegrid(front_camber_Scale)
        Scalegrid(rear_camber_Scale)
        Scalegrid(front_toe_Scale)
        Scalegrid(rear_toe_Scale)

        Scalegrid(front_suspension_Scale)
        Scalegrid(rear_suspension_Scale)
        Scalegrid(front_antiroll_bar_Scale)
        Scalegrid(rear_antiroll_bar_Scale)
        Scalegrid(front_suspension_height_Scale)
        Scalegrid(rear_suspension_height_Scale)

        Scalegrid(ballast_Scale)

        Scalegrid(front_right_tyre_pressure_Scale)
        Scalegrid(front_left_tyre_pressure_Scale)
        Scalegrid(rear_right_tyre_pressure_Scale)
        Scalegrid(rear_left_tyre_pressure_Scale)

#set the current slider values
def setScale(setup):
    front_wing_Scale.set(setup[41])
    rear_wing_Scale.set(setup[44])
    on_throttle_Scale.set(setup[47])
    off_throttle_Scale.set(setup[50])
    front_camber_Scale.set(setup[53]) #-2,50
    rear_camber_Scale.set(setup[56])  #-1.00
    front_toe_Scale.set(setup[59]) #0.15
    rear_toe_Scale.set(setup[62])
    front_suspension_Scale.set(setup[65])
    rear_suspension_Scale.set(setup[68])
    front_suspension_height_Scale.set(setup[71])
    rear_suspension_height_Scale.set(setup[74])
    front_antiroll_bar_Scale.set(setup[77])
    rear_antiroll_bar_Scale.set(setup[80])
    brake_pressure_Scale.set(setup[83])
    brake_bias_Scale.set(setup[86])
    front_right_tyre_pressure_Scale.set(setup[89])
    front_left_tyre_pressure_Scale.set(setup[92])
    rear_right_tyre_pressure_Scale.set(setup[95])
    rear_left_tyre_pressure_Scale.set(setup[98])
    ballast_Scale.set(setup[101])
    fuel_load_Scale.set(setup[104])
    ramp_differential_Scale.set(setup[107])


# combobox command functions  
# comboxes need to remember previous selected track, as they become unselected.

# when race type changes; show new sliders and update the cars in carsbox  
def raceBoxSelected(*args):
    global lboxCountry
    forgetScales()
    gameModeScaleSettings() #show/hide sliders
    
    carsBox['values'] = raceSettings[raceBox.get()] 
    carsBox.current(0) #update carbox
    SelectTrack(lboxCountry)

def carsBoxSelected(*args):
    global lboxCountry
    SelectTrack(lboxCountry)

def weatherBoxSelected(*args):
    global lboxCountry
    SelectTrack(lboxCountry)

#packed setup file with the current slider-values  -return setup
def packSetup():
    setup = struct.pack(setupStructFormat, 
    b'F1CS', 0,1,0,32,0 ,7,                  #\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x07
    b'versionsi32', 0, 9,                     #\x00\x00\x00\x00\t
    b'save_names128', 20,                    #\x14      probably string length of next name
    b'All setups | scruffe', 7,              #\x07 
    b'team_idui16', 0,0,8,                   #\x00\x00\x08
    b'track_idui08',3,12,                    #\x03\x0c
    b'game_mode_idsi32',5,12,                #\x05\x00\x00\x00 \x0c
    b'weather_typebool',1,9,                 #\x01\t
    b'timestampui64',19,14,5,95,0,0,0,0,15,  #\x13\x0e\x05_\x00\x00\x00\x00\x0f
    b'game_setup_modeui08',0,10,              #\x00\n
    b'front_wingfp32', front_wing_Scale.get(), 9,
    b'rear_wingfp32', rear_wing_Scale.get(), 11,
    b'on_throttlefp32', on_throttle_Scale.get(), 12,
    b'off_throttlefp32', off_throttle_Scale.get(), 12,
    b'front_camberfp32', front_camber_Scale.get(), 11,
    b'rear_camberfp32', rear_camber_Scale.get(), 9,
    b'front_toefp32', front_toe_Scale.get(), 8,
    b'rear_toefp32', rear_toe_Scale.get(), 16,
    b'front_suspensionfp32', front_suspension_Scale.get(), 15, 
    b'rear_suspensionfp32', rear_suspension_Scale.get(), 23, 
    b'front_suspension_heightfp32', front_suspension_height_Scale.get(), 22,
    b'rear_suspension_heightfp32', rear_suspension_height_Scale.get(), 18,
    b'front_antiroll_barfp32', front_antiroll_bar_Scale.get(), 17,
    b'rear_antiroll_barfp32', rear_antiroll_bar_Scale.get(), 14,
    b'brake_pressurefp32', brake_pressure_Scale.get(), 10,
    b'brake_biasfp32', brake_bias_Scale.get(), 25,
    b'front_right_tyre_pressurefp32' , front_right_tyre_pressure_Scale.get(), 24,
    b'front_left_tyre_pressurefp32', front_left_tyre_pressure_Scale.get(), 24,
    b'rear_right_tyre_pressurefp32', rear_right_tyre_pressure_Scale.get(), 23,
    b'rear_left_tyre_pressurefp32', rear_left_tyre_pressure_Scale.get(), 7,
    b'ballastfp32', ballast_Scale.get(), 9,
    b'fuel_loadfp32', fuel_load_Scale.get(), 17,
    b'ramp_differentialfp32', ramp_differential_Scale.get(), 17,
    b'published_file_idui64', 31,174,162,128,0,0,0,0        # b'published_file_idui64\x1f\xae\xa2\x80\x00\x00\x00\x00'
    ) 
    
    return setup

#write packedsetup to dir
def writeSetup(filename):
    setup = packSetup()
    with open(filename, 'wb') as file:
        file.write(setup)
    file.close()    

#write to WorkshopFile
def Use(): 
    writeSetup(WorkshopFile)
    statusmsg.set("Loaded  "+ root.filename)

#write to both current file and workshop
def UseSave():
    writeSetup(root.filename)
    writeSetup(WorkshopFile)
    statusmsg.set("Saved Preset & loaded as "+ root.filename)

#write to current file
def Save( ): 
    writeSetup(root.filename)
    statusmsg.set("Saved as: " + root.filename)

#write to filedialogDir
def SaveAs(): 
    askedFilename =  filedialog.asksaveasfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
    writeSetup(askedFilename)
    statusmsg.set("Saved: " + askedFilename)

#open,unpack a setup.bin file and set sliders to files values          error if the file isnt a f1 2020 setup file
def Open(): 
    try:
        root.filename =  filedialog.askopenfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
        setupFile = open(root.filename, "rb")
        setup = struct.unpack(setupStructFormat, setupFile.read())
        statusmsg.set(" Opened (" + root.filename + ")")
        setScale(setup)
    except:
        messagebox.showerror("error","can't open")

#select the file to open, unpack the file, update sliders, if autoUse is checked;  write to workshopfile
def SelectTrack(country): 
    setupWeatherType = str(weatherType[weatherBox.get()])
    raceType = raceBox.get()
    carType = carsBox.get()
    setupType = weatherBox.get()
    circuit = tracks[country]
    root.filename = SetupDir + raceType +'/'+ carType +'/'+ setupType +'/'+ country  +".bin"
    setupFile = open(root.filename, "rb")
    setup = struct.unpack(setupStructFormat, setupFile.read())
    setScale(setup)
    if autoUse.get() == True:   
        Use()
    statusmsg.set(" %s | %s | (%s) %s [%s]" % (raceType, carType, country, circuit, setupWeatherType))

#update the scales after switching setup type
def chooseweatherType(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        country = countrynames[idx]
        SelectTrack(country)

#update config.json auto-use
def setAutoUseButton(*args):
    with open('config.json') as json_file: 
        config = json.load(json_file)     
    json_file.close()

    config['autoUseButton'] = autoUse.get()
    
    with open("config.json", "w") as json_file:
        json.dump(config, json_file, indent=4)
    json_file.close()

#create widgets
lbox = Listbox(c, 
    listvariable=cnames, 
    height=len(countrynames),
    bg=bg,
    fg=fg,
    highlightcolor="black",
    selectbackground="darkred",
    selectforeground="white")
lbox.selection_clear(1, last=None)
raceBox = Combobox(c,
    justify="center", 
    values=race, 
    state='disabled') #state= 'readonly' , 'disabled'
carsBox = Combobox(c,
    justify="center", 
    values=cars, 
    state='readonly') 
weatherBox = Combobox(c,
    justify="center", 
    values=weather_, 
    state='readonly') 
status = ttk.Label(c, 
    textvariable=statusmsg, 
    anchor=W)
autoUseTrackBox = ttk.Checkbutton(c, 
    text='Auto Use track', 
    variable=autoUse, 
    onvalue=True, 
    offvalue=False,
    command=setAutoUseButton)
separatorV = ttk.Separator(c,
    orient='vertical')

#create Button widgets
useButton = ttk.Button(
    c, 
    text="Use", 
    command=Use
    )
useSaveButton = ttk.Button(
    c,
    text="Save & Use", 
    command=UseSave
    )
saveButton = ttk.Button(
    c, 
    text="Save", 
    command=Save
    )
saveAsButton = ttk.Button(
    c, 
    text="Save As", 
    command=SaveAs
    )
openButton = ttk.Button(
    c, 
    text="Open", 
    command=Open
    )

# Grid all the widgets

lbox.grid(
    column=0, row=0, 
    rowspan=6, 
    sticky=(N,S,E,W))
raceBox.grid(
    column=0, row=6, sticky=W)
carsBox.grid(
    column=0, row=7, sticky=W)
weatherBox.grid(
    column=0, row=8, sticky=W)
autoUseTrackBox.grid(
    column=0, row=11, sticky=W, padx=10)

separatorV.grid(
    column=1, row=0, 
    rowspan=12, 
    sticky=(N,S,E,W))

#buttons
useButton.grid(
    column=0, row=50, sticky=NSEW)
#column spacer
useSaveButton.grid(
    column=2, row=50, sticky=NSEW)
saveButton.grid(
    column=3, row=50, sticky=NSEW)
saveAsButton.grid(
    column=4, row=50, sticky=NSEW)
openButton.grid(
    column=5, row=50, sticky=NSEW)

#statusbar
status.grid(
    column=0, row=60, columnspan=6, sticky=(W,E))

c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)


# Colorize alternating lines of the listbox
for i in range(0,len(countrynames),2):
    lbox.itemconfigure(i, background='#576366',fg=fg)

#create sliders(scale) widgets - return  scale
def MakeScale(from_ , to,  label, resolution=1):
    scale = Scale(
        c, 
        from_=from_, 
        to=to, 
        orient=HORIZONTAL, 
        label=label, 
        length=scale_length,
        relief=scale_relief, 
        bg=bg,
        fg=fg,
        troughcolor=bg,
        bd=3,
        activebackground=bg,
        highlightbackground=bg,
        resolution=resolution)
    return scale

#slidername, create slider (from_ , to,  label, resolution)
front_wing_Scale = MakeScale(1, 11,"Front wing")
rear_wing_Scale = MakeScale(1, 11, "Rear wing")
on_throttle_Scale = MakeScale(50, 100, "On throttle")
off_throttle_Scale = MakeScale(50, 100, "Off throttle")
front_camber_Scale = MakeScale(-3.5, -2.5, "Front camber", 0.1) 
rear_camber_Scale = MakeScale(-2, -1, "Rear camber", 0.1) 
front_toe_Scale = MakeScale(0.05, 0.15, "Front toe", 0.01) 
rear_toe_Scale = MakeScale(0.20, 0.50, "Rear toe", 0.03) #there is an offset
front_suspension_Scale = MakeScale(1, 11, "Front suspension")
rear_suspension_Scale = MakeScale(1, 11, "Rear suspension")
front_antiroll_bar_Scale = MakeScale(1, 11, "Front antiroll bar")
rear_antiroll_bar_Scale = MakeScale(1, 11, "Rear antiroll bar")

front_suspension_height_Scale = MakeScale(1, 11, "Front suspension height")
rear_suspension_height_Scale = MakeScale(1, 11, "Rear suspension height")
brake_pressure_Scale = MakeScale(50, 100, "Brake pressure")
brake_bias_Scale = MakeScale(70, 50, "Brake bias")
front_right_tyre_pressure_Scale = MakeScale(21, 25, "Front right tyre pressure", 0.4) 
front_left_tyre_pressure_Scale = MakeScale(21, 25, "Front left tyre pressure", 0.4) 
rear_right_tyre_pressure_Scale = MakeScale(19.5, 23.5, "Rear right tyre pressure", .4) 
rear_left_tyre_pressure_Scale = MakeScale(19.5, 23.5, "Rear left tyre pressure", 0.4) 
ballast_Scale = MakeScale(1, 11 , "Ballast")
fuel_load_Scale = MakeScale(5, 110, "Fuel load")
ramp_differential_Scale = MakeScale(70,100, "Ramp differential")



# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# weather being sent, so it doesn't stick around after we start doing
# other things.
lboxCountry = ""
def showTrackselection(*args):
    global lboxCountry
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        country = countrynames[idx]
        lboxCountry = country
        SelectTrack(country)
        
# Set event bindings for when the selection changes
lbox.bind('<<ListboxSelect>>', showTrackselection)
raceBox.bind("<<ComboboxSelected>>", raceBoxSelected)
carsBox.bind("<<ComboboxSelected>>", carsBoxSelected)
weatherBox.bind("<<ComboboxSelected>>", weatherBoxSelected)

# Set the starting state of the interface, including selecting the
# default weather to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> events are only
# fired when users makes a change, we explicitly call showTrackselection.
weather.set('Dry')
statusmsg.set('')
lbox.selection_set(0)

#set the autoUseTrackBox button if autoUse is enabled
with open('config.json') as json_file: 
    config = json.load(json_file)     
json_file.close()

if config['autoUseButton'] == True:
    autoUseTrackBox.invoke()

#Assigning ComboBox default Values
raceBox.current(0)
carsBox.current(0) 
weatherBox.current(0)
carsBox['values']=raceSettings[raceBox.get()] 

#create sliders
gameModeScaleSettings()
#Load track
showTrackselection()

root.mainloop()