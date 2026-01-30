import exifread
from tabulate import tabulate


with open("IMAGENAME", "rb") as f:
    tags = exifread.process_file(f)
    
for h in tags.keys():
    print(f"{h}: {tags[h]}") 

wanted = ["Image Make", "Image Model", "Image DateTime", "GPSLong", "GPSLatit" ,"LensModel"]
location_key = ["LatitudeRef", "Latitude", "LongitudeRef", "Longitude"]

wanted_dict = {h: tags[h] for items in wanted for h in tags.keys() if items in h}

x = 0
location = ""
error = 0

try:
    while x < 3:
        location += str(wanted_dict[f"GPS GPS{location_key[x+1]}"].values[0]) + "°" + str(wanted_dict[f"GPS GPS{location_key[x+1]}"].values[1]) + "'" + str(float(wanted_dict[f"GPS GPS{location_key[x+1]}"].values[2])) + '"' +    str(wanted_dict[f"GPS GPS{location_key[x]}"])
        x+=2     
except:
    error = 1
    pass

table = [["Device:", str(wanted_dict["Image Model"])], ["Time:", str(wanted_dict["Image DateTime"])], ["Camera:", str(wanted_dict["EXIF LensModel"])]]

if error == 1:
    print(tabulate(table))
else:
    table.append(["Location:", location])
    print(tabulate(table))
    print(f"Location: maps.google.com\maps\place{location}")