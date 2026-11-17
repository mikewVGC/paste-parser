
from __future__ import annotations

import re

from paste_parser.pokemon import Pokemon

"""
Parses a pokepaste (pass the raw text of the paste) into a somewhat usable format
"""

class PasteParser:

    def __init__(self):
        # from the pokepaste source
        self.move_reg = r"^(-)( ([A-Z][a-z\']*(?:[- ][A-Za-z][a-z\']*)*)(?: \[([A-Z][a-z]+)\])?(?: / [A-Z][a-z\']*(?:[- ][A-Za-z][a-z\']*)*)* *)$"
        self.stat_reg = r"^[I|E]Vs: (\d+ HP)?( / )?(\d+ Atk)?( / )?(\d+ Def)?( / )?(\d+ SpA)?( / )?(\d+ SpD)?( / )?(\d+ Spe)?( *)$"

        # hand woven regular expressions
        self.name_regex = r"^([A-zÀ-ÿ][A-zÀ-ÿ\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF '.!?^_-]+)(?: \(([A-z '-]+)\))?(?: \(([MF])\))?(?:( @ )([A-Z][A-z '-]+?))?( *)$"
        self.prop_reg = r"^([A-Z][A-Za-z ]+): (.+)( *)$"
        self.nature_reg = r"^([A-Z][a-z]+) Nature( *)$"

    def parse(self, paste:str) -> list:
        mons = []

        paste = paste.split("\n")

        paste.append("\n")

        mon = Pokemon()

        for line in paste:
            line = line.strip()

            if len(line) == 0:
                if not len(mon.species):
                    continue

                mons.append(mon)

                mon = Pokemon()
                continue

            # fires for nature / stat alignment
            matches = re.findall(self.nature_reg, line)
            if len(matches):
                mon.nature = matches[0][0]
                continue

            # fires for the name/item/etc (nature has to go first since this also matches that)
            matches = re.findall(self.name_regex, line)
            if len(matches):
                if len(matches[0][0]) and not len(matches[0][1]):
                    mon.species = matches[0][0]
                elif len(matches[0][0]) and len(matches[0][1]):
                    if matches[0][1] in ('M', 'F'):
                        mon.species = matches[0][0]
                        mon.gender = matches[0][1]
                    else:
                        mon.nickname = matches[0][0]
                        mon.species = matches[0][1]

                # this will always be gender
                if len(matches[0][2]):
                    mon.gender = matches[0][2]

                # this will always be the item
                if len(matches[0][4]):
                    mon.item = matches[0][4]

                continue

            # fires for stats (needs to go before ability fire)
            matches = re.findall(self.stat_reg, line)
            if len(matches):
                for match in matches[0]:
                    chunks = match.lower().split(" ")
                    if len(chunks) != 2:
                        continue

                    num, stat = chunks
                    if line.startswith("EVs:"):
                        mon.stats[stat]["ev"] = int(num)
                    elif line.startswith("IVs:"):
                        mon.stats[stat]["iv"] = int(num)

                continue

            # fires for other props
            matches = re.findall(self.prop_reg, line)
            if len(matches):
                if matches[0][0] == "Ability":
                    mon.ability = matches[0][1]
                elif matches[0][0] == "Tera Type":
                    mon.tera = matches[0][1]
                elif matches[0][0] == "Shiny":
                    mon.shiny = True if matches[0][1] == "Yes" else False

                continue

            # should fire for just moves
            matches = re.findall(self.move_reg, line)
            if len(matches):
                if len(matches[0][2]):
                    mon.moves.append(matches[0][2])

                continue

        return mons
