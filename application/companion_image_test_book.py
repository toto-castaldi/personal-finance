import unittest
import os
import json
import common.utils as utils
import common.companion_image as companion_image
from decimal import Decimal, getcontext

logger = utils.init_log()

class Testbook(unittest.TestCase):

    def testbook(self):
        getcontext().prec = 2
        with open(os.environ.get("TEST_BOOK"), "r") as f:
            json_file = f.read()
            test_book = json.loads(json_file)
            logger.debug(test_book)
            for test_def_file_path in test_book:
                test_def_value = test_book[test_def_file_path]
                

                if test_def_value.get("skip", False) != True:
                    image, image_type = companion_image.image_type(test_def_file_path)
                    assert image_type == test_def_value["type"], f"wanted {test_def_value['type']}, got {image_type}"
                    
                    if image_type == "SATISPAY":
                        disponibilita, risparmi = companion_image.image_value_satispay(image)
                        
                        self.assertAlmostEqual(disponibilita, Decimal(test_def_value["disponibilita"]))
                        self.assertAlmostEqual(risparmi, Decimal(test_def_value["risparmi"]))

                    if image_type == "ADEGIRO":
                        value = companion_image.image_value_degiro(image)
                        wanted = Decimal(test_def_value["value"])
                        self.assertAlmostEqual(value, wanted)

if __name__ == "__main__":
    unittest.main()


