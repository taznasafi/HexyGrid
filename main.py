from bin import step_01_create_hex_polygon, step_02_create_report
from Hexy.get_path import pathFinder
import multiprocessing as mp


def parallel_processing_worker(state):

    print("working on state {}".format(state))
    step_02_create_report.create_report_by_state(run=True, state=state)

def parallel_processing_state_grids_worker(state):

    print("working on state {}".format(state))

    step_01_create_hex_polygon.create_hex_from_road_fc(run=True, create_hex_geojson=True, create_hex_json=True, res=8, state_wildcard="*_{}".format(state),
                                                       export_child=True, export_to_geopackage=True)


def parallel_processing_state_polygon_hex(state):

    print("working on state {}".format(state))

    step_01_create_hex_polygon.create_hex_from_polygon_by_state(run=True, create_hex_geojson=True, create_hex_json=True, res=8, state_wildcard="*_{}_*".format(state),
                                                       export_child=True, export_to_geopackage=True)

if __name__=="__main__":
    #Step 1: Init multiprocessing.Pool()
    pool = mp.Pool(1)

    # Step 2: `pool.map` the `parallel_processing_worker()`
    pool.map(parallel_processing_state_polygon_hex, ["01"])

    # Step 3: Don't forget to close
    pool.close()

