import exifread
import subprocess

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

filtered_dict = {wanted_rename[want]: tags[want] for want in wanted_rename.keys()}

def format_coord(unformatted_cord) -> str:
    return f"{unformatted_cord[0]}°{unformatted_cord[1]}'{eval(str(unformatted_cord[2]))}\""

for k, v in  filtered_dict.items():
    print(f"{str(k):15} {str(v):50}")


lat = format_coord(list(filtered_dict["Latitude"].values))
long = format_coord(list(filtered_dict["Longitude"].values))
latref = str(filtered_dict["LatitudeRef"])
longref = str(filtered_dict["LongitudeRef"])

def maps_url(lat, long, latref, longref) -> str:
    return f"https://maps.google.com/maps/place/{lat}{latref}+{long}{longref}"

subprocess.run(["firefox", maps_url(long, lat, latref, longref)])
