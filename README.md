# Transformers 2004 AP World
'Version 1.0'
This is the AP Client for integrating Transformers 2004 for PS2 into [Archipelago](https://archipelago.gg).

This must be used with the rebuilt game, as explained in the installation instructions below.

# Gameplay
There are a few options you can set in the YAML that will decide how much your experience changes from normal. That said, base play is the same, collect Minicons, defeat Unicron.

Normally, some locations are locked behind Commander, but in this you can set any difficulty and it will still spawn all locations.

Powerlinx will unlock based on the following criteria:
- Levels are Randomized and you do not start on Amazon, to make starting on a harder level more fair
- Completing Amazon, random levels or not

*Note*: For Archipelago Items, the item received <ins>wont</ins> be displayed in game. You will need to look at the client to see what was received.

## Goal
You have the option to decide between two goal options, Unicron and Bosses. Unicron just means beat Unicron as normal. Bosses means you must beat all level bosses before you can fight Unicron (Unicron will be locked behind minicons and bosses). Bosses is really only necessary if you randomize levels.

You also have the choice to set how many minicons you need to unlock Unicron. You can set it anywhere from 20 to 40 minicons. There are only 40 minicons in the game, period, so use your judgement.

## Added Items
There are a couple items added to the game to make archipelago work. 
- <ins>**Archipelago Minicon and Datacon**:</ins> Added as a placeholder for anything that isnt a minicon or datacon.
- <ins>**Health Refill**:</ins> Filler item that sets your health to full when collected
- <ins>**Big Head Mode**:</ins> Filler item that will toggle on the next time you go to HQ, and will turn off the next time you go to HQ after that.
- <ins>**Stealth Trap**:</ins> Trap item that will turn the enemies invisible for 30 seconds.
- <ins>**Freeze Trap**:</ins> Trap Item that will freeze the player for 10 seconds.
- <ins>**Level Unlocks**:</ins> Used mainly for level randomization, but preset to level completes when not randomized

## Randomization Options
There are a few options for randomization.
- <ins>**Trap Chance**:</ins> The percentage chance that a filler item is a trap item. Set to 0 for no traps
- <ins>**Add Starting Location**:</ins> Adds a starting location for the first level. Necessary if you want to randomize levels and start on starship, otherwise just adds an extra location.
- <ins>**Randomize Levels**:</ins> Randomizes the level you start on and adds level unlock items into the item pool, which can be anywhere, even in another players game. Also turns Boss Fights/Level completions into checks.
- <ins>**Randomize Stats**:</ins> Will randomize the Max Health, Height, Power Capacity, Dash Speed, and Powerlinx Regen of all 3 autobots within limits. These stats will be displayed in the client once you reach HQ for the first time. The names of the autobots will also change (for fun).
- <ins>**Randomize Minicon Levels**:</ins> Randomizes the power level each minicon uses.
- <ins>**Balance Minicon Levels**:</ins> Balances the random power levels so not all are super high or super low
- <ins>**Randomize Minicon Team Colors**:</ins> Randomizes the team color of each minicon. Minicons will still use their normal 3D model, but the icon in the hud and HQ will be colored to show the team color.
- <ins>**Balance Minicon Team Colors**:</ins> Balances the random team colors so not all or most are in one team color.
- <ins>**Visible Progression Items**:</ins> Makes Progression and Trap items for any game into Minicon Locations, while Useful and Filler items will be Datacon Locations. If off, items from other games will be Datacon locations, while any added items for this game will be Minicon Locations
- <ins>**Debug Mode**:</ins> Enables extra information to be printed to the Client to help track down bugs.

# Installation
You will need the following to use the AP World:
- A legally obtained ISO of the game (currently only the USA version is setup (SLUS-20668))
- PCSX2 and a legally obtained PS2 BIOS (will not be explaining how to do basic set up for PCSX2)
- [Exodus](https://darlingeclipseprogramming.com/Exodus/Exodus): Game Rebuilder and Randomizer
- 7-Zip

## Setting Up PCSX2 (PINE)
This client uses PINE, a built in communication method in PCSX2. To enable it, follow the instructions below:
1. Go to **Tools** and turn on **Show Advances Settings** if it is not already on
2. Go to '**System** -> **Settings**'
3. Go to the **Advanced** tab and scroll all the way down till you find the **PINE Settings**
4. Enable PINE and make sure the port is 28011 (Default)

It is also recommended that you right click 'Title' at the top of the game list, then check 'File Title' so you can tell the rebuilt game and original apart

## Setting Up Exodus
When you download Exodus, it will download in a .7z archive, so extract all of the contents into a folder of your choosing.

The first time you open Exodus, you will need to make a folder somewhere for it to extract all the files from the original ISO. This folder should not be where the normal ISO is stored. Then, at the top of the screen, go to '**Build**->**Unpack ISO**' and set the output to the folder you made. It should also ask for you to find where 7-Zip is installed. When this happens, go to 'C:\Program Files\7-Zip' and select the 7z.exe file. This will read the original ISO and copy all the files from it into a folder called 'Extract_Transformers (USA)' (name may be different based on the game version you use) inside the folder you created. **<ins>This only needs to happen once</ins>**

# How to Play
## Creating the Rebuilt ISO
1. Download the patch file (file extension '.aptf') from your Archipelago Room
2. Open Exodus and go to the '**Randomizer**' tab. If you get an error, its likely because you did not unpack the game first. You will know you did the setup right if you see a few files load on the left.
3. Select '**Import Placements**' and '**Automatically Build**', then if you have 'Add Starting Location' on, select '**Beginner Weapon**'
4. Press the '**Randomize**' Button. The first time, it will ask for an output Folder, and you can set it to the same folder as the one you made in setup.
5. You should be prompted to select the patch file you downloaded. This will unzip it into a folder as it imports it, so if you see the file and a folder with the same name, its normal.
6. You should then be prompted to select the original game ISO again. This allows Exodus to copy the files, then edit them based on the imported settings and any other adjustments made by Exodus.
7. The new ISO you need to run will be put into the same folder as the original ISO named '**Transformers (USA)_Rebuild.iso**' (name may be different based on the game version you use).

## Client
1. Run the rebuilt game in PCSX2. There will be a short delay of black screen before the transformers title appears, this is normal and part of running the rebuilt game.
2. Once you reach the main title, you can open the '**Transformers (2004) Client**' from the archipelago launcher. You can also wait till you are in HQ if you wish.
3. Connect to the Archipelago Server and input your slot name (and password if needed).
4. The client will then try connecting to PCSX2 through PINE. Once connected, and you are in HQ, the client will start writing the necessary memory adjustments and unlock your first level. If you have random stats on, it will also print the stats for each Autobot.
5. You can now play as normal.

If you need to quit and come back later, follow the same process as above. It will remember what minicons, datacons, and levels you had unlocked and unlock them, even if you start a new save or your save gets corrupted (shouldnt happen, but you never know with these things)

# Acknowledgements

**APWorld**
- **TheGreenTyphoon**: Getting PINE started and the Minicon Unlock Code
- **Eclipse**: PINE Memory Manager
- **Wirebot**: Logic and Client Code

**Game Mod/Rebuild**
- **Eclipse**: Created Exodus and All game modification
- **Wirebot**: Created Archipelago Minicon Model/Animation and Datacon Icon
- **bbats**: Created Blender VBIN Addon to import/export models and animations for the game
