from dict2xml import dict2xml


def convert_to_xml(students_list):
    dict_for_xml = dict()
    dict_for_xml['student'] = students_list
    xml = '<?xml version = "1.0" encoding = "UTF-8" standalone = "no"?>' + dict2xml(dict_for_xml, wrap="studentList",
                                                                                    indent="  ")
    return xml