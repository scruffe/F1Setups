
from F1Setups import raceSettings , weatherType , countrynames, write , root
import os
import sys
#make default setups
#import os
access_rights = 0o755


install = False
if install == True:
    for race in list(raceSettings):
        for car in raceSettings[race]:
            for weather in list(weatherType):
                path = "C:/Users/88/hello/Setups/" + race +"/"+ car +"/"+ weather
                try:
                    os.makedirs(path, access_rights)
                except OSError:
                    print ("Creation of the directory %s failed" % path)
                else:
                    print ("Successfully created the directory %s" % path)    

                for track in countrynames:
                    root.filename = path +"/"+ track + ".bin"
                    write()
            #os.mkdir(path, access_rights)
