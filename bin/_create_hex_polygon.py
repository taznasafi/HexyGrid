from Hexy import hexy, os
from Hexy import get_path
import my_paths


def create_hex_from_road_fc(run=False,create_hex_geojson=False, create_hex_json=False, res=8, state_wildcard="*", export_child=False, export_to_geopackage=False):

    if run:

        test = hexy.HexyMaker()
        test.in_gdb_path = my_paths.road_by_state_gdb_path
        test.output_folder = test.base_input_folder
        test.out_gdb = test.base_output_folder

        fc_name_list = get_path.pathFinder(env=test.in_gdb_path).get_layer_names_from_gdb_with_wildcard(wildcard=state_wildcard)

        #print(fc_name_list)

        for name in fc_name_list:
            print(name)
            df = test.read_esri_fc(test.in_gdb_path, name)

            #print(bbox)
            if create_hex_json:
                test.get_parent_and_child_hex_dictionary(df,res,name+"_hex_{}".format(res),output_json=True)

            if create_hex_geojson:
                test.polyfill_from_geoJson_extent(df, resolution= res, export_hex=True,
                    geo_json_output_path= os.path.join(test.base_output_folder, 'csv',
                                                       'geojson', name+"_geojson_hex"),
                    export_child=export_child,
                    export_geopackage = export_to_geopackage, layer_name = name)
