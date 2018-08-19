"""
This file exists to hold functions/classes related to creating scenes
"""

import json

def create_scenes(game, character, x, y, source):
    scenes = []
    with open('./rvb/game_data/encounters/{s}.json'.format(s=source)) as j:
        scripts = json.load(j)

    for script in scripts:
        scenes.append(
            create_scene(
                title=script["title"],
                text=script["text"],
                type=script["type"],
                **script["data"]
                )
            )
    return scenes

def create_scene(title, text, type, options=None, effects=None, results=None, skill=None):
    scene = {
        "title": title,
        "text": text,
        "type": type,
    }

    if type == 'choice':
        scene["options"] = []
        assert (options and len(options) > 0),"No options supplied for scene of type choice!"
        for option in options:
            scene["options"].append(create_option(option["text"], option["go_to"], option["id"]))
    elif type == 'skill':
        scene["results"] = []
        scene["skill"] = skill
        scene["rolled"] = False
        assert (results and len(results) > 0),"No results supplied for scene of type skill!"
        count = 0
        for result in results:
            scene["results"].append(create_result(result["text"], result["effects"], result["go_to"], result["range"], count))
            count += 1
    elif type == 'resolution':
        scene["effects"] = []
        scene["messages"] = []
        for effect in effects:
            scene["effects"].append(create_effect(effect["func"], effect["inputs"]))
    elif type == 'combat':
        pass

    return scene

def create_option(text, go_to, option_id, **kwargs):
    option = {
        "id": option_id,
        "text": text,
        "outcome": create_outcome(go_to)
        }
    return option

def create_outcome(scene_id):
    outcome = {
        "go_to": scene_id
    }

    return outcome

def create_result(text, effects, go_to, range, count):
    result = {
        "id": count,
        "text": text,
        "effects": [create_effect(effect["func"], effect["inputs"]) for effect in effects],
        "go_to": go_to,
        "range": range
    }

    return result

def create_effect(func, inputs):
    effect = {
        "func": func,
        "inputs": inputs
    }

    return effect

# x=0
# y=0
# scenes = create_scenes("mountain",x,y)
# print(scenes)
