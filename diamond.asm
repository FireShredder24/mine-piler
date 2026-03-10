#
# Diamond-plotting program for Minecraft redstone computer
#
LDI r15 4 # iteration limit
COPY r5 r15 # current loop index
#
LDI r1 4 # starting x coordinate
LDI r2 7 # starting y coordinate
LDI r3 1 # x increment
LDI r4 0b11111111 # y increment (evaluates to -1)
#
# This assumes a display that monitors the draw/clear register for any writes.
# If it is nonzero after a write it will turn the pixel on, 
# If it's zero it will turn the pixel off.
#
LDI r10 0 # Display X address
LDI r11 1 # Display Y address
LDI r12 2 # Display draw/clear signal address
#
# Loop start
#
.loop
DRAW r10 r1 # Send the X coordinate to the display
DRAW r11 r2 # Send the Y coordinate to the display
DRAW r12 r15 # r15 is always nonzero so we'll use it to draw
ADD r1 r1 r3 # increment X coordinate
ADD r2 r2 r4 # increment Y coordinate
SUB r5 r5 r11 # Subtract 1 from the loop index (r11 is constant)
BIZ r5 !loop 
