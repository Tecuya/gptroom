#!/usr/bin/env python3

import logging
import openai
import json

from typing import Optional


logger = logging.getLogger(__name__)

default_messages = [{"role": "system", "content": """Consider this json: `[{"id":1,"name":"West Hall","desc":"You are in the west hall.","exits":[{"room_id":2,"dir":"east"}]},{"id":2,"name":"East Hall","desc":"You are in the east hall","exits":[{"room_id":1,"dir":"west"}]}]`  This json format is called simpleroom and it can power a small text adventure game that lets the player explore interconnected rooms.  The player starts in room id 1."""}]

messages = default_messages

def get_json_from_prompt(prompt) -> Optional[str]:

    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )


    message = response.get("choices")[0].message
    messages.append(message)

    # print('raw prompt',prompt)
    # print('raw response',message)

    for p2 in message.get("content").split('`'):
        for p in p2.split("\n\n"):
            try:
                d = json.loads(p.strip())
                return d
            except Exception:
                # logger.exception('Could not load chunk')
                pass

    print('None of these returned data was usable:',message)
    return None


def create_rooms(target: str):
    prompt_template = """Using simpleroom format, design a set of rooms according to this prompt "TARGET".  Compose your response using minified json."""
    return get_json_from_prompt(prompt_template.replace("TARGET", target))


def modify_rooms(prompt: str):
    return get_json_from_prompt("""Return the same world, but apply the following modification: PROMPT""".replace("PROMPT", prompt))


default_rooms = [{"id": 1, "name": "Welcome", "desc": "Use /t to visit a world of your choosing.\n\nExample: `/t new york city`.\n\nIf you get a bad result, just try again."}]

rooms = default_rooms
current_room_id = 1

while True:

    try:
        current_room = next(r for r in rooms if r.get('id') == current_room_id)
        print(current_room.get('name'))
        print(current_room.get('desc'))
        print("Exits: ",list(x.get('dir') for x in current_room.get('exits', [])))
    except Exception:
        print("rooms corrupted, resetting",rooms)
        rooms = default_rooms
        continue

    cmd = input("> ")

    cmd_pieces = cmd.split(' ')
    if cmd_pieces[0] == '/t':
        messages = default_messages
        new_rooms = create_rooms((' '.join(cmd_pieces[1:])).strip())
        if new_rooms is not None:
            rooms = new_rooms
            current_room_id = 1
        else:
            print('Teleport failed')
        continue

    if cmd_pieces[0] == '/r':
        print(rooms)
        continue

    if cmd_pieces[0] == '/m':
        new_rooms = modify_rooms((' '.join(cmd_pieces[1:])).strip())
        if new_rooms is not None:
            rooms = new_rooms
        else:
            print('Modify failed')
        continue

    matched_exit = next((x for x in current_room.get('exits', []) if x.get('dir') == cmd), None)
    if matched_exit is None:
        print('Where?')
    else:
        current_room_id = matched_exit.get('room_id')
