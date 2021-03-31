#from tkinter import *
from tkinter import ttk
from tkinter import Tk, Entry, EW, Scale, HORIZONTAL, DISABLED, Label, NSEW, Button, messagebox, filedialog,DoubleVar,IntVar, StringVar,BooleanVar,N,W,E,S,Listbox
from tkinter.ttk import Combobox
from tkinter.filedialog import asksaveasfile
import struct
import webbrowser
import sys
import winreg
import re
import pathlib
import os
import json

F1SetupPath = pathlib.Path(__file__).parent.absolute()
root = Tk()
root.title('F1 Setup editor')
root.iconbitmap(str(F1SetupPath)+'/pog.ico')

with open('config.json') as json_file: 
    config = json.load(json_file)     
json_file.close()

with open('tracks.json', encoding='utf-8') as json_file: 
    tracks = json.load(json_file) 
json_file.close()

theme = config['theme']
s = ttk.Style() #s.theme_names('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
root.tk.call('lappend', 'auto_path', str(F1SetupPath)) 
root.tk.call('package', 'require', 'awdark')
s.theme_use(theme)


SetupDir = str(F1SetupPath) + "/Setups/" 

setupStructPackingFormat = '<4s5l1b 11sfb 13sb 20sb 11s3b 12s2b 16sfb 16s2b 13s9b 19s2b 14sfb13sfb15sfb16sfb16sfb15sfb13sfb12sfb20sfb19sfb27sfb26sfb22sfb21sfb18sfb14sfb29sfb28sfb28sfb27sfb11sfb13sfb21sfb21s8B'

tipURL = "https://paypal.me/valar"

f1_2020_steamID = "1080110"
scruffe_WorkshopID = "2403338074" #f2 2404403390
scruffe_WorkshopUrl = "https://steamcommunity.com/sharedfiles/filedetails/?id="+ scruffe_WorkshopID

bg = "#33393b" #backgroundcolor
fg = "white" #forgroundcolor


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


weatherTypes = { 'Dry':'Dry setup', 'Wet':'Wet setup', 'Custom':'Custom'}


cars = ('All Cars','')
presetsetups = { 
    'Preset 1':'Maximum Downforce',
    'Preset 2':'Increased Downforce', 
    'Preset 3':'Balanced/Default',
    'Preset 4':'Increased Topspeed',
    'Preset 5':'Maximum Topspeed'}

#weather = StringVar()
statusmsg = StringVar()
autoUseChanges = BooleanVar()
autoSaveChanges = BooleanVar()
autoUse = BooleanVar()

 



# precision limiter
#https://stackoverflow.com/questions/54186639/tkinter-control-ttk-scales-increment-as-with-tk-scale-and-a-tk-doublevar
class Limiter(ttk.Scale):
    """ ttk.Scale sublass that limits the precision of values. """

    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')  # Remove non-std kwarg.
        self.chain = kwargs.pop('command', lambda *a: None)  # Save if present.
        super(Limiter, self).__init__(*args, command=self._value_changed, **kwargs)

    def _value_changed(self, newvalue):
        newvalue = round(float(newvalue), self.precision)
        if self.precision == 0:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), (int(newvalue)))
        else:
            self.winfo_toplevel().globalsetvar(self.cget('variable'), (newvalue))
        self.chain(newvalue)  # Call user specified function.




def setConfig(key, value):
    config[key] = value
    with open("config.json", "w") as json_file:
        json.dump(config, json_file, indent=4)
    json_file.close()

def setSteamPath():
    try:    
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam") #<PyHKEY:0x0000000000000094>
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
        steam_path = steam_path[0]
        winreg.CloseKey(hkey)
    except:
        messagebox.showerror("error","Can't find steam Install directory")
        steam_path = filedialog.askdirectory()   #manual entry
    setConfig('steam_path', steam_path)

def getSteamPath():
    if not os.path.isdir(config['steam_path']):
        setSteamPath()
    return config['steam_path']


