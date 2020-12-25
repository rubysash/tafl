# raw code to display tafl board (7x7)
# future plans will have tokens moving around

import pygame	# the main workhorse
import os		# i KNOW I'll need to detect OS and handle paths, etc
import sys		# for sys.exit
import math 	# for square roots on hex, pi on circles

# allows us to use the == QUIT later instead of pygame.locals.QUIT
from pygame.locals import * 

# fixed colors not in pulse
WH = (255,255,255)	# white
BL = (0,0,0)		# black
GY = (128,128,128)	# grey
RE = (255,0,0)		# red

# this can be adjusted if you like
scale = 50  # 30-80 is probably best scale range
num_sq = 7	# must be multiple of 2

legs = num_sq		#
leg1 = legs / 8		# .875
leg2 = leg1 * 2 	#
leg3 = leg1 * 3		#
leg4 = leg1 * 4		#
leg5 = leg1 * 5
leg6 = leg1 * 6
leg7 = leg1 * 7
leg8 = leg1 * 8

ctr  = leg4	

offset = leg1/2

# relative game board size
W  = int(legs*scale)
H  = int(legs*scale)

lw = 3            # line width of polygons

#These are the pulse1 lines (base grid)
lines1 = {
	11 : [offset,offset,offset,leg4+leg3+offset],	# N2S1
	12 : [offset+leg1,offset,offset+leg1,leg7+offset],	#
	13 : [offset+leg2,offset,offset+leg2,leg7+offset],	#
	14 : [offset+leg3,offset,offset+leg3,leg7+offset],	#
	15 : [offset+leg4,offset,offset+leg4,leg7+offset],	#
	16 : [offset+leg5,offset,offset+leg5,leg7+offset],	#
	17 : [offset+leg6,offset,offset+leg6,leg7+offset],	#
	18 : [offset+leg7,offset,offset+leg7,leg7+offset],	#
	21 : [offset,offset,leg7+offset,offset],	# W2E1
	22 : [offset,leg1+offset,leg7+offset,leg1+offset],	#
	23 : [offset,leg2+offset,leg7+offset,leg2+offset],	#
	24 : [offset,leg3+offset,leg7+offset,leg3+offset],	#
	25 : [offset,leg4+offset,leg7+offset,leg4+offset],	#
	26 : [offset,leg5+offset,leg7+offset,leg5+offset],	#
	27 : [offset,leg6+offset,leg7+offset,leg6+offset],	#
	28 : [offset,leg7+offset,leg7+offset,leg7+offset],	#
}

# these are the pulse2 escape areas
lines2 = {
	31 : [offset,offset,offset+leg1,offset+leg1],	# NW \
	32 : [offset+leg1,offset,offset,offset+leg1],	# NW /
	33 : [offset+leg6,offset,offset+leg7,offset+leg1],	# NE \
	34 : [offset+leg6,offset+leg1,offset+leg7,offset],	# NE /
	35 : [offset+leg3,offset+leg3,offset+leg4,offset+leg4],	# CTR \
	36 : [offset+leg4,offset+leg3,offset+leg3,offset+leg4],	# CTR /
	37 : [offset,offset+leg6,offset+leg1,offset+leg7],	# SW \
	38 : [offset,offset+leg7,offset+leg1,offset+leg6],	# SW /
	39 : [offset+leg6,offset+leg6,offset+leg7,offset+leg7],	# SE \
	40 : [offset+leg6,offset+leg7,offset+leg7,offset+leg6],	# SE /
}


def main():
	# can't run pygame without init, just do it
	pygame.init()

	# clock required to limit fps
	FPS = pygame.time.Clock()

	# one of (possibly many) surfaces to draw on
	SURF = pygame.display.set_mode((W,H))

	# the title bar
	pygame.display.set_caption("Ard-Ri / Hnefatafl / Viking Chess (7)")

	# default colors start at black
	r1,g1,b1 = (0,0,0)
	r2,g2,b2 = (0,0,0)

	# used to pulse color
	flip_r1,flip_g1,flip_b1 = (1,1,1)
	flip_r2,flip_g2,flip_b2 = (1,1,1)

	#Game loop begins
	while True:
		# current color of pulse, r,g,b set at bottom of while 
		r1,flip_r1 = get_pulse(flip_r1,r1,1) # mix and match your pulse, red
		b2,flip_b2 = get_pulse(flip_b2,b2,5) # mix and match your pulse, red
		pulse1 = (r1,g1,b1)
		pulse2 = (r2,g2,b2)

		# fill our surface with white
		SURF.fill(GY)

		# event section
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:

				# update where we just clicked
				(x,y) = pygame.mouse.get_pos()

			if event.type == QUIT:
				# pygame has a buggy quit, do both
				pygame.quit()
				sys.exit()

		draw_board(SURF,pulse1,pulse2,lw)
		# update the screen object itself
		pygame.display.update()	# update entire screen if no surface passed

		# tick the fps clock
		FPS.tick(60)

'''
moved out to clean up the main()
can comment on/off to troubleshoot
'''
def draw_board(surf,pulse1,pulse2,lw):

	for xy in lines1:
		pygame.draw.line(surf, pulse1,
			(lines1[xy][0] * scale,lines1[xy][1] * scale),
			(lines1[xy][2] * scale,lines1[xy][3] * scale),
			lw
		)

	for xy in lines2:
		pygame.draw.line(surf, pulse2,
			(lines2[xy][0] * scale,lines2[xy][1] * scale),
			(lines2[xy][2] * scale,lines2[xy][3] * scale),
			lw
		)


'''
just pulse 255 to 0 back to 255 repeat 
set boundaries so we don't get invalid rgb value
input: state of the flip, and current color code
return: updated flip and color code
'''
def get_pulse(flipped,c,step):

	if flipped:
		if c < 255: c += step
		else:
			c = 255
			flipped = 0
	else:
		if c > step: c -= step
		else:
			c = 0
			flipped = 1

	if c > 255: c = 255
	if c < 0: c = 0

	return (c,flipped)



if __name__ == '__main__':
	# capture ctrl c
	try:
		main()
	except KeyboardInterrupt:
		# pygame has a buggy quit, do both
		pygame.quit()
		sys.exit()



