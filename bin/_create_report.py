from Hexy import hexy, os
import my_paths

def create_report(run=False, ):
    reporter = hexy.HexyMaker()
    reporter.in_gdb_path = my_paths.road_by_state_gdb_path
    reporter.in_path = os.path.join(reporter.base_input_folder, 'json')
    reporter.output_folder = os.path.join(reporter.base_output_folder, 'csv', 'json')

    if run:
        reporter.create_roads_in_child_hex()


def create_report_by_state(run=False, state=None):

    reporter = hexy.HexyMaker()
    reporter.in_gdb_path = my_paths.road_by_state_gdb_path
    reporter.in_path = os.path.join(reporter.base_input_folder, 'json')
    reporter.output_folder = os.path.join(reporter.base_output_folder, 'csv', 'json')

    if run:
        reporter.create_roads_in_child_hex_by_state(state=state)