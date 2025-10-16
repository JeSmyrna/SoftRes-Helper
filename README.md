# SoftRes-Helper
privat project working on a SR+ sheet helper

This program can now manage users and their alts.
- Add player, Add character to player
- Delete player or Delete character alt
- print the whole dictionary to show all the players and their characters

Tool can now manage SR+ sheets in form of csv files.
- Create new sheets (Do that for first time users), fill with column names
- print the whole sheet to show all the SR+ of every player.
  Will show you the last 6 raid days attendance, if sheet has to many raid days recorded
- export to google spread sheet (currently not working)

SR+ Sheet - Make New Entry
- make new entry (reads raidres export, attendeese and lootlog), asks if you have updated those files.
- It then looks who was there in attendeese and gets the soft reserve from the raidres
- It checks if player exists in player dictionary and asks you to add them. Either as player or alt.
- It checks if an alt of player already has a SR+ in this sheet and asks if you wanna replace the current SR+
  if they haven't reserved the same items. Will move it to the log file with a note 'replaced'
- It checks if player is not yet in the Sheet and you can choose what to put in (item 1, item 2, nothing)
  Note: "Nothing" is for players who don't want anything or have reserved a mount.
        So the tool wont ask you to add this character everytime.
- Checks if players reserved same item to not loose their SR+
- Asks you to give it a date (recommended) to name the new column entry
- It checks after this the lootlog to see if anyone has got their SR+
- if thats the case it asks you if you wanna move it to the log file
- After everything it will fill anyones attendance for the day with (absent/present)
  and calc the new bonus roll for next raid

Manual editing:
- add new player manually and fill all days with empty attendance
- delete player from sheet, move it to the logfile with the note 'deleted'
- award a player the SR+ and move it to the logfile
- award through loot log again, if needed

This program is hardcoded for the loot rules of Stonewall Inn.
- for every 2 weeks of not attending adds -5 to the Bonusroll
- 2 SR for each raid, one of them is the SR+ and has to be always the same, even attending with an alt
- no double SR
- no SR+ on mounts (can be ignored with this tool)

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
- enter the "raid date" what "raid" and save a log [x]
- check if one of the players got their SR+ loot, push the entry to a log [x]
- delete player from SR+ Sheets [x]
- add to the bonus roll [x]
- check the soft reserved items with the sheet to see if any player changed their SR+ : reset bonus roll to 0 [x]
- check the loot tracker to see which player got their SR+, manual confirmation [x]
- check when the player attended raid, if longer than 2 weeks : Bonus roll -5 [x]
- edit player entries: SR+ Item, prev rolls, days attended (Bonus roll gets automatically calculated, so no edit possible) [ ]
- use the function for replacing character names with player names, to just search for player names to clarify, if player already have an SR+ [x]
- check if players changed their SR+ via raidres, ask user if player changed SR+, reset SR+ and only give the newest day as bonus. [x]
- manual make copy [ ]
- if 'nothing' is reserved still record attendance but don't calculate bonus roll [x]

- export to csv [x]
- export to google sheet [?] no idea why it broke
- style the sheet for readability [x]

SQL Databank connection: [?]
- can do, not yet sure if needed. Sticking with base functions
