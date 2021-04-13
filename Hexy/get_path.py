import fnmatch
import os
import pandas as pd
from fiona import listlayers
from enum import Enum
from collections import defaultdict
import re


class pathFinder:


    def __init__(self, env=None, outPathFolder=None, outPathGDB = None):
        self.env = env
        self.outPathFolder = outPathFolder
        self.outPathGDB = outPathGDB

    def path_grabber(self, wildcard=None):
        parsed_path_list = []
        for root, dirs, files in os.walk(self.env):
            for file in fnmatch.filter(files, wildcard):
                parsed_path_list.append(os.path.join(root, file))

        return list(parsed_path_list)

    def gdb_path_grabber(self, wildcard=None):
        parsed_path_list = []
        for root, dirs, files in os.walk(self.env):
            for dir in fnmatch.filter(dirs, wildcard):
                parsed_path_list.append(os.path.join(root, dir))

        return list(parsed_path_list)


    @classmethod
    def get_all_shapefile_path_walk(cls, path):
        file_loc = []

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in files:
                # for the files that endswith .shp, join the root and file
                if file.endswith(".shp"):
                    # create a local variable that we can assign the root and file path then loop it
                    path = os.path.join(root, file)
                    # append the path in our file_loc list
                    file_loc.append(path)

        return list(file_loc)


    @classmethod
    def get_shapefile_path_wildcard(cls, path, wildcard):
        file_loc = []

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in fnmatch.filter(files, wildcard+".shp"):
                # for the files that endswith .shp, join the root and file
                file_loc.append(os.path.join(root, file))

        if list(file_loc) == 'NoneType':
            raise Warning("Did not find path, check your wild card")

        else:
            return list(file_loc)
    r"\n\t"
    @classmethod
    # create a list of fips from the table.
    def make_fips_list(cls):
        import pandas as pd
        Fips_table_path = r"./state_FIPS.txt"
        data = pd.read_csv(Fips_table_path, sep='|')
        data["STATE"] = data["STATE"].astype(str)
        data['STATE'] = data["STATE"].apply(lambda x: x.zfill(2))
        return data.STATE.tolist()


    @classmethod
    def query_provider_by_FIPS(cls, path, fips):
        import pandas as pd
        df = pd.read_csv(path)
        fips_query = df.query("stateFIPS ==" + str(fips))
        fips_query = fips_query.dropna(axis=1, how="any")
        return list(fips_query.applymap(int).values.flatten()[1:])

    @classmethod
    def query_provider_pid_by_provider_FRN(cls, table_path, frn):
        df = pd.read_csv(table_path)
        df['f477_provider_frn'] = df["f477_provider_frn"].apply(lambda x: "%010d" % x)
        query_results = df.query("f477_provider_frn == '{}'".format(frn))
        #print(query_results)
        dic = query_results.to_dict('records')
        return dic[0]

    @classmethod
    def query_pid_by_dba(cls, table_path, dba):

        df = pd.read_csv(table_path)
        # print(df)
        query_results = df.query("dba =='{}'".format(dba))
        dic = query_results.to_dict('records')
        #print(dic)
        return dic[0]

    @classmethod
    def query_df_column_wildcard(cls, path, type=None, sheet_name=None, column_name=None, q=None):

        if type =='xlx':
            df = pd.read_excel(path, sheet_name=sheet_name, engine='openpyxl')
            query_results = df[df[column_name].str.contains(q)]
        else:
            df = pd.read_csv(path)
            # print(df)
            query_results = df.query(q)
        dic = query_results.to_dict('records')
        #print(dic)
        return dic


    @classmethod
    def filter_List_of_shapefiles_paths_with_wildcard(cls, path_link_list, wildcard):
        for path_link in path_link_list:
            if fnmatch.fnmatch(os.path.basename(path_link), wildcard + ".shp"):
                return path_link



    @classmethod
    def get_shapefile_path_walk_dict(cls, path, ):


        file_dict = defaultdict(list)

        # use os.walk to find the root, directory, and files
        for root, dirs, files in os.walk(path):
            # create a loop by files
            for file in files:
                # for the files that endswith .shp, join the root and file
                if file.endswith(".shp"):
                    # create a local variable that we can assign the root and file path then loop it
                    file_dict[root].append(file)


        return file_dict

    def get_layer_names_from_gdb_with_wildcard(self, wildcard="*"):
        filtered_name_list = []
        if self.env.endswith(".gdb"):
            for layer in listlayers(self.env):
                #print(layer)
                if fnmatch.fnmatch(layer, wildcard):
                    filtered_name_list.append(layer)
            return list(filtered_name_list)
        else:
            raise Exception("the file path must be gdb")