def setWorkshop_dir():  
    steam_path = getSteamPath() 
    libraryfolders_data = steam_path + r"\steamapps\libraryfolders.vdf"
    with open(libraryfolders_data) as f: 
        libraries = [steam_path]
        lf = f.read()
        libraries.extend([fn.replace("\\\\", "\\") for fn in
            re.findall(r'^\s*"\d*"\s*"([^"]*)"', lf, re.MULTILINE)])
        for library in libraries:   
            appmanifest = library + r"\steamapps\appmanifest_" + f1_2020_steamID + ".ACF"
            if os.path.isfile(appmanifest):
                with open(appmanifest) as ff: 
                    ff.read()
                    WorkshopFile = library+"/steamapps/workshop/content/"+f1_2020_steamID+"/"+ scruffe_WorkshopID +"/ugcitemcontent.bin"
                    if os.path.isfile(WorkshopFile):
                        setConfig('WorkshopFile', WorkshopFile)
                    else:
                        messagebox.showerror("error", "Not Subscribed to steam workshop, Subscribe to: "+ scruffe_WorkshopUrl)
                        OpenUrl(scruffe_WorkshopUrl)
                ff.close()
    f.close()


def getWorkshop_dir():
    if not os.path.isfile(config['WorkshopFile']):
        setWorkshop_dir()
    return config['WorkshopFile']


def OpenUrl(url):
    webbrowser.open_new(url)

#grid the sliders that we can use for this race type (f1, f2, etc)
def gameModeScaleSettings(*args): 
    race = raceBox.get()
    if race == 'F1 2020':
        ballast_Scale.config(state='disabled')
        ramp_differential_Scale.config(state='disabled')

        on_throttle_Scale.config(state='enabled')
        off_throttle_Scale.config(state='enabled')
        brake_pressure_Scale.config(state='enabled')
        fuel_load_Scale.config(state='enabled')
        
    elif race == 'F2 2020' or race == 'F2 2019': #f2 2020 & f2 2019
        ballast_Scale.config(state='enabled')
        ramp_differential_Scale.config(state='enabled')

        on_throttle_Scale.config(state='disabled')
        off_throttle_Scale.config(state='disabled')
        brake_pressure_Scale.config(state='disabled')
        fuel_load_Scale.config(state='disabled')

    elif race == 'classic':  #save to diffrent file location
        ballast_Scale.config(state='enabled')
        ramp_differential_Scale.config(state='disabled')

        on_throttle_Scale.config(state='enabled')
        off_throttle_Scale.config(state='enabled')
        brake_pressure_Scale.config(state='enabled')
        fuel_load_Scale.config(state='enabled')

#Translates the 10 steps in sliders to actual values for/from the setup files
def setSliderOffset(value, offset, step , res=1):
    product = round(value - offset,  res)
    pruduct = round(product / step , res )
    return pruduct
def getSliderOffset(value, offset, step , res=1):
    multiplier =  round(value * step - step, res)
    product = round(offset + multiplier, res)
    return product

def SetSliders(setup):
    front_wing_Scale.set(setup[41])
    rear_wing_Scale.set(setup[44])
    on_throttle_Scale.set(setup[47])
    off_throttle_Scale.set(setup[50])

    front_camber_Scale.set(setSliderOffset(setup[53], -3.5, 0.1))
    rear_camber_Scale.set(setSliderOffset(setup[56], -2, 0.1))
    front_toe_Scale.set(setSliderOffset(setup[59], 0.05, 0.01, 2))
    rear_toe_Scale.set(setSliderOffset(setup[62], 0.20, 0.03, 2))

    front_suspension_Scale.set(setup[65])
    rear_suspension_Scale.set(setup[68])
    front_suspension_height_Scale.set(setup[71])
    rear_suspension_height_Scale.set(setup[74])
    front_antiroll_bar_Scale.set(setup[77])
    rear_antiroll_bar_Scale.set(setup[80])
    brake_pressure_Scale.set(setup[83])
    brake_bias_Scale.set(setup[86])

    front_right_tyre_pressure_Scale.set(setSliderOffset(setup[89], 21, 0.4))
    front_left_tyre_pressure_Scale.set(setSliderOffset(setup[92], 21, 0.4))
    rear_right_tyre_pressure_Scale.set(setSliderOffset(setup[95], 19.5, 0.4))
    rear_left_tyre_pressure_Scale.set(setSliderOffset(setup[98], 19.5, 0.4))

    ballast_Scale.set(setup[101])
    fuel_load_Scale.set(setup[104])
    ramp_differential_Scale.set(setup[107])


