# -*- coding:utf-8 -*-

import json
import copy
import difflib


class DictUtils(object):
    DELIMITER = '.'

    @classmethod
    def count_properties(cls, dict_obj):
        """Count up the number of properties.

        Arguments:
            (dict) dict_obj: Target

        Returns:
            (dict): The number of properties.
        """
        report = {}
        cls.__count_dict_properties(report, '', dict_obj)
        return report

    @classmethod
    def equals(cls, dict_obj1, dict_obj2, ignore_properties):
        """Return true if dict_obj1 and dict_obj2 are same.

        Arguments:
            (dict) dict_obj1:               Target one
            (dict) dict_obj2:               Target other
            (list(str)) ignore_properties:  Ignore properties

        Returns:
            (bool): True / False
        """
        cut1 = copy.deepcopy(dict_obj1)
        cut2 = copy.deepcopy(dict_obj2)

        if ignore_properties:
            cls.__dict_cut(cut1, ignore_properties)
            cls.__dict_cut(cut2, ignore_properties)

        return cut1 == cut2

    @classmethod
    def diff(cls, dict_obj1, dict_obj2, ignore_properties=None, ignore_order=False):
        """Create diff.

        Arguments:
            (dict) dict_obj1:               Target one
            (dict) dict_obj2:               Target other
            (list(str)) ignore_properties:  Ignore Properties
            (bool) ignore_order:            Ignore order in array

        Returns:
            (list): Diff (Empty list if same.)
        """
        j1 = copy.deepcopy(dict_obj1)
        j2 = copy.deepcopy(dict_obj2)
        if ignore_properties:
            cls.__dict_cut(j1, ignore_properties)
            cls.__dict_cut(j2, ignore_properties)
        if ignore_order:
            cls.__dict_sort(j1)
            cls.__dict_sort(j2)

        jstr1 = json.dumps(j1, indent=4, ensure_ascii=False, sort_keys=True)
        jstr2 = json.dumps(j2, indent=4, ensure_ascii=False, sort_keys=True)

        ds = difflib.unified_diff(jstr1.splitlines(), jstr2.splitlines())
        return list(ds)

    @classmethod
    def __count_dict_properties(cls, report, key_root, dict_obj):
        for k, v in dict_obj.items():
            if isinstance(v, dict):
                cls.__count_dict_properties(report, cls.DELIMITER.join([key_root, k]), v)
            elif isinstance(v, list):
                cls.__count_list_properties(report, '%s[]' % cls.DELIMITER.join([key_root, k]), v)
            else:
                cls.__count(report, cls.DELIMITER.join([key_root, k]))

    @classmethod
    def __count_list_properties(cls, report, key_root, list_obj):
        cls.__count(report, '%s (size:%d)' % (key_root, len(list_obj)))
        for v in list_obj:
            if isinstance(v, dict):
                cls.__count_dict_properties(report, key_root, v)
            elif isinstance(v, list):
                cls.__count_list_properties(report, '%s[]' % key_root, v)
            else:
                cls.__count(report, '%s -> ?' % key_root)

    @classmethod
    def __count(cls, report, property):
        if property in report:
            report[property] += 1
        else:
            report[property] = 1

    @classmethod
    def __dict_cut(cls, dict_obj, cut_properties, location=''):
        if location in cut_properties:
            dict_obj.clear()
            return

        for k, v in dict_obj.items():
            if isinstance(v, dict):
                cls.__dict_cut(v, cut_properties, "{0}.{1}".format(location, k))
            elif isinstance(v, list):
                cls.__list_cut(v, cut_properties, "{0}.{1}".format(location, k))
            else:
                if "{0}.{1}".format(location, k) in cut_properties:
                    dict_obj[k] = None

    @classmethod
    def __list_cut(cls, list_obj, cut_properties, location=''):
        if location in cut_properties:
            list_obj.clear()
            return

        for i, v in enumerate(list_obj):
            if isinstance(v, dict):
                cls.__dict_cut(v, cut_properties, "{0}.{1}".format(location, '[]'))
            elif isinstance(v, list):
                cls.__list_cut(v, cut_properties, "{0}.{1}".format(location, '[]'))
            else:
                list_obj[i] = None

    @classmethod
    def __dict_sort(cls, dict_obj):
        for k, v in dict_obj.items():
            if isinstance(v, dict):
                cls.__dict_sort(v)
            elif isinstance(v, list):
                cls.__list_sort(v)
            else:
                pass

    @classmethod
    def __list_sort(cls, list_obj):
        for v in list_obj:
            if isinstance(v, dict):
                cls.__dict_sort(v)
            elif isinstance(v, list):
                cls.__list_sort(v)
            else:
                pass
        list_obj.sort(key=lambda m: json.dumps(m, sort_keys=True, ensure_ascii=False))
