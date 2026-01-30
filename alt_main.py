import exifread
import sys


def format_coord(unformatted_cord) -> str:
    return f"{unformatted_cord[0]}°{unformatted_cord[1]}'{eval(str(unformatted_cord[2]))}\""

def maps_url(lat, long, latref, longref) -> str:
    return f"https://maps.google.com/maps/place/{lat}{latref}+{long}{longref}"

def convert_coord_to_decimal(degrees:float, minutes:float, seconds:float) -> float:
    """
    converts "angle" representation into decimal
    """
    return degrees + (minutes/60) + (seconds/3600)

COORD_KEYS = {
        "GPS GPSLatitude":"Latitude",
        "GPS GPSLatitudeRef":"LatitudeRef",
        "GPS GPSLongitudeRef":"LongitudeRef",
        "GPS GPSLongitude":"Longitude",
}

def get_coord_from_image(image_path:str) -> tuple:
    """
    Returns a tuple where the first argument is the latitude in decimal and the second argument is the longitude in decimal (signs included)
    """
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
    filtered_dict = {COORD_KEYS[want]: tags.get(want) for want in (COORD_KEYS.keys())}
    #print(filtered_dict)
    lat = [eval(str(val)) for val in filtered_dict["Latitude"].values]
    long = [eval(str(val)) for val in filtered_dict["Longitude"].values]
    latref = str(filtered_dict["LatitudeRef"])
    longref = str(filtered_dict["LongitudeRef"])
    signs_dict = {
        'N':1,
        'S':-1,
        'E':1,
        'W':-1
    }
    lat_decimal = signs_dict[latref]*convert_coord_to_decimal(*lat)
    long_decimal = signs_dict[longref]*convert_coord_to_decimal(*long)
    return (lat_decimal, long_decimal)

def main():
    if len(sys.argv) == 1:
        exit("Error: please enter a directory with all your images")
    files_list = sys.argv[1:]
    csv_string = "lat,lon\n"
    for image in files_list:
        coord_in_decimal = get_coord_from_image(image)
        csv_string += f"{coord_in_decimal[0]},{coord_in_decimal[1]}\n"
    print(csv_string)
if __name__ == "__main__":
    main()
