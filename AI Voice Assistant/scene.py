import asyncio

"""Definition of the supported bulb effects."""

from typing import Dict, Iterable, List, cast

from pywizlight.bulblibrary import BulbClass

# Ordered by name and not by ID
SCENES = {
    35: "Alarm",
    10: "bedtime",
    29: "candle light",
    27: "Christmas",
    6: "cozy",
    13: "Coolwhite",
    26: "Club",
    12: "Daylight",
    33: "Diwali",
    23: "deep dive",
    22: "Fall",
    5: "Fireplace",
    7: "Forest",
    15: "Focus",
    30: "golden white",
    28: "Halloween",
    24: "Jungle",
    25: "Mojito",
    14: "Night",
    1: "Ocean",
    4: "Party",
    31: "Pulse",
    8: "Pastel",
    19: "plant growth",
    2: "Romance",
    16: "Relax",
    36: "snowy sky",
    3: "Sunset",
    20: "Spring",
    21: "Summer",
    32: "Steam punk",
    17: "Truecolors",
    18: "tv time",
    34: "White",
    9: "Wake-up",
    11: "Warm white",
    1000: "Rhythm",
}
SCENE_NAME_TO_ID = {scene_name: scene_id for (scene_id, scene_name) in SCENES.items()}
TW_SCENES = [6, 9, 10, 11, 12, 13, 14, 15, 16, 18, 29, 30, 31, 32, 33, 35]
DW_SCENES = [9, 10, 14, 29, 31, 32, 34, 35]

SCENES_BY_CLASS: Dict[BulbClass, List[str]] = {
    BulbClass.RGB: list(cast(Iterable, SCENES.values())),
    BulbClass.TW: [SCENES[key] for key in TW_SCENES],
    BulbClass.DW: [SCENES[key] for key in DW_SCENES],
}


def get_id_from_scene_name(scene: str) -> int:
    """Return the id of an given scene name.

    :param scene: Name of the scene
    :raises ValueError: Return if not in scene list
    :return: ID of the scene
    """
    scene_id = SCENE_NAME_TO_ID.get(scene)
    if not scene_id:
        raise ValueError(f"Scene '{scene}' not in scene list.")
    return scene_id
#
def get_scene_id(user_input: str) -> int | None:
    """Return the scene ID if the name appears in user input."""
    try:
        user_lower = user_input.lower()
        for scene_id, scene_name in SCENES.items():
            if scene_name.lower() in user_lower:
                return scene_id
    except Exception as e:
        return None
    
async def get_available_scenes():
    return list(SCENES.values())

#
async def get_top_five_scenes(top_n: int = 5):
    """Return the first N available scenes (default = 5)."""
    return list(SCENES.values())[:top_n]