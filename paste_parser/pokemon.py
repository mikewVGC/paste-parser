
from dataclasses import dataclass, field

"""
represents a single Pokemon
"""

@dataclass
class Pokemon():

    species:str = ""
    nickname:str = ""
    gender:str = ""
    item:str = ""
    ability:str = ""
    moves:list = field(default_factory=list)
    shiny:bool = False
    nature:str = ""
    tera:str = ""

    stats:dict = field(default_factory=lambda: {
        "hp": { "iv": 32, "ev": 0 },
        "atk": { "iv": 32, "ev": 0 },
        "def": { "iv": 32, "ev": 0 },
        "spa": { "iv": 32, "ev": 0 },
        "spd": { "iv": 32, "ev": 0 },
        "spe": { "iv": 32, "ev": 0 },
    })
