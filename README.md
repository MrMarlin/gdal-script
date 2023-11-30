# How to install
```
mkdir gdal-script
cd gdal-script
mkdir output images
git clone https://github.com/ChHarding/TouchTerrain_for_CAGEO.git
cd TouchTerrain_for_CAGEO

# make sure python venv module is installed if not already satisfied
sudo apt install python3-venv

#install gdal
sudo apt install g++
sudo apt install pyhton3-dev
sudo apt install libgdal-dev

export CPLUS_INCLUDE_PATH=/usr/include/gdal
export C_INCLUDE_PATH=/usr/include/gdal

# create venv for required packages
python3 -m venv venv
. venv/bin/activate

# install required packages !!order is very important here because gdal can be a bit of a bitch!!
pip install numpy
pip install --no-cache-dir --force-reinstall GDAL=="$(gdal-config --version).*"
pip install -r requirements.txt
cd ..
```

# How to use
The script takes a CSV file with a list of download link for individual GeoTIFF tiles. These tiles 
are then joinde into one big tile namen "chonk.tif". This "chonk.tif" is then converted into a printable 
STL file. If you only want to print a single GeoTIFF tile or have already a joined GeoTIFF file, you 
can place it in the "images" folder and rename it to "chonk.tif". If you do so, you can pass anything 
as the first argument and "skip" as the second argument.


`python3 TouchTerrain_for_CAGEO/merge.py <link to CSV> [skip]`
