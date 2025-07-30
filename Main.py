import pygame
import serial
import random
import time


pygame.init()


#class
class TimeCount:
    def __init__(self):
        self.elapsed_time = 0
        self.timer = 0
       
        pass
    def Set_Time(self,_time):
        self.time = _time
        self.timer = _time
        self.lastTimer = timer
        self.start_tick = pygame.time.get_ticks()
    def Time_Count(self):
        
        self.elapsed_time = (pygame.time.get_ticks() - self.start_tick) / 1000
        self.timer = max(0,self.time - self.elapsed_time)
        self.lastTime = self.timer;
    def TimeUP(self):
        self.Time_Count()
        if self.timer <= 0:
            return True
        else:
            return False
    def Get_Timer(self):
        self.Time_Count()
        return self.timer


# Variables
WIDTH = 1360
HEIGHT = 768
running = True
fruit_size = 300
ramdom_fruit_name = "Grape"
wait_for_spin = False
elapsed_time = 0
timer = TimeCount()
state_time = 0
start_tick = 0
spin_count = 10
current_spin = 0
score = 0
grape_score = 0
tomato_score = 0
orange_score = 0
mistake_score = 0

game_time = 30
game_timer = TimeCount()

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (105, 247, 0)
fruit_names = [
    "Grape",
    "Tomato",
    "Orange"
]

fruit_map = {
    "G": "Grape",
    "T": "Tomato",
    "O": "Orange"
}
state = {
    "M":"MainMenu",
    "S":"SetUP",
    "SP":"Spin",
    "P":"Play",
    "G": "GameOver",
    "C": "Corrent",
    "IC": "Incorrent"
    
}

game_state = None
fruit_images ={
    name:pygame.image.load(f"{name}.png") for name in fruit_names
}

fruit_images_Fix_scale = {
    name: pygame.transform.scale(image,(fruit_size,fruit_size)) for name,image in fruit_images.items()
}

fruit_images = fruit_images_Fix_scale

menu_background = pygame.image.load("bg-startscene.png")
menu_background = pygame.transform.scale(menu_background,(WIDTH,HEIGHT))


# Load play background Image
back_ground = pygame.image.load("bg-gameplay.png")
back_ground = pygame.transform.scale(back_ground,(WIDTH,HEIGHT))

#Font
font_path = "CherryBombOne-Regular.ttf"
font_small = pygame.font.Font(font_path,36)
font_medium = pygame.font.Font(font_path,60)
font_large = pygame.font.Font(font_path,100)


# Initialize

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Fruit Game 2")
clock = pygame.time.Clock()


ser = None
try:
    ser = serial.Serial("COM5",115200,timeout=0.1) # Windows
    #ser = serial.Serial("/dev/ttyAPE0",baudrate=115200,timeout=0.1) # raspberry pi
except:
    print("Not Found Serial ")




def Micro_Bit_Serial():
    if not ser : return
    if game_state == state["M"]:
         if ser.in_waiting > 0:
            command = ser.readline().decode().strip()
            if command in fruit_map:
                Start_State(state["S"])
    elif game_state == state["P"]:
        if ser.in_waiting > 0:
            command = ser.readline().decode().strip()
            print(command)
            Check_Fruit(command)
    elif game_state == state["G"]:
        if ser.in_waiting > 0:
            command = ser.readline().decode().strip()
            if command in fruit_map:
                 Start_State(state["S"])






def Input_Test(_event):
    
    
    if game_state == state["M"]:
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_g or  _event.key == pygame.K_t or  _event.key == pygame.K_o:
               Start_State(state["S"])
    
    elif game_state == state["S"]:
        pass
    elif game_state == state["P"]:
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_g:
                Check_Fruit("G")
            if _event.key == pygame.K_t:
                Check_Fruit("T")
            if _event.key == pygame.K_o:
                Check_Fruit("O")
    elif game_state == state["G"]:
        if _event.type == pygame.KEYDOWN:
            if _event.key == pygame.K_g or  _event.key == pygame.K_t or  _event.key == pygame.K_o:
               Start_State(state["S"])
           
        pass

def Check_Fruit(_key):
    global score,grape_score,tomato_score,orange_score
    if not _key in fruit_map: 
        return
    
    # if ramdom_fruit_name == fruit_map[_key]:
    #     score += 1
    #     Start_State(state["C"])
    # else:
    #     score -= 1
    #     Start_State(state["IC"])
    
    if ramdom_fruit_name == fruit_map["G"]:
        grape_score += 1
        Start_State(state["C"])
    elif ramdom_fruit_name == fruit_map["T"]:
        tomato_score += 1
        Start_State(state["C"])
    elif ramdom_fruit_name == fruit_map["O"]:
        orange_score += 1
        Start_State(state["C"])
    else:
        mistake_score += 1
        Start_State(state["IC"])
def Draw_Fruit():
    if ramdom_fruit_name in fruit_names:
        screen.blit(fruit_images[ramdom_fruit_name],(WIDTH / 2 - fruit_size / 2,HEIGHT / 2 - fruit_size / 2 ))
     
