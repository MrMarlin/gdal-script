import datetime
import requests
from osgeo import gdal
from os import listdir, chdir, mkdir
from os.path import isfile, join
import sys
import os.path
from touchterrain.common import TouchTerrainEarthEngine as TouchTerrain
from touchterrain.common.TouchTerrainGPX import *
import zipfile
import shutil
from multiprocessing.pool import ThreadPool

def download_tile(url):
    path, link = url

    r = requests.get(link)
    with open(f'{tiles_dir}/{path}', 'wb') as file:
        file.write(r.content)

def zip_links(link_file):
    counter = 0
    url_zips = []
    for link in requests.get(link_file).content.decode('utf-8').split('\n'):
        url_zips.append((f'{counter}', link))
        counter += 1

    return url_zips

def download_tiles_parallel(zips):
    pool = ThreadPool(8)
    pool.imap_unordered(download_tile, zips)
    pool.close()
    pool.join()
    

file_link  = sys.argv[1]
tiles_dir = './images'
output_dir = './output'
file_name = f'{tiles_dir}/chonk.tif'

if not sys.argv[len(sys.argv)-1] == "skip":
    download_tiles_parallel(zip_links(file_link))
    tiles = [f'{tiles_dir}/{f}' for f in listdir(tiles_dir) if isfile(join(tiles_dir,f))]
    print(tiles)
    g = gdal.Warp(file_name, tiles,  format="GTiff", options=["COMPRESS=LZW", "TILED=YES", "NUM_THREADS=ALL_CPUS", "BIGTIFF=YES"])



args = TouchTerrain.initial_args # default args

# Comment out one of following two lines:
#args["importedDEM"] =  "stuff/pyramid.tif" # location of local geotiff to use
args["importedDEM"] = f'{file_name}' # use online DEM rasters instead

# convert into an absolute path for later
if args["importedDEM"] != None:
    args["importedDEM"]= os.path.abspath(args["importedDEM"]) 
    print("importedDEM", args["importedDEM"])

args["tilewidth"] = 200 # in mm
args["ntilesx"] = 1 # number of tiles in x  
args["ntilesy"] = 1 # number of tiles in y 
args["basethick"] = 2 # in mm
args["printres"] = 0.08 # in mm
args["zscale"] = 1 # elevation scale factor
args["zip_file_name"] = datetime.datetime.now().isoformat() # terrain model will be inside tmp/myterrain.zip
args["CPU_cores_to_use"] = 1

# create zipfile under tmp with the STL file of the terrain model
totalsize, full_zip_file_name = TouchTerrain.get_zipped_tiles(**args) 
print("Created zip file", full_zip_file_name,  "%.2f" % totalsize, "Mb")

with zipfile.ZipFile(full_zip_file_name, 'r') as zip_ref:
    zip_ref.extractall(output_dir)

shutil.rmtree(f'{tiles_dir}')
mkdir(f'{tiles_dir}')
