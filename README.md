## Welcome to Grocery4's Minecraft Coordinate tracker!
This is my first ever almost-seriously developed web-app, created in Python using the Flask framework!
For this very reason I invite you to keep in mind that most features will surely be very primitive and often
very buggy.

## With that being said, here are the main features and usage:

### 1. Basic form application to insert the location of interest and coordinates.
Usually the Y coordinate is omitted, but currently there's no check to determine if X and Y coordinates
are inserted.

### 2. Display list of inserted entries.
The list of coordinates is being managed by a very simple database table. At the moment there is
no way to hide/unhide coordinates, and every player can delete eachother's coordinates.
This application was made to be used among friends; nonetheless, I'm working on giving a choice
wether to display publicly or privately every coordinate.

## Work in progress:

### 1. Login | Register
To identify who inserted what, an account must be made, guests won't be able to add nor remove anything.

### Public vs Private coordinates
As cited before, I'm working on creating a system where the player is able to choose wether to show
to anyone the coordinate set, or to make it private or visible only to certain players.