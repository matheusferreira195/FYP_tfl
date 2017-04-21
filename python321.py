import sys
import win32com.client as com  # com library

import dialoghelper
import pddlhelper
import vissimhelper
import vaphelper

def _close_program(message):
    # Display error message in console if any
    if message != '':
        print 'ERROR MESSAGE: ' + message
        dialoghelper.showerror(message)
    print '\n== END OF SCRIPT =='
    sys.exit()


def _get_absolute_path_for_file(filepath):
    return dialoghelper.get_absolute_path_for_file(filepath)


def _look_for_sg_by_sc_id(sc_id):
    sc = Vissim.Net.SignalControllers.ItemByKey(sc_id)
    if sc is None:
        print 'No Signal Controller with id: ' + str(sc_id)
        return None
    else:
        return sc


print '== START OF SCRIPT =='

model_file = dialoghelper.ask_for_plan()
if not dialoghelper.check_file_chosen(model_file):
    _close_program('Please choose a file')

new_timing  = pddlhelper.get_new_stages_information(model_file)
if new_timing == {}:
    _close_program('Could not read signal timing from ' + model_file)

inpx_file = dialoghelper.ask_for_model()

Vissim = com.Dispatch('Vissim.Vissim')
Vissim.BringToFront()

if not vissimhelper.check_vissim_initialised(Vissim):
    _close_program('Vissim program not found.'
                   'It might be because the program is not installed on the machine')

Vissim.LoadNet(inpx_file)
Vissim.BringToFront()

for key, value in new_timing.items():
    print 'Looking for : ' + key
    filepath = ''
    look_for_that_prefix = vissimhelper.junction_prefix
    # if stringhelper.does_string_contain_substring(key, look_for_that_prefix):
    # sc_id = int(re.sub(look_for_that_prefix, '', key))
    divide = key.split('_')
    sc_id = int(divide[len(divide) - 1])
    print 'Looking for signal controller key: ' + str(sc_id)
    signal_controller = _look_for_sg_by_sc_id(sc_id)

    # vap_filepath = signal_controller.AttValue('SupplyFile1')
    vap_filepath = 'C:\\Users\\Ivaylo\\Desktop\\A3 FT Model v2\\33.vap'

    if vap_filepath == '':
        print 'No VAP file for key: ' + key
    else:
        vap_filepath = _get_absolute_path_for_file(vap_filepath)
        print 'Found VAP file for: ' + key + ' : ' + vap_filepath
        new_vap_file = vaphelper.edit_timing_changes(vap_filepath, value)
        signal_controller.SetAttValue('SupplyFile1', new_vap_file)
        print 'New VAP file set: ' + signal_controller.AttValue('SupplyFile1')

Vissim.SaveNet()
