import os
import json
import common.utils as utils
import common.companion_image as companion_image

logger = utils.init_log()

if __name__ == "__main__":
    with open(os.environ.get("TEST_BOOK"), "r") as f:
        json_file = f.read()
        test_book = json.loads(json_file)
        logger.debug(test_book)
        for test_def_file_path in test_book:
            test_def_value = test_book[test_def_file_path]
            logger.debug(test_def_file_path)
            logger.debug(test_def_value)

            if test_def_value.get("skip", False) != True:
                image, image_type = companion_image.image_type(test_def_file_path)
                assert image_type == test_def_value["type"], f"wanted {test_def_value['type']}, got {image_type}"
                
                if image_type == "SATISPAY":
                    disponibilita, risparmi = companion_image.image_value_satispay(image)
                    
                    assert disponibilita == test_def_value["disponibilita"] , f"wanted {test_def_value['disponibilita']}, got {disponibilita}"
                    assert risparmi == test_def_value["risparmi"] , f"wanted {test_def_value['risparmi']}, got {risparmi}"

                if image_type == "DEGIRO":
                    value = companion_image.image_value_degiro(image)
                    assert str(value) == str(test_def_value["value"]) , f"wanted {test_def_value['value']}, got {value}"

