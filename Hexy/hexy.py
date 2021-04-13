import os
import my_paths
from collections import defaultdict
import Hexy.__init__ as int_paths
from Hexy import logger, get_path
import pandas as pd
from functools import reduce
import geopandas as gp
from shapely.geometry import shape, Polygon, box
from h3 import h3
import json
import contextily as ctx
import cenpy
from decorator import *

class HexyMaker:

    base_input_folder, base_output_folder = int_paths.input_path, int_paths.output_path
    gdb_output_dic = defaultdict(list)
    def __init__(self, in_gdb_path=None, in_gdb_2_path=None, in_path=None, in_path2=None,
                 output_folder=None, out_path=None,
                 out_gdb_name=None, out_gdb=None):
        self.in_gdb_path = in_gdb_path
        self.in_gdb_2_path = in_gdb_2_path
        self.in_path = in_path
        self.in_path2 = in_path2
        self.output_folder = output_folder
        self.out_path = out_path
        self.out_gdb_name = out_gdb_name
        self.out_gdb = out_gdb

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def read_esri_fc(self, gdb_path, fc_name, driver='FileGDB'):
        """
        :param gdb_path: input esri gdb path
        :param fc_name:  esri feature class name
        :param driver: geopandas driver
        :return: geopandas DataFrame
        """
        if gdb_path.endswith(".gdb"):

            fc = gp.read_file(gdb_path,
                               driver=driver, layer=fc_name)
            return fc
        else:
            raise Exception("Make sure the you provide the right gdb path")

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def geojson_to_geoPandas_df(self, in_geojson):
        """
        :param input geojason format
        :return geopandas DataFrame

        """

        if in_geojson.endswith('.geojson'):
            return gp.read_file(in_geojson)
        else:
            raise Exception("Make sure the file is geojson file")

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def polyfill_from_geoJson_extent(self, df, parent_resolution, export_hex=False, geo_json_output_path=None, export_child=None, export_geopackage=False, layer_name=None):
        #todo: check the projection, the child projection seems to be right but not the parent, the parent hex are distorted.
        """

        :param df: input geopandas Dataframe
        :param parent_resolution: H3 Hex resolution
        :param export_hex: boolean, if you want to export the hexs
        :param geo_json_output_path: output of h3 geojson
        :param export_child: boolean, if you want to export the child of resolution
        :param export_geopackage: boolean, if you want to export to geopackage
        :param layer_name: the name of the layer that you want to export

        """


        bbox = box(*df.total_bounds)


        hexs = h3.polyfill(bbox.__geo_interface__, parent_resolution, geo_json_conformant=True)

        polygonise = lambda hex_id: Polygon(
            h3.h3_to_geo_boundary(
                hex_id, geo_json=True)
        )

        all_polys = gp.GeoSeries(list(map(polygonise, hexs)), index=hexs, crs="EPSG:4326")


        #print(all_polys)

        if export_hex is True and geo_json_output_path is not None:
            all_polys.to_file(geo_json_output_path +"_{}.json".format(parent_resolution), driver='GeoJSON')

        if export_hex is True and export_geopackage is True and layer_name is not None:
            all_polys.to_file(os.path.join(self.out_gdb, '{}_H3_hexy.gpkg'.format(layer_name)), layer="{}_res_{}".format(layer_name, parent_resolution), driver='GPKG')

        if export_child:
            child_res = parent_resolution + 1

            hexs = h3.polyfill(bbox.__geo_interface__, child_res , geo_json_conformant=True)

            polygonise = lambda hex_id: Polygon(
                h3.h3_to_geo_boundary(
                    hex_id, geo_json=True)
            )

            all_polys = gp.GeoSeries(list(map(polygonise, hexs)), index=hexs, crs="EPSG:4326")

            if export_hex is True and geo_json_output_path is not None:
                all_polys.to_file(geo_json_output_path + "_{}.json".format(child_res), driver='GeoJSON')

            if export_hex is True and export_geopackage is True and layer_name is not None:
                all_polys.to_file(os.path.join(self.out_gdb, '{}_H3_hexy.gpkg'.format(layer_name)),
                                  layer="{}_res_{}".format(layer_name,child_res),
                                  driver='GPKG')

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def polyfill_from_polyon(self, polygon, parent_resolution, export_hex=False, geo_json_output_path=None,
                                     export_child=None, export_geopackage=False, layer_name=None):

        """

        :param df: input geopandas Dataframe
        :param parent_resolution: H3 Hex resolution
        :param export_hex: boolean, if you want to export the hexs
        :param geo_json_output_path: output of h3 geojson
        :param export_child: boolean, if you want to export the child of resolution
        :param export_geopackage: boolean, if you want to export to geopackage
        :param layer_name: the name of the layer that you want to export

        """

        polygon_buffer = polygon['geometry'].buffer(0.0000001)[0]
        #print(polygon_buffer)

        hexs = h3.polyfill(polygon_buffer.__geo_interface__, parent_resolution, geo_json_conformant=True)

        polygonise = lambda hex_id: Polygon(
            h3.h3_to_geo_boundary(
                hex_id, geo_json=True)
        )

        all_polys = gp.GeoSeries(list(map(polygonise, hexs)), index=hexs, crs="EPSG:4326")

        # print(all_polys)

        if export_hex is True and geo_json_output_path is not None:
            all_polys.to_file(geo_json_output_path + "_{}.json".format(parent_resolution), driver='GeoJSON')

        if export_hex is True and export_geopackage is True and layer_name is not None:
            all_polys.to_file(os.path.join(self.out_gdb, 'gpkg', '{}_H3_hexy.gpkg'.format(layer_name)),
                              layer="{}_res_{}".format(layer_name, parent_resolution), driver='GPKG')

        if export_child:
            child_res = parent_resolution + 1

            hexs = h3.polyfill(polygon_buffer.__geo_interface__, child_res, geo_json_conformant=True)

            polygonise = lambda hex_id: Polygon(
                h3.h3_to_geo_boundary(
                    hex_id, geo_json=True)
            )

            all_polys = gp.GeoSeries(list(map(polygonise, hexs)), index=hexs, crs="EPSG:4326")

            if export_hex is True and geo_json_output_path is not None:
                all_polys.to_file(geo_json_output_path + "_{}.json".format(child_res), driver='GeoJSON')

            if export_hex is True and export_geopackage is True and layer_name is not None:
                all_polys.to_file(os.path.join(self.out_gdb, 'gpkg', '{}_H3_hexy.gpkg'.format(layer_name)),
                                  layer="{}_res_{}".format(layer_name, child_res),
                                  driver='GPKG')

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def read_json_from_file(self, path):
        with open(path) as f:
            data = json.load(f)

        return data

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def get_child__to_parent_hex_dictionary(self, df, child, output_name=None, output_json=False):
        """

        :param df: input geopandas geodataframe
        :param parent_resolution: the parent h3 resolution
        :param output_name: json dictionary name
        :param output_json: boolean, if you want to output to json file format
        :return: hex dictionary {"parent_hex_id": ["child_hex_id"]}
        """

        # parent_hex = list(h3.h3_to_parent(child_hex_id, child - 1))
        pass



    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def get_parent_and_child_hex_dictionary(self, df, parent_resolution, output_name=None, output_json=False):
        """

        :param df: input geopandas geodataframe
        :param parent_resolution: the parent h3 resolution
        :param output_name: json dictionary name
        :param output_json: boolean, if you want to output to json file format
        :return: hex dictionary {"parent_hex_id": ["child_hex_id"]}
        """

        hex_dict = defaultdict(list)
        bbox = box(*df.total_bounds)
        parent_hexs_list = h3.polyfill(bbox.__geo_interface__, parent_resolution, geo_json_conformant=True)

        for parent in parent_hexs_list:
            child_hex = list(h3.h3_to_children(parent, parent_resolution+1))
            hex_dict[parent].append(child_hex)

        if output_json:
            output = os.path.join(self.output_folder,"json", output_name+".json")
            with open(output, 'w') as out_json:
                json.dump(hex_dict, out_json)
            print("outfile: ", output)


        return hex_dict

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def save_json(self, python_dictionary, output_path):
        """

        :param python_dictionary: python dictionary object
        :param output_path: output path

        """
        with open(output_path, 'w') as fp:
            json.dump(python_dictionary, fp, indent=4)
        print("saved file to : {}".format(output_path))

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def create_map(self, in_gp_df, color="yellow", layer_trans=0.25):
        """

        :param in_gp_df: input geodataframe
        :param color: the color of the layer
        :param layer_trans: layer transparency
        :return: matplotlib static map
        """

        ax = in_gp_df.plot(alpha=layer_trans, color=color)
        return ctx.add_basemap(ax, crs=in_gp_df.crs.to_string())

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def create_spatial_index(self, in_GeoSeries):
        """

        :param in_GeoSeries: input geoseries
        :return: R-Tree spatial index
        """
        return in_GeoSeries.sindex

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def cal_pct_of_child_with_roads_for_parent_hexs(self):
        """
        This function creates pct of child hexs for the parent hex. This function is linear,
        state by state. Might take long time to complete.

        """
        import warnings
        warnings.filterwarnings("ignore")

        state_list = get_path.pathFinder.make_fips_list()

        nested_master_dict = defaultdict(list)

        for state in state_list:

            print("working on state Fips:", state)

            road_list = get_path.pathFinder(env=self.in_gdb_path).get_layer_names_from_gdb_with_wildcard("*_{}".format(state))
            #print(road_list)
            if len(road_list)>0:

                for road in road_list:
                    print("\t", road)
                    print("\tloading Road Fc From GDB to Memory")
                    road_df = HexyMaker(self).read_esri_fc(self.in_gdb_path, road)


                    r_df = gp.GeoSeries(road_df['geometry'])

                    print("\t\tCreating Spatial Index to speed up the process")

                    spatial_index = HexyMaker(self).create_spatial_index(r_df)

                    print("\t\tcreating Parent child dictionary using {} layer as a reference".format(road))
                    hex_dict = HexyMaker(self).get_parent_and_child_hex_dictionary(df=road_df,parent_resolution=8)
                    #print(hex_dict)
                    print("\t\tLooping over {} number of parent Hex ids, so go for a walk.... don't watch the paint dry\n".format(len(hex_dict.keys())))
                    for parent, children_list in hex_dict.items():
                        #print(parent)
                        child_counter = 0
                        for child in children_list[0]:
                            #print(child)
                            c = [Polygon(h3.h3_to_geo_boundary(child, geo_json=True))]

                            child_df = gp.GeoDataFrame(
                                                        {
                                                        "parent_id": [parent],
                                                        "child_id": [child],
                                                        'geometry': c
                                                        },
                                                        crs="EPSG:4326"
                                            )

                            child_df.to_crs(epsg=4269, inplace=True)


                            possible_matches_index = list(spatial_index.intersection(child_df.total_bounds))

                            # delete spatial index to free up memory.
                            del spatial_index
                            # get possible matches of the road dataframe and drop the none intersecting features
                            possible_matches = road_df.iloc[possible_matches_index]


                            precise_matches = possible_matches[possible_matches.intersects(c[0])]

                            #print(precise_matches)


                            if  len(precise_matches)>0:
                                #print("intersect")
                                child_counter += 1
                            else:
                                pass

                        nested_master_dict[road].append({parent: {'pct_child_with_road':child_counter / 7}})
                        #print(dict(nested_master_dict))
                    print("\t\tsaving Json file")
                    HexyMaker(self).save_json(dict(nested_master_dict),os.path.join(self.output_folder,
                                                                                        "hexyH3Grid_{}.json".format(road)))

    @logger.time_it()
    @logger.event_logger(logger.create_logger())
    def cal_pct_of_child_with_roads_for_parent_hexs_by_state(self, state):
        import warnings
        warnings.filterwarnings("ignore")

        state_list = get_path.pathFinder.make_fips_list()

        nested_master_dict = defaultdict(list)



        road_list = get_path.pathFinder(env=self.in_gdb_path).get_layer_names_from_gdb_with_wildcard(
            "*_{}".format(state))
        # print(road_list)
        if len(road_list) > 0:

            for road in road_list:
                print("\t", road)
                print("\tloading Road Fc From GDB to Memory")
                road_df = HexyMaker(self).read_esri_fc(self.in_gdb_path, road)

                r_df = gp.GeoSeries(road_df['geometry'])

                print("\t\tCreating Spatial Index to speed up the process")

                spatial_index = HexyMaker(self).create_spatial_index(r_df)

                print("\t\tcreating Parent child dictionary using {} layer as a reference".format(road))
                hex_dict = HexyMaker(self).get_parent_and_child_hex_dictionary(df=road_df, parent_resolution=8)
                # print(hex_dict)
                print(
                    "\t\tLooping over {} number of parent Hex ids, so go for a walk.... don't watch the paint dry\n".format(
                        len(hex_dict.keys())))
                for parent, children_list in hex_dict.items():
                    # print(parent)
                    child_counter = 0
                    for child in children_list[0]:
                        child_dict = {}
                        c = [Polygon(h3.h3_to_geo_boundary(child, geo_json=True))]

                        child_df = gp.GeoDataFrame(
                            {
                                "parent_id": [parent],
                                "child_id": [child],
                                'geometry': c
                            },
                            crs="EPSG:4326"
                        )

                        child_df.to_crs(epsg=4269, inplace=True)

                        possible_matches_index = list(spatial_index.intersection(child_df.total_bounds))
                        possible_matches = road_df.iloc[possible_matches_index]
                        precise_matches = possible_matches[possible_matches.intersects(c[0])]

                        # print(precise_matches)

                        if len(precise_matches) > 0:
                            # print("intersect")
                            child_counter += 1

                        else:
                            pass

                    nested_master_dict[road].append({parent: {'number_childs_with_roads': child_counter }})

                    # print(dict(nested_master_dict))
                print("\t\tsaving Json file")
                HexyMaker(self).save_json(dict(nested_master_dict), os.path.join(self.output_folder,
                                                                                 "hexyH3Grid_{}.json".format(
                                                                                     road)))