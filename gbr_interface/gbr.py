import requests
import csv

north_west = [655000,218235]
south_east = [663400,214855]
url = f'https://api3.geo.admin.ch/rest/services/api/MapServer/identify?geometryType=esriGeometryEnvelope&geometry={north_west[0]},{north_west[1]},{south_east[0]},{south_east[1]}&tolerance=0&layers=all:ch.bfs.gebaeude_wohnungs_register&returnGeometry=false'

r = requests.get(url)
input = r.json()
output = []
for building in input['results']:
    attr = building['attributes']
    buildingtype = 'unknown'
    if attr['gkat'] == 1080:
        buildingtype = 'small_without_living'
    elif attr['gkat'] in [1020, 1030, 1040]:
        buildingtype = 'living'
    elif attr['gklas'] in [1271, 1276, 1277, 1278]:
        buildingtype = 'agriculture'

    gbr_url = f'https://map.geo.admin.ch/?ch.bfs.gebaeude_wohnungs_register={attr["egid"]}_0&time=None&lang=de&topic=ech'
    el = {
        'egid': attr['egid'],
        'street': attr['strname_deinr'],
        'zip': attr['dplz4'],
        'city': attr['ggdename'],
        'description': attr['gbez'],
        'buildingtype': buildingtype,
        'gkat': attr['gkat'],
        'gklas': attr['gklas'],
        'coordinate_lat': attr['gkode'],
        'coordinate_lon': attr['gkodn'],
        'area': attr['garea'],
        'volume': attr['gvol'],
        'url':gbr_url
    }
    output.append(el)


with open('output.csv', 'w', encoding='utf8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output[0].keys())
    writer.writeheader()
    writer.writerows(output)