# combobox command functions  
# comboxes need to remember previous selected track, as they become unselected.

# when race type changes; show new sliders and update the cars in carsbox  
def raceBoxSelected(*args):
    global currentTrack
    gameModeScaleSettings() #show/hide sliders
    
    carsBox['values'] = raceSettings[raceBox.get()] 
    carsBox.current(0) #update carbox
    SelectTrack(currentTrack)

def boxSelected(*args):
    global currentTrack

    trackList = getList(tracks)
    trackBox.selection_set(trackList.index(currentTrack))

def getList(dict):
        return [*dict]

def getTrackId():
    global currentTrack                                                  #currently selected track
    tracksSeason = {
        "Australia": "Melbourne Grand Prix Circuit",
        "France": "Circuit Paul Ricard",
        "China": "Shanghai International Circuit",
        "Bahrain": "Bahrain International Circuit",
        "Spain": "Circuit de Barcelona-Catalunya",
        "Monaco": "Circuit de Monaco",
        "Canada": "Circuit Gilles-Villeneuve",
        "Britain": "Silverstone Circuit",
        "Hockenheim": "ITS NOT EVEN SHIPPED",
        "Hungary": "Hungaroring",
        "Belgium": "Circuit De Spa-Francorchamps",
        "Italy": "Autodromo Nazionale Monza",
        "Singapore": "Marina Bay Street Circuit",
        "Japan": "Suzuka International Racing Course",
        "Abu Dhabi": "Yas Marina Circuit",
        "USA": "Circuit of The Americas",
        "Brazil": "Autódromo José Carlos Pace",
        "Austria": "Spielberg" ,
        "Russia": "Sochi Autodrom",
        "México": "Autódromo Hermanos Rodríguez",
        "Azerbaijan": "Baku City Circuit",
        "Bahrain Short": "Bahrain International Circuit (Short)",
        "Britain Short": "Silverstone Circuit (Short)",
        "USA Short": "Circuit of The Americas (Short)",
        "Japan Short": "Suzuka International Racing Course (Short)",
        "Vietnam": "Hanoi Circuit",
        "The Netherlands": "Circuit Zandvoort"
    }
    
    trackList = getList(tracksSeason)
    track_id = trackList.index(currentTrack)
    return track_id
def getWeatherId():
    weather = weatherBox.get()
    if weather == "Wet":
        return 0
    else:
        return 1
def getTeamId():
    teamIDs = [                                #https://forums.codemasters.com/topic/50942-f1-2020-udp-specification/
        "Mercedes",
        "Ferrari",
        "Red Bull",
        "Williams",
        "Racing Point",
        "Renault",
        "AlphaTauri",
        "Haas",
        "McLaren",
        "Alfa Romeo"
        ]
    team = carsBox.get()
    if team == "All Cars":
        return 41 #multiplayer car
    else:
        return teamIDs.index(team)

