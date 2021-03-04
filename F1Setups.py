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


F1SetupPath = pathlib.Path(__file__).parent.absolute()

root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(F1SetupPath)+'/pog.ico')

s = ttk.Style() #s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.tk.call('lappend', 'auto_path', str(F1SetupPath)) #'C:/Users/88/hello/awthemes-10.2.1/awthemes-10.2.1'
root.tk.call('package', 'require', 'awdark')
s.theme_use('awdark')

steamappid = "1080110" #f12020 steam id
WorkshopID = "2403338074" #f2 2404403390
#WorkshopFile = "D:/SteamLibrary/steamapps/workshop/content/1080110/"+ WorkshopID +"/ugcitemcontent.bin"
WorkshopUrl = "https://steamcommunity.com/sharedfiles/filedetails/?id="+ WorkshopID
SetupDir = str(F1SetupPath) + "/Setups/" #"c:\Users\88\hello\F1Setups/Setups/
setupStructFormat = '<4s5l1b 11sfb 13sb 20sb 11s3b 12s2b 16sfb 16s2b 13s9b 19s2b 14sfb13sfb15sfb16sfb16sfb15sfb13sfb12sfb20sfb19sfb27sfb26sfb22sfb21sfb18sfb14sfb29sfb28sfb28sfb27sfb11sfb13sfb21sfb21s8B'


bg = "#33393b"
fg = "white"
scale_length = "200" #length of all the sliders
scale_relief = "flat"

tracks = {
    "Abu Dhabi": "Yas Marina Circuit",
    "Australia": "Melbourne Grand Prix Circuit",
    "Austria": "Spielberg" ,
    "Azerbaijan": "Baku City Circuit",
    "Bahrain": "Bahrain International Circuit",
    "Bahrain Short": "Bahrain International Circuit (Short)",
    "Belgium": "Circuit De Spa-Francorchamps",
    "Brazil": "Autódromo José Carlos Pace",
    "Britain": "Silverstone Circuit",
    "Britain Short": "Silverstone Circuit (Short)",
    "Canada": "Circuit Gilles-Villeneuve",
    "China": "Shanghai International Circuit",
    "France": "Circuit Paul Ricard",
    "Hungary": "Hungaroring",
    "Italy": "Autodromo Nazionale Monza",
    "Japan": "Suzuka International Racing Course",
    "Japan Short": "Suzuka International Racing Course (Short)",
    "Monaco": "Circuit de Monaco",
    "México": "Autódromo Hermanos Rodríguez",
    "Russia": "Sochi Autodrom",
    "Singapore": "Marina Bay Street Circuit",
    "Spain": "Circuit de Barcelona-Catalunya",
    "The Netherlands": "Circuit Zandvoort",
    "USA": "Circuit of The Americas",
    "USA Short": "Circuit of The Americas (Short)",
    "Vietnam": "Hanoi Circuit"}

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
sentmsg = StringVar()
statusmsg = StringVar()
loadSystem = BooleanVar()

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
except:
    steam_path = None
    messagebox.showerror("error","Can't find steam Install directory")

winreg.CloseKey(hkey)


try:    #get WorkshopFile install dir
    libraryfolder = steam_path[0] + r"\steamapps\libraryfolders.vdf"
    with open(libraryfolder) as f: #"C:\Program Files (x86)\Steam\SteamApps\libraryfolders.vdf"
        libraries = [steam_path[0]] #C:\Program Files (x86)\Steam
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
                        open(WorkshopFile, "rb")
                        break
                    except:
                        messagebox.showerror("error", "Not Subscribed to steam workshop, Subscribe to: "+WorkshopUrl)
            except:
                appmanifest = None
except:
    libraryfolder = None
    messagebox.showerror("error","Can't find steam libraries")

#update the scales after switching setup type
def chooseweatherType(*args):
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        country = countrynames[idx]
        SelectTrack(country)

#create widgets

