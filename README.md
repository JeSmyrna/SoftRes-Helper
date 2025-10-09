# SoftRes-Helper
privat project working on a SR+ sheet helper

At the moment, this program only manages users and can give the intersect of players
who have put an SR in raidres and were present at raid

Current and future features:

Manage players and their characters:
- add new players [x]
- add new characters to said player [x]
- add new characters to existing players [x]
- delete players [x]
- delete characters [x]
- create table for different Raid SR+ Sheets [x]

Manage SR+ sheets:
- add players to SR+ Sheet with their SR+ [x]
- add players manually to SR+ Sheets [x]
- get the attendance [x]
- look for the received loot [x]
- enter the "raid date" what "raid" and save a log : Data\raidtable-name\date-raid-log.txt (intersection data) [x]
- check if one of the players got their SR+ loot, push the entry to a log [x]
- delete player from SR+ Sheets [x]
- add to the bonus roll [x]
- check the soft reserved items with the sheet to see if any player changed their SR+ : reset bonus roll to 0 [?]
- check the loot tracker to see which player got their SR+, manual confirmation [x]
- check when the player attended raid, if longer than 2 weeks : Bonus roll -5 [x]
- edit player entries: SR+ Item, prev rolls, days attended (Bonus roll gets automatically calculated, so no edit possible) [ ]
- use the function for replacing character names with player names, to just search for player names to clarify [ ]
- make copy function needs last day of the previous sheet, to calculate the decay -5 correct [ ]
- manual make copy [?]

- export to csv [x]
- export to google sheet [ ]
- style the sheet for readability [x]

SQL Databank connection: [?]
- can do, not yet sure if needed. Sticking with base functions (Priority Top to Bottom)