#packed setup file with the current slider-values  -return setup
def packSetup():
    #ui08  |Unsigned 8-bit integer
    #i08   |Signed 8-bit integer
    #fp32   |Floating point (32-bit)

    #all vars have a check value at the end, i have no idea what they do. Remove them and the game crashes. ¯\_(ツ)_/¯
    setup = struct.pack(setupStructPackingFormat, 
    b'F1CS', 0,1,0,32,0 ,7,                  #\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x07
    b'versionsi32', 0, 9,                     #\x00\x00\x00\x00\t
    b'save_names128', 20,                    #\x14      probably string length of next name
    b'All setups | scruffe', 7,              #\x07 
    b'team_idui16', getTeamId(),0,8,                   #\x00\x00\x08
    b'track_idui08', getTrackId(),12,                    #\x03\x0c
    b'game_mode_idsi32',5,12,                #\x05\x00\x00\x00 \x0c
    b'weather_typebool',getWeatherId(),9,                 #\x01\t
    b'timestampui64',19,14,5,95,0,0,0,0,15,  #\x13\x0e\x05_\x00\x00\x00\x00\x0f
    b'game_setup_modeui08',0,10,              #\x00\n
    b'front_wingfp32', front_wing_Scale.get(), 9,
    b'rear_wingfp32', rear_wing_Scale.get(), 11,
    b'on_throttlefp32', on_throttle_Scale.get(), 12,
    b'off_throttlefp32', off_throttle_Scale.get(), 12,
    b'front_camberfp32', getSliderOffset(front_camber_Scale.get(), -3.5, 0.1) , 11,
    b'rear_camberfp32', getSliderOffset(rear_camber_Scale.get(), -2, 0.1), 9,
    b'front_toefp32', getSliderOffset(front_toe_Scale.get(), 0.05, 0.01, 2), 8,
    b'rear_toefp32', getSliderOffset(rear_toe_Scale.get(), 0.20, 0.03, 2), 16,
    b'front_suspensionfp32', front_suspension_Scale.get(), 15, 
    b'rear_suspensionfp32', rear_suspension_Scale.get(), 23, 
    b'front_suspension_heightfp32', front_suspension_height_Scale.get(), 22,
    b'rear_suspension_heightfp32', rear_suspension_height_Scale.get(), 18,
    b'front_antiroll_barfp32', front_antiroll_bar_Scale.get(), 17,
    b'rear_antiroll_barfp32', rear_antiroll_bar_Scale.get(), 14,
    b'brake_pressurefp32', brake_pressure_Scale.get(), 10,
    b'brake_biasfp32', brake_bias_Scale.get(), 25,
    b'front_right_tyre_pressurefp32' , getSliderOffset(front_right_tyre_pressure_Scale.get(), 21, 0.4), 24,
    b'front_left_tyre_pressurefp32', getSliderOffset(front_left_tyre_pressure_Scale.get(), 21, 0.4), 24,
    b'rear_right_tyre_pressurefp32', getSliderOffset(rear_right_tyre_pressure_Scale.get(), 19.5, 0.4), 23,
    b'rear_left_tyre_pressurefp32', getSliderOffset(rear_left_tyre_pressure_Scale.get(), 19.5, 0.4), 7,
    b'ballastfp32', ballast_Scale.get(), 9,
    b'fuel_loadfp32', fuel_load_Scale.get(), 17,
    b'ramp_differentialfp32', ramp_differential_Scale.get(), 17,
    b'published_file_idui64', 31,174,162,128,0,0,0,0        # b'published_file_idui64\x1f\xae\xa2\x80\x00\x00\x00\x00' 
    ) 
    
    return setup

def Write_Setup(filename):
    setup = packSetup()
    with open(filename, 'wb') as file:
        file.write(setup)
    file.close()    

def Use_Setup(): 
    WorkshopFile = getWorkshop_dir()
    Write_Setup(WorkshopFile)
    statusmsg.set("Using current setup")

def Save_Setup(): 
    Write_Setup(root.filename)
    statusmsg.set("Saved as: " + root.filename)

def UseSave_Setup():
    Use_Setup()
    Save_Setup()

def SaveAs_Setup(): 
    askedFilename =  filedialog.asksaveasfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
    Write_Setup(askedFilename)
    statusmsg.set("Saved: " + askedFilename)

def Open_Setup(): 
    try:
        root.filename =  filedialog.askopenfilename(initialdir = F1SetupPath,title = "Select file",filetypes = (("bin files","*.bin"),("all files","*.*")))
        setupFile = open(root.filename, "rb")
        setup = struct.unpack(setupStructPackingFormat, setupFile.read())
        statusmsg.set(" Opened (" + root.filename + ")")
        SetSliders(setup)
    except:
        messagebox.showerror("error","can't open")

def loadSetupFile(path):
    f = open(path, "rb")
    setup = struct.unpack(setupStructPackingFormat, f.read())
    f.close()
    SetSliders(setup)
    if autoUse.get() == True:   
        Use_Setup()

def makeDir(path):
    access_rights = 0o755
    if os.path.isdir(path) == False:
        try:
            os.makedirs(path, access_rights)
        except OSError:
            print ("Creation of the directory %s failed" % path)