def Random_Fruit():
    global ramdom_fruit_name
    priviout_fruit = ramdom_fruit_name
    while priviout_fruit == ramdom_fruit_name:
        ramdom_fruit_name = random.choice(fruit_names)
    


     
def Reset_Time():
    global state_time,timer,elapsed_time
    state_time = 0
    #timer = 0
    elapsed_time = 0



def Start_State(_newState):
    
    global game_state,state_time,current_spin
    global spin_count,game_timer,timer,score
    
   
    game_state = _newState
    
    if game_state == state["M"]:
        pass
    elif game_state == state["S"]:
        current_spin = 0
        game_timer.Set_Time(game_time)
        Reset_Time()
        score = 0
        Start_State(state["SP"])
    elif game_state == state["SP"]:
        current_spin = 0
        spin_count = random.choice([10,13,18])
        
    elif game_state == state["P"]:
        game_timer.Set_Time(game_timer.lastTimer)
        screen.fill(WHITE)
        Draw_Fruit()
    elif game_state == state["G"]:
        pass
    elif game_state == state["C"]:
        screen.fill(GREEN)
        #Set_Timer(1)
        timer.Set_Time(1)
        
    elif game_state == state["IC"]:
        screen.fill(RED)
        #Set_Timer(1)
        timer.Set_Time(1)
    
def Set_Timer(_time):
    global state_time,start_tick
    Reset_Time()
    state_time = _time
    start_tick = pygame.time.get_ticks()

def Get_Timer():
    global elapsed_time,timer
    
    elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
   # timer = max(0,state_time - elapsed_time)  
   
    return timer


# def DisplayScore():
#     #Grape
#     score_text = font_small.render(f"Score:{score}",True,BLACK)
#     score_rect = score_text.get_rect()
#     score_rect.center = (WIDTH *0.09,HEIGHT * 0.05)
#     screen.blit(score_text,score_rect)

def DisplayScore():
    #Grape
    score_text = font_small.render(f"{grape_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.19)
    screen.blit(score_text,score_rect)
    
    #Tomato
    score_text = font_small.render(f"{tomato_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.52)
    screen.blit(score_text,score_rect)
    
    #Orange
    score_text = font_small.render(f"{orange_score}",True,BLACK)
    score_rect = score_text.get_rect()
    score_rect.center = (WIDTH *0.09,HEIGHT * 0.84)
    screen.blit(score_text,score_rect)






def DiaplayTime():
    timer_text = font_medium.render(f"{int(game_timer.Get_Timer())}",True,BLACK)
    timer_rect = timer_text.get_rect()
    timer_rect.center = (WIDTH  - 150,80)
    screen.blit(timer_text,timer_rect)



def GameOver():
    screen.fill(BLACK)
  
    gameOver = font_large.render(f"Game Over",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 5))

    gameOver = font_medium.render(f"Score Sum: {(grape_score + tomato_score + orange_score) - mistake_score}",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 3))
    
    gameOver = font_medium.render("Touch Any Fruit To Play Again",True,WHITE)
    text_width, text_height = gameOver.get_size()
    screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 2))



def MainMenu():
    screen.blit(menu_background,(0,0))
  
    # gameOver = font_large.render(f"Fruit Game 2",True,WHITE)
    # text_width, text_height = gameOver.get_size()
    # screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 5))

   
    
    # gameOver = font_medium.render("Touch Any Fruit To Play ",True,WHITE)
    # text_width, text_height = gameOver.get_size()
    # screen.blit(gameOver,((WIDTH / 2) - (text_width / 2 ), HEIGHT / 2))




game_timer.Set_Time(game_time)
Start_State(state["M"])
while running:
    
    # pygame Event

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        Input_Test(event)

    if game_state == state["M"]:
        MainMenu()
        Micro_Bit_Serial()
    
    elif game_state == state["SP"]:
        
        screen.fill(YELLOW)
        if current_spin < spin_count and not wait_for_spin:
            Random_Fruit()
            current_spin += 1
            #Set_Timer(0.05)
            timer.Set_Time(0.05)
            wait_for_spin = True
        Draw_Fruit()
        if wait_for_spin and timer.TimeUP():
             wait_for_spin = False
        
        if current_spin >= spin_count:
            Start_State(state["P"])
        
    elif game_state == state["P"]:
        screen.blit(back_ground,(0,0))
       
        Micro_Bit_Serial()
        Draw_Fruit()
        DisplayScore()
        DiaplayTime()
        if game_timer.TimeUP():
            Start_State(state["G"])
    elif game_state == state["G"]:
        GameOver()
        Micro_Bit_Serial()
       
    elif game_state == state["C"]:
        # elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
        # timer = max(0,state_time - elapsed_time)
        
        # if tGetimer <= 0:
        #     Start_State(state["S"])
       
        if timer.TimeUP() :
            Start_State(state["SP"])
        
    elif game_state == state["IC"]:
        # elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
        # timer = max(0,state_time - elapsed_time)
        
        # if timer <= 0:
        #     Start_State(state["S"])
        if timer.TimeUP() :
            Start_State(state["SP"])
        
    



    pygame.display.flip()
   

    clock.tick(30)
pygame.quit()
if ser:
    ser.close()





