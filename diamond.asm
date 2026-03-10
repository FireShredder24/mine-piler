#
# Diamond-plotting program for Minecraft redstone computer
# 
# MANDATORY NOOP
NOOP
#
LDI r8 0 # overwriting logic fail detect register
#
LDI r15 4 # iteration limit
COPY r5 r15 # current loop index
#
LDI r1 4 # starting x coordinate
LDI r2 7 # starting y coordinate
LDI r3 1 # x increment
LDI r4 0b11111111 # y increment (evaluates to -1)
LDI r7 7 # maximum coordinate value
#
# This assumes a display that monitors the draw/clear register for any writes.
# If it is nonzero after a write it will turn the pixel on, 
# If it's zero it will turn the pixel off.
#
LDI r10 0 # Display X address
LDI r11 1 # Display Y address
LDI r12 2 # Display draw/clear signal address
#
# Main drawing loop
#
.draw
DRAW r10 r1 # Send the X coordinate to the display
DRAW r11 r2 # Send the Y coordinate to the display
DRAW r12 r15 # r15 is always nonzero so we'll use it to draw
ADD r1 r1 r3 # increment X coordinate
ADD r2 r2 r4 # increment Y coordinate
SUB r5 r5 r11 # Subtract 1 from the loop index (r11 is constant)
BIZ r5 !bounce # exit current loop and change increments if index is zero
JUMP !draw # otherwise keep drawing
.bounce
SUB r6 r1 r7 # checking equal to 7
BIZ r6 !bounceleft
BIZ r1 !bounceright
SUB r6 r2 r7 # checking equal to 7
BIZ r6 !bouncedown
BIZ r2 !bounceup
LDI r8 255 # print bruh moment if we failed
.bounceleft
LDI r3 0b11111111
JUMP !draw
.bounceright
LDI r3 1
JUMP !draw
.bouncedown
LDI r4 0b11111111
JUMP !draw
.bounceup
LDI r4 1
JUMP !draw