def makeFile():
    global currentTrack
    race = raceBox.get()
    car = carsBox.get()
    weather = weatherBox.get()

    path = SetupDir + race +'/'+ car +'/'+ weather +'/'
    
    makeDir(path)
    if config['defaultsetups'] == "Preset":
        presetFile = SetupDir + "Presets/Preset 3.bin" 
    else:
        presetFile = SetupDir + race +'/'+ config['defaultsetups'] +'/'+ weather +'/'+ currentTrack  +".bin"
    loadSetupFile(presetFile)
    Write_Setup(root.filename)

#select the file to open, unpack the file, update sliders, if autoUse is checked;  write to workshopfile
def SelectTrack(country): 
    race = raceBox.get()
    car = carsBox.get()
    weather = weatherBox.get()
    root.filename = SetupDir + race +'/'+ car +'/'+ weather +'/'+ country  +".bin"

    if os.path.isfile(root.filename) == False:
        makeFile()

    loadSetupFile(root.filename)
    statusmsg.set(" %s | %s | (%s) %s [%s]" % (race, car, country, tracks[country], weatherTypes[weather]))

def highlightTrack(): #keep the trackname highlighted when you lose focus
    global currentTrack
    trackList = getList(tracks)
    trackBox.selection_set(trackList.index(currentTrack))



# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N,W,E,S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0,weight=1)


sliderFrame = ttk.LabelFrame(
    c, 
    text = "Setup",
    labelanchor='nw',
    padding = 5
    )
sliderFrame.grid(
    row=0,
    rowspan=15,
    column=2,
    columnspan=5)

#create widgets
trackBox = Listbox(
    c, 
    listvariable=cnames, 
    height=len(countrynames),
    bg=bg,
    fg=fg,
    highlightcolor="black",
    selectbackground="darkred",
    selectforeground="white")
trackBox.selection_clear(1, last=None)
raceBox = Combobox(c,
    justify="center", 
    values=list(raceSettings), 
    state='disabled') #state= 'readonly' , 'disabled'
carsBox = Combobox(c,
    justify="center", 
    values=cars, 
    state='readonly') 
weatherBox = Combobox(c,
    justify="center", 
    values=list(weatherTypes), 
    state='readonly') 

presetBox = Combobox(c,
    justify="center", 
    values=list(presetsetups.values()), 
    state='readonly') 



status = ttk.Label(c, 
    textvariable=statusmsg, 
    anchor=W)

autoUseChangesBox = ttk.Checkbutton(c, 
    text='Auto Use Changes', 
    variable=autoUseChanges, 
    onvalue=True, 
    offvalue=False,
    command= lambda: setConfig('autoUseChanges',autoUseChanges.get()))
autoSaveChangesBox = ttk.Checkbutton(c, 
    text='Auto Save Changes', 
    variable=autoSaveChanges, 
    onvalue=True, 
    offvalue=False,
    command= lambda: setConfig('autoSaveChanges',autoSaveChanges.get()))
autoUseTrackBox = ttk.Checkbutton(c, 
    text='Auto Use track', 
    variable=autoUse, 
    onvalue=True, 
    offvalue=False,
    command= lambda: setConfig('autoUseButton',autoUse.get()))

#separatorV = ttk.Separator(c,
#    orient='vertical')

#create Button widgets


useButton = ttk.Button(
    c, 
    text="Use", 
    command=Use_Setup
    )
useSaveButton = ttk.Button(
    c,
    text="Save & Use", 
    command=UseSave_Setup
    )
saveButton = ttk.Button(
    c, 
    text="Save", 
    command=Save_Setup
    )
saveAsButton = ttk.Button(
    c, 
    text="Save As", 
    command=SaveAs_Setup
    )
openButton = ttk.Button(
    c, 
    text="Open", 
    command=Open_Setup
    )

#create tipURL widget
tipBtn = ttk.Button(
    c, 
    text="Tip?", 
    command=lambda: OpenUrl(tipURL)
    )




