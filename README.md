# gptroom

## What?

A script to wander through fictional worlds created by chatgpt.

To run it you need `openai` library installed (`pip install openai`) and you
need to set the OPENAI_API_KEY env variable to a valid API key.

It'd be cool to extend it to auto-generate monsters and items and stuff.  I also think we could dynamically regenerate the rooms map in realtime so the player lives in some kind of ever-shifting version of the world they asked for in the prompt.

## Demo

```
sean@creosote:~/git/gptroom$ ./gptroom.py
Welcome
Use /teleport to visit a world of your choosing.

Example: `/teleport a detailed map of the starship enterprise`.

If you get a bad result, just try again.
Exits:  []
> /teleport a detailed map of the starship enterprise
Bridge
The bridge of the USS Enterprise NCC-1701-D.  Captain Picard presides from the captain's chair in the center of the room.
Exits:  ['east', 'north', 'southwest', 'south']
> south
Briefing Room
The Enterprise has a briefing room where the senior officers gather to discuss the ship's current mission.
Exits:  ['north']
> north
Bridge
The bridge of the USS Enterprise NCC-1701-D.  Captain Picard presides from the captain's chair in the center of the room.
Exits:  ['east', 'north', 'southwest', 'south']
> north
Turbolift
A turbo lift.  You can travel to any floor of the Enterprise from here.
Exits:  ['south', 'up', 'down']
> down
Sick Bay
The Enterprise's sick bay is where the ship's doctor treats the crew's injuries and illnesses.
Exits:  ['up']
> up
Turbolift
A turbo lift.  You can travel to any floor of the Enterprise from here.
Exits:  ['south', 'up', 'down']
> south
Bridge
The bridge of the USS Enterprise NCC-1701-D.  Captain Picard presides from the captain's chair in the center of the room.
Exits:  ['east', 'north', 'southwest', 'south']
> southwest
Main Engineering
Main engineering is where the ship's warp core is located.  Chief Engineer Geordi La Forge has his office here.
Exits:  ['northeast', 'south']
> south
Jeffries Tubes
Jeffries Tubes are the ship's maintenance ducts.  One can travel throughout the entire ship from here.
Exits:  ['north', 'east', 'west']
>

```