lbox = Listbox(c, listvariable=cnames, height=len(countrynames),bg=bg,fg=fg,highlightcolor="black",selectbackground="darkred",selectforeground="white")
lbox.selection_clear(1, last=None)
raceBox = Combobox(c,justify="center", values=race, state='disabled') #state= 'readonly' , 'disabled'
carsBox = Combobox(c,justify="center", values=cars, state='readonly') 
weatherBox = Combobox(c,justify="center", values=weather_, state='readonly') 
status = ttk.Label(c, textvariable=statusmsg, anchor=W)
check = ttk.Checkbutton(c, text='Auto Use', variable=loadSystem, onvalue=True, offvalue=False)
separatorV = ttk.Separator(c,orient='vertical')

# Grid all the widgets

lbox.grid(column=0, row=0, rowspan=6, sticky=(N,S,E,W))
raceBox.grid(column=0, row=6, sticky=W)
carsBox.grid(column=0, row=7, sticky=W)
weatherBox.grid(column=0, row=8, sticky=W)
check.grid(column=0, row=11,sticky=W,padx=10)
status.grid(column=0, row=60, columnspan=6, sticky=(W,E))
separatorV.grid(column=1, row=0, rowspan=12, sticky=(N,S,E,W))
c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(5, weight=1)


# Colorize alternating lines of the listbox
for i in range(0,len(countrynames),2):
    lbox.itemconfigure(i, background='#576366',fg=fg)


