from xml.dom.minidom import parse
import json

dom = parse('govi.kml')

marks = dom.getElementsByTagName('Placemark')

output = []

for mark in marks:
    kvid = mark.getAttribute('id')
    
    name = mark.getElementsByTagName('name')[0].childNodes[0].data
    
    coordinates = mark.getElementsByTagName('coordinates')[0].childNodes[0].data
    
    lat, lon = coordinates.split(',')
    
    output.append({'name': name, 'id': kvid, 'lat': float(lat), 'lon': float(lon)})
    
open('kml.json', 'w').write(json.dumps(output, indent=2))