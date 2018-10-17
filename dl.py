# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 21:27:54 2018

@author: smrak
"""
from pathlib import Path
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from datetime import datetime
import urllib3
from typing import Union

def dl(date:datetime = None, 
       wl: int = None, 
       res: int = 512, 
       odir: Union[str,Path] = None):
    if wl is None: 
        wl = '0193'
        print ('Wavelength requirement was not specified. Default wavelength \
               is 0193A. Next time specify your wavelength as: wl=')
    # Convert wl to str, make sure there are 4 digits
    wl = str(wl)
    if (len(wl) < 4): wl = '0' + wl 
    # Convert res 2 string
    res = str(res)
    # Prepare url address for SDO images
    urlroot = 'https://sdo.gsfc.nasa.gov/assets/img/browse/'
    month = str(date.month) if date.month >= 10 else '0' + str(date.month)
    day = str(date.day) if date.day >= 10 else '0' + str(date.day)
    url = urlroot + str(date.year) + '/' + month + '/' + day + '/'
    
    # urllib3 object: https
    http = urllib3.PoolManager()
    # Open the https page
    req = Request(url)
    page = urlopen(req).read()
    # bs4 parse html objects
    soup = BeautifulSoup(page, 'html.parser')
    # get <a> objects
    clips = soup.find_all('a')
    # parse attribures to a list of directories [{href: x}, {href, 'y'}, {...}]
    ahrefs = [href.attrs for href in clips]
    
    # Init empty lists
    t = []
    picture = []
    # date for parse:
    datestr = date.strftime('%Y%m%d')
    # Parse images according to resolution, date, wavelength and type
    for i,line in enumerate(ahrefs):
        if ('.jpg' in line['href']) and (res in line['href']) and \
            (datestr in line['href']) and (wl in line['href']):
            t.append(datetime.strptime(line['href'][:15], '%Y%m%d_%H%M%S'))
            picture.append(line['href'])
        else:
            pass
    # Save the suckers
    odir = Path(odir).expanduser()
    if not odir.is_dir():
        odir = odir.parent()
    
    for i, urlpic in enumerate(picture):
        savefn = odir / urlpic
        r = http.request('GET', url+urlpic, preload_content=False)
        with open(savefn, 'wb') as f:
            f.write(r.read())


#urlroot = 'https://sdo.gsfc.nasa.gov/assets/img/browse/' #2016/03/09/'
res = 1024
date = datetime(2012,3,20)#'20120320'
wl = '0193'
odir = 'E:\\sdo\\20120320\\'

dl(date=date,wl=193,res=res,odir=odir)