#create slider widgets
front_wing_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Front wing", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg)
rear_wing_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Rear wing", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
on_throttle_Scale = Scale(c, from_=50, to=100,orient=HORIZONTAL, label="On throttle", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
off_throttle_Scale = Scale(c, from_=50, to=100,orient=HORIZONTAL, label="Off throttle", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
front_camber_Scale = Scale(c, from_=-3.5, to=-2.5,orient=HORIZONTAL, label="Front camber", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.1) 
rear_camber_Scale = Scale(c, from_=-2, to=-1,orient=HORIZONTAL, label="Rear camber", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.1) 
front_toe_Scale = Scale(c, from_=0.05, to=0.15,orient=HORIZONTAL, label="Front toe", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.01) 
rear_toe_Scale = Scale(c, from_=0.20, to=0.50,orient=HORIZONTAL, label="Rear toe", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.03) #there is an offset
front_suspension_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Front suspension", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
rear_suspension_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Rear suspension", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
front_antiroll_bar_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Front antiroll bar", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
rear_antiroll_bar_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Rear antiroll bar", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 

front_suspension_height_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Front suspension height", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
rear_suspension_height_Scale = Scale(c, from_=1, to=11,orient=HORIZONTAL, label="Rear suspension height", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
brake_pressure_Scale = Scale(c, from_=50, to=100,orient=HORIZONTAL, label="Brake pressure", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
brake_bias_Scale = Scale(c, from_=70, to=50,orient=HORIZONTAL, label="Brake bias", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
front_right_tyre_pressure_Scale = Scale(c, from_=21, to=25,orient=HORIZONTAL, label="Front right tyre pressure", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.4) 
front_left_tyre_pressure_Scale = Scale(c, from_=21, to=25,orient=HORIZONTAL, label="Front left tyre pressure", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.4) 
rear_right_tyre_pressure_Scale = Scale(c, from_=19.5, to=23.5,orient=HORIZONTAL, label="Rear right tyre pressure", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg, resolution=0.4) 
rear_left_tyre_pressure_Scale = Scale(c, from_=19.5, to=23.5,orient=HORIZONTAL, label="Rear left tyre pressure", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg,resolution=0.4) 
ballast_Scale = Scale(c, from_=1, to=11 ,orient=HORIZONTAL, label="Ballast", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
fuel_load_Scale = Scale(c, from_=5, to=110,orient=HORIZONTAL, label="Fuel load", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 
ramp_differential_Scale = Scale(c,orient=HORIZONTAL, label="Ramp differential", length=scale_length,relief=scale_relief, bg=bg,fg=fg,troughcolor=bg,bd=3,activebackground=bg,highlightbackground=bg) 

ri = 0 #set row integer
def Scalegrid(scale):
    global ri
    row = ri
    column = 2
    maxrows = 11
    if ri >= maxrows:
        row -= maxrows 
        column = 4
    scale.grid(row=row, column=column, columnspan=2,sticky='NSEW')#needs own line
    ri += 1
def forgetScales(): #remove the sliders 
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
def gameModeScaleSettings(*args): #only grid the sliders that we can use for this mode
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
    
def raceBoxSelected(*args):
    global trackremember
    forgetScales()
    gameModeScaleSettings() #show/hide sliders
    
    carsBox['values'] = raceSettings[raceBox.get()] 
    carsBox.current(0) #update carbox
    SelectTrack(trackremember)
def carsBoxSelected(*args):
    global trackremember
    SelectTrack(trackremember)
def weatherBoxSelected(*args):
    global trackremember
    SelectTrack(trackremember)

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

def write():
    
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
    
    with open(root.filename, 'wb') as file:
        file.write(setup)
    file.close()



def Use(): #save the setup to a default file
    saveFilename = root.filename #lets you save as track name after using
    root.filename = WorkshopFile
    write()
    root.filename = saveFilename
    statusmsg.set("Loaded  "+ root.filename)

def UseSave():
    write()
    root.filename = WorkshopFile
    write()
    statusmsg.set("Saved Preset & loaded as "+ root.filename)

def Save( ): #save the setup to a default file & overwrite the track save
    write()
    statusmsg.set("Saved as: " + root.filename)

def SaveAs(): #save the setup to a default file & save whereever you want
    root.filename =  filedialog.asksaveasfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
    write()
    statusmsg.set("Saved: " + root.filename)

def Open(): #open a setup fle
    root.filename =  filedialog.askopenfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
    #error if the file isnt a f1 2020 setup file
    setupFile = open(root.filename, "rb")
    setup = struct.unpack(setupStructFormat, setupFile.read())
    name = setup[15]
    statusmsg.set(str(name) + " Loaded (" + root.filename + ")")
    setScale(setup)

def SelectTrack(country): #buttons will use this to load the track into the program
    #error if the file isnt a f1 2020 setup file
    setupWeatherType = str(weatherType[weatherBox.get()])
    raceType = raceBox.get()
    carType = carsBox.get()
    setupType = weatherBox.get()
    root.filename = SetupDir + raceType +'/'+ carType +'/'+ setupType +'/'+ country  +".bin"
    
    setupFile = open(root.filename, "rb")
    setup = struct.unpack(setupStructFormat, setupFile.read())
    circuit = tracks[country]
    setScale(setup)
    if loadSystem.get() == True: #if checked the setup will automaticly write to the default file
        Use()
    statusmsg.set(" %s | %s | (%s) %s [%s]" % (raceType, carType, country, circuit, setupWeatherType))

ttk.Button(c, text="Use", command=Use).grid(column=0, row=50, sticky=NSEW)
#column spacer
ttk.Button(c, text="Save & Use", command=UseSave).grid(column=2, row=50, sticky=NSEW)
ttk.Button(c, text="Save", command=Save).grid(column=3, row=50, sticky=NSEW)
ttk.Button(c, text="Save As", command=SaveAs).grid(column=4, row=50, sticky=NSEW)
ttk.Button(c, text="Open", command=Open).grid(column=5, row=50, sticky=NSEW)

# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# weather being sent, so it doesn't stick around after we start doing
# other things.
trackremember = ""
def showTrackselection(*args):
    global trackremember
    idxs = lbox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        country = countrynames[idx]
        trackremember = country
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
sentmsg.set('')
statusmsg.set('')
lbox.selection_set(0)

#Assigning ComboBox Values
raceBox.current(0)
carsBox.current(0) 
weatherBox.current(0)
carsBox['values']=raceSettings[raceBox.get()] 

#create sliders
gameModeScaleSettings()
#Load track
showTrackselection()

root.mainloop()