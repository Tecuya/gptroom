#!/usr/bin/env python3

import logging
import openai
import dirtyjson

logger = logging.getLogger(__name__)

prompt_template = """Consider this json: `[{id: 1, name: "West Hall", desc: "You are in the west hall.", exits: [{room_id: 2, dir: "east"}]},{id: 2, name: "East Hall", desc: "You are in the east hall", exits: [{room_id: 1, dir: "west"}]}]`  This json format can power a small text adventure game that lets the player explore interconnected rooms.  The player starts in room id 1.  Using this same format, design a small set of rooms according to this prompt "TARGET".  compose your response using minified json.  return ONLY the json and nothing else."""

def target_to_json(target: str):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt_template.replace("TARGET", target),
        max_tokens=2048,
    )

    response_text = response.choices[0].text
    pieces = response_text.split('`')

    for p in pieces:
        try:
            d = dirtyjson.loads(p.strip())
            return d
        except Exception:
            # logger.exception('Could not load chunk')
            pass
    else:
        print('None of these returned data was usable:',pieces)
        return None

rooms = [{"id": 1, "name": "Welcome", "desc": "Use /teleport to visit a world of your choosing.\n\nExample: `/teleport an enchanted forest filled with riddles and mystery`.\n\nIf you get a bad result, just try again."}]

current_room_id = 1
while True:
    current_room = next(r for r in rooms if r.get('id') == current_room_id)
    print(current_room.get('name'))
    print(current_room.get('desc'))
    print("Exits: ",list(x.get('dir') for x in current_room.get('exits', [])))
    cmd = input("> ")

    cmd_pieces = cmd.split(' ')
    if cmd_pieces[0] == '/teleport':
        new_rooms = target_to_json((' '.join(cmd_pieces[1:])).strip())
        if new_rooms is not None:
            rooms = new_rooms
            current_room_id = 1
        else:
            print('Teleport failed')
        continue

    if cmd_pieces[0] == '/json':
        print(rooms)
        continue

    matched_exit = next((x for x in current_room.get('exits', []) if x.get('dir') == cmd), None)
    if matched_exit is None:
        print('Where?')
    else:
        current_room_id = matched_exit.get('room_id')
