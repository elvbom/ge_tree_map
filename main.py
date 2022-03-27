import ee
import folium
import os
import webbrowser

from helpers import BASEMAPS, set_vis_params


def authenticate():
    ee.Authenticate()


def add_layer(path, params_dict, show=False):
    img = ee.Image(path)
    mask = img.updateMask(img.gt(0))
    for n, vis_param in params_dict.items():
        f_map.add_image(mask, vis_param, n, show=show, opacity=0.6)
    return f_map


def show_web_map(f_map, file_name):
    f_map.save(file_name)
    webbrowser.open('file://' + os.path.realpath(file_name), new=2)


def elevation_mt_everest():
    # example from https://spatial.utk.edu/maps/ee-api-folium-setup.html
    dem = ee.Image('USGS/SRTMGL1_003')
    coords = ee.Geometry.Point([86.9250, 27.9881])
    elev = dem.sample(coords, 30).first().get('elevation').getInfo()
    print('Elevation Mt Everest (m):', elev)


ee.Initialize()

# create a folium map object with long lat for Sweden
lat_swe, lon_swe = 63, 15
f_map = folium.Map(location=[lat_swe, lon_swe], zoom_start=5)

# add custom maps
BASEMAPS['esri_satellite'].add_to(f_map)

# add data: Hansen Global Forest Change v1.8
hansen_params = {
    'tree cover': set_vis_params(['treecover2000'], 0, 100, ['d3ffcc', '094200']),
    'tree loss': set_vis_params(['lossyear'], 0, 20, ['ffd500', 'ff0004'])
}
# add_layer('UMD/hansen/global_forest_change_2020_v1_8', hansen_params)

# add data: Global Forest Canopy Height, 2005 height
canopy_params = {
    'canopy height (under 20 m)': set_vis_params(['1'], 0, 20, ['d6fcfc', '0000FF']),
    'canopy height (over 20 m)': set_vis_params(['1'], 20, 73, ['#c4c4ff', '#00003b'])
}
# add_layer('NASA/JPL/global_forest_canopy_height_2005', canopy_params)

# add data: Global PALSAR-2/PALSAR Forest/Non-Forest Map
# FIXME fixa så man kan filtrera datum
# FIXME https://developers.google.com/earth-engine/datasets/catalog/JAXA_ALOS_PALSAR_YEARLY_FNF
palsar_params = set_vis_params(['fnf'], 1, 3, ['006400', 'FEFF99', '0000FF'])
f_map.add_image_collection('JAXA/ALOS/PALSAR/YEARLY/FNF', 'forest vs non-forest', palsar_params, 'palsar params')


# add a layer control panel
f_map.add_child(folium.LayerControl())

show_web_map(f_map, 'hansen_map')
