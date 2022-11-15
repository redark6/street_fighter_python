# Street Fighter Python with AI project

Hi ! this repository contains a street fighter 2 "like" video game powered by AI, in its core, you will find a classic arcade fighter game with simple mechanics i.e. moving, simple punch, kick, longer range attack, parrying and jumping.
The point with this project is to train two AI (one for each character) that will enable them to engage in a fight and win it.
Each character has its own set of attack (namely different ranges for the same damage output) so it might be possible for one to come out better than the other.


# How to install

Download the IA branch and run the main.py file (requires python 3.10 or above) you will be prompted with the game interface in an IA vs player game mode (you can manually change it to go back to an IA vs IA game mode). The game comes with a pre generated Qtable wich will enable it to run smoothly without the need of training the AI model beforehand.

To change those settings, refer to How to change the settings section.

## Controls 
You will play Guile, the character at the left side of you screen, all sound effects referring to loosing or winning as well as the text message will be for your character.


### Xbox controller
![xbox controller mapping](https://media.discordapp.net/attachments/773113743034286081/1042186057220886528/image.png)

### keyboard
Q: go back
D: move forward
W: jump

R: kick
T: punch
Y: Range attack

## How to change the settings 

### Switch to AI vs AI or Player vs AI game mode
Set the PLAYER_PLAY boolean to FALSE if you want the IA vs IA gamemode or TRUE if you want the player vs IA gamemode

### Regenerate the Qtable: 
Lauch the game in AI vs AI gamemode then set LEARN_MODE boolean to "true" value (in main.py file)

### Controler vs keyboard gamemode
If you want to play with an XBOX gamepad (work on windows, not tested with other OS atm) simply plug it before launching the game, keyboard input will still be available
