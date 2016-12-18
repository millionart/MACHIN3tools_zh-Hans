# Center Cube

If nothing is selected, places a cube at the cursor location, but with X zeroed out, enters edit mode, selects all and initiates the scale tool. If objects are selected, it zeroes out x.
This allows for quick, precise additions and alignment of geometry, without having to manually center them on the x axis using the N panel.

Default Key: Shift + C  
Video Demonstration: https://twitter.com/machin3io/status/806963166404087808  

# Cleans Up Good
All at once: removes doubles, deletes loose vertices and edges, dissolves degenerates, recalculates normals, removes 2-edged vertices, selects non-manifold geometry.
To be used frequently while modeling, to keep everything clean, tidy and working.   
Cleans Up Good can be called in edit mode and object mode, including on a selection of objects. By default, the keyboard shortcut will only work in edit mode.
Access the sript from the spacebarmenu in that case, or set the 'objectmodeshortcut' switch to true, to make the clean up shortcut work in edit and object mode. 

The script also exposes the "Remove 2-edged vertices" class seperatedly, to be called via the spacebar menu, should that be desired.
Set "auto2edged" to False, if you don't want it to run with each clean up. There will be a delay with heavy geometry.

Default Key: 3  
Video Demonstration: https://twitter.com/machin3io/status/810309079075848193  


# Clipping Plane Toggle

This script allows for quick toggling through 3 different clipping plain values. Useful when you need to get very close to some vertices, or when you need to see and select through overlapping geometry. Toggle back to a bigger valuei, when you are zoomed out again, to avoid "bleeding edges" on the bounderies of your objects or viewport AO creating a moire pattern.
The clipping values will also influence how close "View Selected" will focus on your selection.


Default Key: Mouse Button 5  
Video Demonstration: https://twitter.com/machin3io/status/805790547889844224


# Focus
Disables all Mirror modifiers of the selected objects, then enters local view. Re-enables mirror modifiers again, when exiting local view.

Default Key: CTRL + F  
Video Demonstration: https://twitter.com/machin3io/status/806936075784462336 


# Light Switch

Useful when working in changing light situations, but also handy when cleaning up edges after boolean operations, to get a fresh look at your model and re-evaluate it in different "light conditions" or just to better see dark mesh areas.

Set up the theme folder as well as the themes and matcaps you want to use in the script.

Default Key: CTRL + Mouse Button 5  
Video Demonstration: https://twitter.com/machin3io/status/805770460755595264
 

# Multi Mirror Mirror
This script wraps around Rob Fornof's excellent Mirror Mirror Tool(https://github.com/fornof/BlenderAddons/blob/master/MirrorMirrorTool.py) and adds support for mirroring a selection of objects at once.

Default Key: Shift + Alt + X/Y/Z  
Video Demonstration: https://twitter.com/machin3io/status/807718239044300800  

# Shading Switch
Switches between Material and Solid shading modes. Also re-assigns Z key for wireframe switching, and Shift + Z for render switching dynamically according to the current shading mode.
This allows for consistent use of the Z and Shift + Z keys across those two shading modes. 

Default Key: Shift + Mouse Button 5   
Video Demonstration: https://twitter.com/machin3io/status/810133309497999360  
