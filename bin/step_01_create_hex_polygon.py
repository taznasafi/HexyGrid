from Hexy import hexy, os
from Hexy import get_path
import my_paths


def create_hex_from_road_fc(run=False,create_hex_geojson=False, create_hex_json=False, res=8, state_wildcard="*", export_child=False, export_to_geopackage=False):
    """

    :param run:
    :param create_hex_geojson:
    :param create_hex_json:
    :param res:
    :param state_wildcard:
    :param export_child:
    :param export_to_geopackage:
    :return:
    """
    if run:

        hexy_maker = hexy.HexyMaker()
        hexy_maker.in_gdb_path = my_paths.road_by_state_gdb_path
        hexy_maker.output_folder = hexy_maker.base_input_folder
        hexy_maker.out_gdb = hexy_maker.base_output_folder

        fc_name_list = get_path.pathFinder(env=hexy_maker.in_gdb_path).get_layer_names_from_gdb_with_wildcard(wildcard=state_wildcard)

        #print(fc_name_list)

        for name in fc_name_list:
            print(name)
            df = hexy_maker.read_esri_fc(hexy_maker.in_gdb_path, name)


            #print(bbox)
            if create_hex_json:
                hexy_maker.get_parent_and_child_hex_dictionary(df,res,name+"_hex_{}".format(res),output_json=True)

            if create_hex_geojson:
                hexy_maker.polyfill_from_geoJson_extent(df, parent_resolution= res, export_hex=True,
                                                        geo_json_output_path= os.path.join(hexy_maker.base_output_folder, 'csv', 'geojson', name+"_geojson_hex"),
                                                        export_child=export_child,
                                                        export_geopackage = export_to_geopackage, layer_name = name)


def create_hex_from_polygon_by_state(run=False, create_hex_geojson=False,
                            create_hex_json=False, res=8,
                            state_wildcard="*", export_child=False,
                            export_to_geopackage=False):

    hexy_maker = hexy.HexyMaker()
    hexy_maker.in_gdb_path = my_paths.state_boundary_polygons
    hexy_maker.output_folder = hexy_maker.base_input_folder
    hexy_maker.out_gdb = hexy_maker.base_output_folder

    fc_name_list = get_path.pathFinder(env=hexy_maker.in_gdb_path).get_layer_names_from_gdb_with_wildcard(
        wildcard=state_wildcard)

    # print(fc_name_list)

    for name in fc_name_list:
        print(name)
        df = hexy_maker.read_esri_fc(hexy_maker.in_gdb_path, name)

        # print(bbox)
        if create_hex_json:
            hexy_maker.get_parent_and_child_hex_dictionary(df, res, name + "_hex_{}".format(res), output_json=True)

        if create_hex_geojson:
            hexy_maker.polyfill_from_polyon(df, parent_resolution=res, export_hex=True,
                                                    geo_json_output_path=os.path.join(hexy_maker.base_output_folder,
                                                                                      'csv', 'geojson',
                                                                                      name + "_geojson_hex"),
                                                    export_child=export_child,
                                                    export_geopackage=export_to_geopackage, layer_name=name)