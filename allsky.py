import numpy as np
import datetime
from PIL import Image
from PIL import ImageDraw
import ephem
import math
import win32com.client      #needed to load COM objects

util = win32com.client.Dispatch("ASCOM.Utilities.Util")

def get_stars_info(star):
    OPD=ephem.Observer()
    OPD.lat='-22.5344'
    OPD.lon='-45.5825'
    OPD.date = datetime.datetime.utcnow()
    # %% these parameters are for super-precise estimates, not necessary.
    OPD.elevation = 1864 # meters
    OPD.horizon = 0
    sun = ephem.Sun(OPD)
    moon = ephem.Moon(OPD)        
    sidereal_time = OPD.sidereal_time()
    rigel = ephem.star(star)
    alt, az = get_az_alt(rigel._ra, rigel._dec, sidereal_time)
    return alt, az
    
def edit_image():
    # open image
    img = Image.open('allsky340c.jpg').convert("RGBA")
    txt = Image.new('RGBA', img.size, (255,255,255,0))
    # draw image object
    I1 = ImageDraw.Draw(txt)

    alt, az = get_stars_info('Antares')
    x, y = pol2cart(90-alt, 55+az)
    print(x,y)
    # add text to image
    I1.text((320+x, 240-y), "Antares", fill=(255, 255, 0, 75))

    #STAR2
    alt, az = get_stars_info('Arcturus')
    x, y = pol2cart(90-alt, 55+az)
    print(x,y)
    # add text to image
    I1.text((320+x, 240-y), "Arcturus", fill=(255, 255, 0, 75))

    #Star3
    alt, az = get_stars_info('Acrux')
    x, y = pol2cart(90-alt, 55+az)
    print(x,y)
    # add text to image
    I1.text((320+x, 240-y), "Acrux", fill=(255, 255, 0, 75))

    #Star4
    alt, az = get_stars_info('Vega')
    x, y = pol2cart(90-alt, 55+az)
    print(x,y)
    # add text to image
    I1.text((320+x, 240-y), "Vega", fill=(255, 255, 0, 75))

    # save image
    combined = Image.alpha_composite(img, txt)
    combined.show()

def get_az_alt(pointRA, pointDEC, sideral):
    DEG = 180 / math.pi
    RAD = math.pi / 180.0
    coordRA = util.HMSToHours(pointRA)
    coordDEC = util.DMSToDegrees(pointDEC)
    lst = util.HMSToHours(sideral)
    H = (lst - coordRA) * 15
    latitude = util.DMSToDegrees('-22:32:04')

    #altitude calc
    sinAltitude = (math.sin(coordDEC * RAD)) * (math.sin(latitude * RAD)) + (math.cos(coordDEC * RAD) * math.cos(latitude * RAD) * math.cos(H * RAD))
    altitude = math.asin(sinAltitude) * DEG #altura em graus

    #azimuth calc
    y = -1 * math.sin(H * RAD)
    x = (math.tan(coordDEC * RAD) * math.cos(latitude * RAD)) - (math.cos(H * RAD) * math.sin(latitude * RAD))

    #This AZposCalc is the initial AZ for dome positioning
    AZposCalc = math.atan2(y, x) * DEG

    #converting neg values to pos
    if (AZposCalc < 0) :
        AZposCalc = AZposCalc + 360    

    print(altitude, AZposCalc)
    return(altitude, AZposCalc)

def pol2cart(rho, phi):
    x = rho * np.cos(math.radians(phi))
    y = rho * np.sin(math.radians(phi))
    x=3*x+x/2
    y=2.8*y+y/2
    return(x, y)

edit_image()