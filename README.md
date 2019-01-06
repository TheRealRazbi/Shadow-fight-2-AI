# Shadow-fight-2-AI
This project is about a DQN agent trying to play Shadow Fight 2 using visual input.

[First of all , I'm not a native english speaker so I'm sure there are mistakes]

## Status :

File1 : working 

File2 : working

Example : [This is just an example of a working DQN that works on the cartpole game using openai gym] working


Screen_Grabber : working [not made by me btw]


## Usage:

### File 1 : It has been tested on an 1080p resolution and not any other resolution , not sure if it works. Open bluestacks and open it in the smallest possible size then open the game. With file1 you can test the already working functions , from detecting the timer , if the round is paused, hp bars.



### File 2 :  With file2 is the actually AI kinda working , you will have to setup a save dir at the end of the file [Also the model is 2GB per save and it saves when it finishes the episodes] Each episode = 1 round in game and a round is recognized if it sees it's start. Only the latest model will be used [with the highest amount of episodes not necesary the newest] .


#### Update : Added auto-save and auto-load and can be easily changed, changed epsilon based on the episodes played already


### Example : working , but has no use more than an example in case I mess up the file2

### Screen_Grabber : it's obvious what it does

#### Update : now you can specify the color of the image
