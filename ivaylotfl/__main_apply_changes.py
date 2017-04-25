import sys
import win32com.client as com  # com library
import logging  # logging library

import __dialoghelper
import pddlhelper
import vissimhelper
import vaphelper


def __close_program(message):
    # Display error message in dialog if any
    if message != '':
        logging.getLogger('tfl_ivaylo').error('ERROR MESSAGE: ' + message)
        __dialoghelper.show_error_box_with_message(message)
    print '\n== END OF SCRIPT =='
    sys.exit()


def __get_absolute_path_for_file(filepath):
    return __dialoghelper.get_absolute_path_for_file(filepath)


def main():
    # initiliaze logger
    logger = logging.getLogger('tfl_ivaylo')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('extract_changes.log')
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    logger.info('== START OF SCRIPT ==')
    # Load PDDL plan
    model_file = __dialoghelper.ask_for_plan()
    if not __dialoghelper.is_file_chosen(model_file):
        __close_program('Please choose a file')

    new_timing = pddlhelper.get_new_stages_information(model_file)
    if new_timing == {}:
        __close_program('Could not read signal timing from ' + model_file)

    # Load Vissim
    inpx_file = __dialoghelper.ask_for_model()
    vissim = vissimhelper.initialise_vissim(com)
    if vissim is None:
        __close_program('Vissim program not found.'
                       'It might be because the program is not installed on the machine')

    vissimhelper.bring_vissim_to_front(vissim)
    vissimhelper.load_vissim_network(vissim, inpx_file)

    # Apply changes
    for key, value in new_timing.items():
        logger.info('Looking for : ' + key)
        divide = key.split('_')
        sc_id = int(divide[len(divide) - 1])
        logger.info('Looking for signal controller key: ' + str(sc_id))
        signal_controller = vissimhelper.get_sc_by_id(vissim, sc_id)
        vap_filepath = vissimhelper.get_vapfile(signal_controller)
        # vap_filepath = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap'
        if vap_filepath == '':
            logger.info('No VAP file for key: ' + key)
        else:
            vap_filepath = __get_absolute_path_for_file(vap_filepath)
            new_vap_file = vaphelper.edit_timing_changes(vap_filepath, value)
            vissimhelper.set_vap_file(signal_controller, new_vap_file)
            logger.info('Found VAP file for: ' + key + ' : ' + vap_filepath)
            logger.info('New VAP file set: ' + signal_controller.AttValue('SupplyFile1'))
            vissimhelper.save_network(vissim)