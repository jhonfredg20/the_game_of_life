import pygame
import sys
import numpy as np
import time


def main():
    
    ### --- PyGame configurations --- ###
    
    # Initialize PyGame
    pygame.init() 
    
    # Width and height of the screen
    width, height = 800, 600

    # Creation of the screen
    screen = pygame.display.set_mode((width, height)) #

    # Background Color
    bg = 25, 25, 25

    # Paint the background
    screen.fill(bg)

    # Number of cells
    nxC, nyC = 70, 50

    # Size of cells
    dimCW = width / nxC
    dimCH = height / nyC

    # Cell status: Live = 1; Dead = 0
    status = np.zeros((nxC, nyC))

    # Pause or Run
    pause_run = False

    ### --- PyGame configurations --- ###


    ### --- Execution loop --- ###
    while True:
        
        # Copy status
        new_status = np.copy(status)

        # Events
        for event in pygame.event.get():
            # Quit The Game of Life
            if event.type == pygame.QUIT:
                sys.exit()
    
            # Pause or Run
            if event.type == pygame.KEYDOWN:
                pause_run = not pause_run

            # Mouse
            mouse_click = pygame.mouse.get_pressed()
            if sum(mouse_click) > 0:
                pos_x, pos_y = pygame.mouse.get_pos()
                x, y = int(np.floor(pos_x/dimCW)), int(np.floor(pos_y/dimCH))
                
                # new_status = np.abs(new_status[x, y] - 1)
                new_status[x,y] = not mouse_click[2]


        ### --- Logic Zone --- ###

        # Clean background
        screen.fill(bg)


        for y in range(0, nyC):
            for x in range(0, nxC):
                

                if not pause_run:

                    # Calculates the number of close neighbors
                    n_neigh = status[(x - 1) % nxC, (y - 1) % nyC] + \
                              status[(  x  ) % nxC, (y - 1) % nyC] + \
                              status[(x + 1) % nxC, (y - 1) % nyC] + \
                              status[(x - 1) % nxC, (  y  ) % nyC] + \
                              status[(x + 1) % nxC, (  y  ) % nyC] + \
                              status[(x - 1) % nxC, (y + 1) % nyC] + \
                              status[(  x  ) % nxC, (y + 1) % nyC] + \
                              status[(x + 1) % nxC, (y + 1) % nyC] 

                    # Rule #1 : A dead cell with exactly 3 living neighbors, "revives"
                    if status[x, y] == 0 and n_neigh == 3:
                        new_status[x, y] = 1

                    # Rule #2 : A living cell with less than 2 or more than 3 living neighbors, "dies"
                    elif status[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):
                        new_status[x, y] = 0

                # Creation of the polygons of each cell when drawing
                poly = [((x)   * dimCW,   (y) * dimCH),
                        ((x+1) * dimCW,   (y) * dimCH),
                        ((x+1) * dimCW, (y+1) * dimCH),
                        ((x)   * dimCW, (y+1) * dimCH)]
                
                # Draw the cell for each pair of x and y
                if new_status[x, y] == 1: 
                    pygame.draw.polygon(screen, (255, 255, 255), poly, width=0)
                else: 
                    pygame.draw.polygon(screen, (128, 128, 128), poly, width=1)


        # Update game status
        status = np.copy(new_status)

        ### --- Logic Zone --- ###


        # Update screen
        time.sleep(0.1)
        pygame.display.flip()
        
    ### --- Execution loop --- ###


if __name__ == '__main__':
    main()
