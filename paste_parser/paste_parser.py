
from __future__ import annotations

import re

from paste_parser.pokemon import Pokemon

"""
Parses a pokepaste (pass the raw text of the paste) into a somewhat usable format
"""

class PasteParser:

    def __init__(self):
        # slightly awkward regexes from the pokepaste source
        self.main_reg = r"^(?:(.* \()([A-Z][a-z0-9:']+\.?(?:[- ][A-Za-z][a-z0-9:']*\.?)*)(\))|([A-Z][a-z0-9:']+\.?(?:[- ][A-Za-z][a-z0-9:']*\.?)*))(?:( \()([MF])(\)))?(?:( @ )([A-Z][a-z0-9:']*(?:[- ][A-Z][a-z0-9:']*)*))?( *)$"
        self.move_reg = r"^(-)( ([A-Z][a-z\']*(?:[- ][A-Za-z][a-z\']*)*)(?: \[([A-Z][a-z]+)\])?(?: / [A-Z][a-z\']*(?:[- ][A-Za-z][a-z\']*)*)* *)$"
        self.stat_reg = r"^[I|E]Vs: (\d+ HP)?( / )?(\d+ Atk)?( / )?(\d+ Def)?( / )?(\d+ SpA)?( / )?(\d+ SpD)?( / )?(\d+ Spe)?( *)$"


    def parse(self, paste:str) -> list:
        mons = []

        paste = paste.split("\n")

        paste.append("\n")

        mon = Pokemon()

        for line in paste:
            line = line.strip()

            # As One is messing with the nickname part of the regex
            # "As One (Spectrier)" which needs to be fixed at some point
            if line.startswith("Ability: As One"):
                line = "Ability: As One  "

            if len(line) == 0:
                if not len(mon.species):
                    continue

                mons.append(mon)

                mon = Pokemon()
                continue

            # this fires for most lines
            matches = re.findall(self.main_reg, line)
            if len(matches):
                if len(matches[0][1]): # species is here if there's a nickname
                    mon.species = matches[0][1]
                    mon.nickname = matches[0][0][0:-2] # nicknames have ' (' at the end
                if len(matches[0][8]):
                    mon.item = matches[0][8]
                if len(matches[0][3]):
                    if matches[0][3].startswith("Ability: "):
                        _, mon.ability = matches[0][3].split(': ')
                    elif matches[0][3].startswith("Tera Type: "):
                        _, mon.tera = matches[0][3].split(': ')
                    elif matches[0][3].startswith("Shiny: "):
                        _, mon.shiny = matches[0][3].split(': ')
                    elif matches[0][3].endswith(" Nature"):
                        mon.nature, _ = matches[0][3].split(' Nature')
                    else:
                        mon.species = matches[0][3] # if there's no nickname species is here!

                continue
            
            # should fire for just moves
            matches = re.findall(self.move_reg, line)
            if len(matches):
                if len(matches[0][2]):
                    mon.moves.append(matches[0][2])

                continue

            # fires for stats
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

        return mons
