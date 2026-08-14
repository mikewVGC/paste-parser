
import unittest
from unittest.mock import patch, mock_open

import json

from paste_parser.paste_parser import PasteParser


class TestPasteParser(unittest.TestCase):

    def test_parser_basic_ots(self):

        parser = PasteParser()

        with open("tests/pastes/basic-cts.paste", 'r') as pastefile:
            mons = parser.parse(pastefile.read())

        self.assertEqual(mons[0].species, "Garchomp")
        self.assertEqual(mons[0].item, "Life Orb")


    def test_parser_full_sheet(self):

        parser = PasteParser()

        with open("tests/pastes/full-ots-champs.paste", 'r') as pastefile:
            mons = parser.parse(pastefile.read())

        self.assertEqual(mons[1].species, "Incineroar")
        self.assertEqual(mons[1].item, "Sitrus Berry")
        self.assertEqual(mons[1].stats["hp"]["ev"], 31)


    def test_parser_edge_case_sheet(self):

        parser = PasteParser()

        with open("tests/pastes/full-ots-sv.paste", 'r') as pastefile:
            mons = parser.parse(pastefile.read())

        self.assertEqual(mons[0].species, "Calyrex-Shadow")
        self.assertEqual(mons[0].stats["atk"]["iv"], 0)

        self.assertEqual(mons[1].species, "Talonflame")
        self.assertEqual(mons[1].item, "")
        self.assertEqual(mons[1].stats["hp"]["ev"], 252)

        self.assertEqual(mons[4].species, "Amoonguss")
        self.assertEqual(mons[4].nickname, "Nap Time")
