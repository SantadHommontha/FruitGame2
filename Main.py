import pygame
import serial
import random
import time

# Variables
WIDTH = 800
HEIGHT = 600
running = True
fruit_size = 50
ramdom_Fruit = None
wait_for_spin = False
# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

fruit_names = [
    "Banana",
    "Apple",
    "Orange"
]

fruit_images ={
    name:pygame.image.load(f"{name}.png") for name in fruit_names
}

fruit_images_Fix_scale = {
    name: pygame.transform.scale(image,(fruit_size,fruit_size)) for name,image in fruit_images.items()
}

fruit_images = fruit_images_Fix_scale

class Fruit:
    def __init__(self):
        pass


# Initialize
pygame.init()
screen = pygame.display.set_Mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Game 2")
clock = pygame.time.clock()





ser.serial.Serial("COM5",115200,timeout=0.1)


def spin_Image():
    global wait_for_spin ,ramdom_Fruit
    wait_for_spin = True

    for i in range(10):
        random_name = random.choice(fruit_names)
        screen.blit(fruit_images[random_name],(WIDTH / 2,HEIGHT / 2))
        pygame.display.flip()
        time.sleep(0.5)





while running:
    
    screen.fill(WHITE)


    spin_Image()





    # pygame Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(30)
pygame.quit()
ser.close()





