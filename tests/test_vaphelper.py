import unittest
import vaphelper  # class to be tested
import os.path  # to get path of the file being tested


class VapHelperTest(unittest.TestCase):

    # Tests the vaphelper functions when handling empty files
    # Should return error codes : -1 or empty objects/arrays
    def test_no_cyclelength_provided(self):
        _filepath = os.path.abspath('emptyfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_no_plans_provided(self):
        _filepath = os.path.abspath('emptyfile.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath)
        # len(cycl
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when handling files with the desired keys but no values provided
    # Should return error codes : -1
    def test_no_value_for_cyclelength(self):
        _filepath = os.path.abspath('halfemptyfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, -1)

    def test_no_value_for_plans(self):
        _filepath = os.path.abspath('halfemptyfile.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath)
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

    # Tests the vaphelper functions when handling correctly structured files
    # In the specific test the values that have to be returned are:
    # CycleLength = 72
    # Plans = [9, 24, 56, 72]
    def test_correct_cyclelength(self):
        _filepath = os.path.abspath('goodvapfile.vap')
        cycle_length = vaphelper.get_cycle_length_from_vap(_filepath)
        self.assertEqual(cycle_length, 72)

    def test_correct_plans(self):
        _filepath = os.path.abspath('goodvapfile.vap')
        plans = vaphelper.get_stage_lenghts_from_vap(_filepath)
        self.assertEqual(len(plans), 0)
        self.assertEqual(plans, [])

    #

if __name__ == '__main__':
    unittest.main()
