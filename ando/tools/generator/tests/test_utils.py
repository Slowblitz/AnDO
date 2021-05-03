import unittest

from ando.tools.generator.tests.utils import (initialize_test_directory, test_directory)
from ando.tools.generator.utils import (save_tsv, save_json)
import pandas as pd
import os
from pathlib import Path
import copy


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        initialize_test_directory()

    def test_create_file(self):
        df = pd.DataFrame()
        path_to_save = test_directory / "test_create_file.tsv"
        save_tsv(df, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_dummy_file(self):
        df = pd.read_csv(test_directory / 'test_files' / 'participants.tsv', sep='\t')
        path_to_save = test_directory / "test_create_dummy_file.tsv"
        save_tsv(df, path_to_save)

        self.assertTrue(Path(path_to_save).exists())
        df_test = pd.read_csv(test_directory / "test_create_dummy_file.tsv" , sep='\t')
        self.assertTrue(df_test.equals(df))

    def test_merge_existing_file(self):

        a = pd.DataFrame({
            "a": [1],
            "c": [0],
            "d": [2]
        })
        b = pd.DataFrame({
            "a": [0],
            "b": [1],

        })
        res = pd.DataFrame({
            "a": [0, 1],
            "b": [1, 'NaN'],
            "c": ['NaN', 0],
            "d": ['NaN', 2]
        })
        a.to_csv(test_directory / 'test_files' / 'a.tsv', sep='\t', index=False)
        b.to_csv(test_directory / 'test_files' / 'b.tsv', sep='\t', index=False)
        res.to_csv(test_directory / 'test_files' / 'dummy_res.tsv', sep='\t', index=False)

        df_dummy = pd.read_csv(test_directory / 'test_files' / 'a.tsv', sep='\t')
        df_res = pd.read_csv(test_directory / 'test_files' / 'dummy_res.tsv', sep='\t')
        # merge a -> b
        save_tsv(df_dummy, test_directory / 'test_files' / 'b.tsv')
        # read b
        df_test = pd.read_csv(test_directory / 'test_files' / 'b.tsv', sep='\t')

        self.assertTrue(df_test.equals(df_res))

    def test_create_json(self):
        data = {'test': 'dummy'}
        path_to_save = test_directory / "dummy.json"
        save_json(data, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_json_file_existing(self):
        data = {'test': 'dummy',
                'list': ['dummy'],
                "test_dict": {
                            "key_in_dict_1": "1",
                            }
                }
        result = copy.deepcopy(data)
        path_to_save = test_directory / 'test_files' / "dummy_file.json"
        save_json(result, path_to_save)
        # verify that all 1st level keys and values are preserved
        self.assertTrue(all([k in result for k in data.keys()]))  # key at first lvl
        self.assertTrue(all([data[k] == result[k] for k in data.keys() if not hasattr(data[k], '__iter__')]))
        self.assertEqual(result["test_dict"]["key_in_dict_1"], "1")  # 2nd lvl hard coded