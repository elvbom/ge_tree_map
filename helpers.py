import ee
import folium


def make_tile_layer(tiles, attr, name, show=False, opacity=1):
    return folium.TileLayer(
        tiles=tiles,
        attr=attr,
        name=name,
        overlay=True,
        control=True,
        show=show,
        opacity=opacity
    )


BASEMAPS = {
    'google_maps': make_tile_layer(
        'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        'Google',
        'Google Maps'
    ),
    'google_satellite': make_tile_layer(
        'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        'Google',
        'Google Satellite'
    ),
    'google_terrain': make_tile_layer(
        'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        'Google',
        'Google Terrain'
    ),
    'google_satellite_hybrid': make_tile_layer(
        'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        'Google',
        'Google Satellite'
    ),
    'esri_satellite': make_tile_layer(
        'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        'Esri',
        'Esri Satellite'
    )
}


def set_vis_params(bands, mini, maxi, palette):
    return {'bands': bands, 'min': mini, 'max': maxi, 'palette': palette}


def add_ee_image(self, ee_object, vis_params, name, show, opacity=1):
    try:
        map_id_dict = ee.Image(ee_object).getMapId(vis_params)
        make_tile_layer(
            map_id_dict['tile_fetcher'].url_format,
            'Google Earth Engine',
            name,
            show=show,
            opacity=opacity
        ).add_to(self)
    except:
        print("Could not display {}".format(name))


def add_ee_image_collection(self, ee_object, legend, vis_params, name, opacity=1):
    try:
        dataset = ee.ImageCollection(ee_object).filterDate('2017-01-01', '2017-12-31')
        forestNonForest = dataset.select(vis_params['bands'])
        map_id_dict = forestNonForest.getMapId(vis_params)
        make_tile_layer(
            tiles=map_id_dict['tile_fetcher'].url_format,
            attr='Google Earth Engine',
            name=legend,
            opacity=opacity
        ).add_to(self)
    except:
        print("Could not display {}".format(name))


def add_ee_geometry(self, ee_object, name):
    try:
        folium.GeoJson(
            data=ee_object.getInfo(),
            name=name,
            overlay=True,
            control=True,
        ).add_to(self)
    except:
        print("Could not display {}".format(name))


def add_ee_feature_collection(self, ee_object, vis_params, name, opacity=1):
    try:
        ee_object_new = ee.Image().paint(ee_object, 0, 2)
        map_id_dict = ee.Image(ee_object_new).getMapId(vis_params)
        make_tile_layer(
            map_id_dict['tile_fetcher'].url_format,
            'Google Earth Engine',
            name,
            opacity=opacity
        ).add_to(self)
    except:
        print("Could not display {}".format(name))


folium.Map.add_image = add_ee_image
folium.Map.add_image_collection = add_ee_image_collection
folium.Map.add_geometry = add_ee_geometry
folium.Map.add_feature_collection = add_ee_feature_collection