root.ri = 1
#create & grid sliders(scale) widgets - return  scale
def MakeScale(from_ , to, text,  step=0 , offset=1, res=1):
    row = root.ri
    root.ri += 1

    separator = ttk.Separator(sliderFrame)
    
    #create emptyspace every 2
    if (row % 3) == 0:
        ttk.Label(
            sliderFrame, 
            anchor=W).grid(row=row)
        row += 1
        root.ri += 1

    input_var = DoubleVar(value=0.)
    column =2
    rowspan = 1
    sticky = 'NSEW'

    input_var = IntVar()

    scale = Limiter(
        sliderFrame, 
        from_=from_, 
        to=to, 
        orient=HORIZONTAL,
        length=200,
        variable=input_var,
        precision=0 ##
        )
    scaleTxt = ttk.Label(
        sliderFrame, 
        text=text, 
        anchor=W)
    scaleNr = ttk.Label(
            sliderFrame, 
            textvariable = input_var, 
            anchor=E,
            width=5)
    
    if step != 0:  
        def update_other_label(name1, name2, mode):
            value = input_var.get()
            product = getSliderOffset(value, offset, step, res)            

            input_var_mult.set(product)
        input_var.trace("w", update_other_label)
        input_var_mult = DoubleVar()
        
        scaleNr.config(textvariable = input_var_mult)
    
    
    separator.grid(row=row)
    scaleTxt.grid(row=row, column=column, columnspan=1, rowspan=rowspan, sticky=sticky)
    scale.grid(row=row, column=column+1, columnspan=2, rowspan=rowspan, sticky=sticky)
    scaleNr.grid(row=row, column=column+4, columnspan=1, rowspan=rowspan, sticky=sticky)
    
    
    return scale

front_wing_Scale = MakeScale(1, 11,"Front wing")
rear_wing_Scale = MakeScale(1, 11, "Rear wing")
on_throttle_Scale = MakeScale(50, 100, "On throttle")
off_throttle_Scale = MakeScale(50, 100, "Off throttle")
front_camber_Scale = MakeScale(1, 11, "Front camber", 0.1, -3.5)
rear_camber_Scale = MakeScale(1, 11, "Rear camber", 0.1, -2) 
front_toe_Scale = MakeScale(1, 11, "Front toe", 0.01, 0.05, 2)
rear_toe_Scale = MakeScale(1, 11, "Rear toe", 0.03, 0.20, 2) #there is an offset
front_suspension_Scale = MakeScale(1, 11, "Front suspension")
rear_suspension_Scale = MakeScale(1, 11, "Rear suspension")
front_antiroll_bar_Scale = MakeScale(1, 11, "Front antiroll bar")
rear_antiroll_bar_Scale = MakeScale(1, 11, "Rear antiroll bar")

front_suspension_height_Scale = MakeScale(1, 11, "Front suspension height")
rear_suspension_height_Scale = MakeScale(1, 11, "Rear suspension height")
brake_pressure_Scale = MakeScale(50, 100, "Brake pressure")
brake_bias_Scale = MakeScale(70, 50, "Brake bias")
front_right_tyre_pressure_Scale = MakeScale(1, 11, "Front right tyre pressure", .4, 21)#, 0.4) 
front_left_tyre_pressure_Scale = MakeScale(1, 11, "Front left tyre pressure", .4, 21) 
rear_right_tyre_pressure_Scale = MakeScale(1, 11, "Rear right tyre pressure", .4, 19.5) 
rear_left_tyre_pressure_Scale = MakeScale(1, 11, "Rear left tyre pressure", .4, 19.5) 
ballast_Scale = MakeScale(1, 11 , "Ballast")
ramp_differential_Scale = MakeScale(70,100, "Ramp differential")
fuel_load_Scale = MakeScale(5, 110, "Fuel load")

#test = MakeScale(1, 11, "test",.4 , 21)
# Grid all the widgets

trackBox.grid(
    column=0, row=0, 
    rowspan=3, 
    sticky=(N,S,E,W))
raceBox.grid(
    column=0, row=3, sticky=W)
carsBox.grid(
    column=0, row=4, sticky=W)
weatherBox.grid(
    column=0, row=5, sticky=W)

presetBox.grid(
    column=0, row=6, sticky=W)

autoUseChangesBox.grid(
    column=0, row=12, sticky=W, padx=10)
autoSaveChangesBox.grid(
    column=0, row=13, sticky=W, padx=10)
autoUseTrackBox.grid(
    column=0, row=14, sticky=W, padx=10)
