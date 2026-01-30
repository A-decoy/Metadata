import exifread

def format_coord(unformatted_cord) -> str:
    return f"{unformatted_cord[0]}°{unformatted_cord[1]}'{eval(str(unformatted_cord[2]))}\""

def maps_url(lat, long, latref, longref) -> str:
    return f"https://maps.google.com/maps/place/{lat}{latref}+{long}{longref}"

with open("./IMAGENAME", 'rb') as f:
    tags = exifread.process_file(f)

wanted_rename = {
    "GPS GPSLatitude":"Latitude",
    "GPS GPSLatitudeRef":"LatitudeRef",
    "GPS GPSLongitudeRef":"LongitudeRef",
    "GPS GPSLongitude":"Longitude",
    "EXIF LensModel":"LensModel",
    "Image Make":"Image Make",
    "Image Model":"Image Model",
    "Image DateTime":"Date"
}

filtered_dict = {wanted_rename[want]: tags.get(want) for want in (wanted_rename.keys())}

for k, v in  filtered_dict.items():
    if v != None:
        print(f"{str(k):15} {str(v):50}")

try:
    lat = format_coord(list(filtered_dict["Latitude"].values))
    long = format_coord(list(filtered_dict["Longitude"].values))
    latref = str(filtered_dict["LatitudeRef"])
    longref = str(filtered_dict["LongitudeRef"])
    print(maps_url(lat, long, latref, longref))
except:
    pass