#separatorV.grid(
#    column=1, row=0, 
#    rowspan=33, 
#    sticky=(N,S,E,W))

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
tipBtn.grid(column=6, row=50, sticky=NSEW)
#statusbar
status.grid(
    column=0, row=60, columnspan=6, sticky=(W,E))

c.grid_columnconfigure(0, weight=1)
c.grid_rowconfigure(11, weight=1)


def tracksBackgroundColor():
    for i in range(0,len(countrynames),2):
        trackBox.itemconfigure(i, background='#576366',fg=fg)



# Called when the selection in the listbox changes; figure out
# which country is currently selected, and then lookup its country
# code, and from that, its population.  Update the status message
# with the new population.  As well, clear the message about the
# weather being sent, so it doesn't stick around after we start doing
# other things.
currentTrack = ""
def showTrackselection(*args):
    global currentTrack
    idxs = trackBox.curselection()
    if len(idxs)==1:
        idx = int(idxs[0])
        country = countrynames[idx]
        currentTrack = country
        SelectTrack(country)
        
def SliderEvent(*args):
    autoUseChanges = config['autoUseChanges']
    autoSaveChanges = config['autoSaveChanges']
    if autoUseChanges == True and autoSaveChanges == True:
        UseSave_Setup()
        return
    if autoUseChanges == True:
        Use_Setup()
    if autoSaveChanges == True:
        Save_Setup()




def presetBoxSelected(*args):
    
    nr = str(presetBox.current() + 1) 
    name = "Preset " + nr + ".bin"
    path = SetupDir + "Presets/" + name
    loadSetupFile(path)
    
    statusmsg.set(" Loaded (" + presetBox.get() + ")")
    presetBox.set("Load Preset")
    


# Set event bindings for when the selection changes
trackBox.bind('<<ListboxSelect>>', showTrackselection)
raceBox.bind("<<ComboboxSelected>>", raceBoxSelected)
carsBox.bind("<<ComboboxSelected>>", boxSelected)
weatherBox.bind("<<ComboboxSelected>>", boxSelected)
presetBox.bind("<<ComboboxSelected>>", presetBoxSelected)


#slider event bindings
front_wing_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_wing_Scale.bind("<ButtonRelease-1>", SliderEvent)
on_throttle_Scale.bind("<ButtonRelease-1>", SliderEvent)
off_throttle_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_camber_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_camber_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_toe_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_toe_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_suspension_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_suspension_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_antiroll_bar_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_antiroll_bar_Scale.bind("<ButtonRelease-1>", SliderEvent)

front_suspension_height_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_suspension_height_Scale.bind("<ButtonRelease-1>", SliderEvent)
brake_pressure_Scale.bind("<ButtonRelease-1>", SliderEvent)
brake_bias_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_right_tyre_pressure_Scale.bind("<ButtonRelease-1>", SliderEvent)
front_left_tyre_pressure_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_right_tyre_pressure_Scale.bind("<ButtonRelease-1>", SliderEvent)
rear_left_tyre_pressure_Scale.bind("<ButtonRelease-1>", SliderEvent)
ballast_Scale.bind("<ButtonRelease-1>", SliderEvent)
fuel_load_Scale.bind("<ButtonRelease-1>", SliderEvent)
ramp_differential_Scale.bind("<ButtonRelease-1>", SliderEvent)

    
    
    
    

# Set the starting state of the interface, including selecting the
# default weather to send, and clearing the messages.  Select the first
# country in the list; because the <<ListboxSelect>> events are only
# fired when users makes a change, we explicitly call showTrackselection.
#weather.set('Dry')
statusmsg.set('')
trackBox.selection_set(0)

if config['autoUseChanges'] == True:
    autoUseChangesBox.invoke()
if config['autoSaveChanges'] == True:
    autoSaveChangesBox.invoke()
if config['autoUseButton'] == True:
    autoUseTrackBox.invoke()

#Assigning ComboBox default Values
raceBox.current(0)
carsBox.current(0) 
weatherBox.current(0)
presetBox.set("Load Preset")
carsBox['values']=raceSettings[raceBox.get()] 




if __name__ == "__main__":
    tracksBackgroundColor()
    #create sliders
    gameModeScaleSettings()

    #Load track
    showTrackselection()

root.mainloop()