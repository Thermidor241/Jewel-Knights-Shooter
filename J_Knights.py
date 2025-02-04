import pygame
import math
import sys
import random
import time

pygame.mixer.pre_init(buffer=1024)
pygame.init()
pygame.mixer.set_num_channels(30) 
running = True  # Flag to control the main loop
# Set up the screen
score = 0
screen = pygame.display.set_mode((800, 800),pygame.FULLSCREEN)
pygame.display.set_caption("Pygame Example")
pygame.mixer.music.load('Music/Title.mp3')

#Other
#rogue = pygame.image.load('sprite.png').convert_alpha()
fish = pygame.image.load('Player/JK-13_Sprite.png').convert_alpha()
bullet_im = pygame.image.load('Player/JK_Buster.png').convert_alpha()
ebullet_im = pygame.image.load('Enemies/E_bullet.png').convert_alpha()
bug = pygame.image.load('Enemies/Bug_Bot.png').convert_alpha()
bom = pygame.image.load('Enemies/Bomb_Bot.png').convert_alpha()
clock = pygame.time.Clock()

# Ost
pygame.mixer.music.load('Music/Stage_1.mp3')
confirm_sound = pygame.mixer.Sound('Sounds/Select_Sound.wav')
shoot_sound = pygame.mixer.Sound('Sounds/Pew_Pew.wav')
boom = pygame.mixer.Sound('Sounds/Boom.wav')
hurt = pygame.mixer.Sound('Sounds/Damage.wav')
#Text stuff
t_font = pygame.font.Font('font.otf',25)
size = (80,80)
esizea = (65,65)
ebsize = (35,35)
bsize = (40,40)
#rogue = pygame.transform.scale(rogue,size)
fish_img = pygame.transform.scale(fish,size)
bullet_img = pygame.transform.scale(bullet_im,bsize)
ebullet_img = pygame.transform.scale(ebullet_im,ebsize)
bug_img = pygame.transform.scale(bug,esizea)
bom_img = pygame.transform.scale(bom,esizea)
#fishrec = fish_img.get_rect(midbottom = (80,400))
R_x_pos = 600

def show_title_screen():
    title_font = pygame.font.Font('font.otf', 50)
    title_text = title_font.render("JEWEL KNIGHTS", True, (255, 255, 255))
    start_font = pygame.font.Font('font.otf', 30)
    start_text = start_font.render("Press Enter to Start", True, (255, 255, 255))
    pygame.mixer.music.load('Music/Title.mp3')
    pygame.mixer.music.play(-1)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start
                    pygame.mixer.Sound.play(confirm_sound)
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load('Music/Stage_1.mp3')
                    return
                if event.key == pygame.K_ESCAPE:  # Press Enter to start
                    pygame.quit()
                    sys.exit()
        
        screen.fill((255, 200, 0))  # Clear the screen with yellow
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, screen.get_height() // 2 - title_text.get_height() // 2 - 50))
        screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, screen.get_height() // 2 + 20))
        pygame.display.flip()
        clock.tick(60)
def game_over(score):
    pygame.mixer.music.unload()
    pygame.mixer.music.stop()
    font = pygame.font.Font('font.otf', 100)
    hi_score = score
    text = font.render("GAME OVER", True, (0, 255, 255))
    text2 = font.render("Score : " + str(hi_score),True,(0, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Press Enter to start
                    pygame.mixer.Sound.play(confirm_sound)
                    pygame.mixer.music.load('Music/Stage_1.mp3')
                    main_game_loop()
                if event.key == pygame.K_ESCAPE:  # Press Enter to start
                    pygame.quit()
                    sys.exit()
        
        screen.fill((255, 0, 0))  # Clear the screen with red
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2 - 50))
        screen.blit(text2, (screen.get_width() // 2 - text2.get_width() // 2, screen.get_height() // 2 + 20))
        pygame.display.flip()
        clock.tick(60)

#BG Class
class BG():
    def __init__(self):
        self.bgimage =  pygame.image.load('Background/Stage_1.jpg').convert()
        self.rect_im = self.bgimage.get_rect()

        self.bgY1 = 0
        self.bgX1 = 0
 
        self.bgY2 = self.rect_im.height
        self.bgX2 = 0
 
        self.moving_speed = 8

    def update(self):
        self.bgY1 += self.moving_speed
        self.bgY2 += self.moving_speed
        if self.bgY1 >= self.rect_im.height:
            self.bgY1 = -self.rect_im.height
        if self.bgY2 >= self.rect_im.height:
            self.bgY2 = -self.rect_im.height
             
    def render(self):
         screen.blit(self.bgimage, (self.bgX1, self.bgY1))
         screen.blit(self.bgimage, (self.bgX2, self.bgY2))


#Background stuff


#JK Class
class JK(object):
    def __init__(self,x,y):
        self.health = 200
        self.bar = health_bar(self.health,200)
        self.coltime = 0
        self.immune = False
        self.frame_num = 0
        self.timesincehit = pygame.time.get_ticks()
        self.immunetime = 3000
        self.x = x
        self.y = y
        self.image = fish_img
        # This is the hitbox for JK
        self.hitbox = (self.x + 30, self.y + 20, 20, 20)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # List to keep track of bullets fired by 13
        self.bullets = []
        self.bullspeed = 15
        self.focus_speed = 5
        self.norm_speed = 15
        self.vel = self.norm_speed
        #Shootloop
        self.shootLoop = 0
        self.loopmax = 5
        
        
    def update(self):
         #Shoot loop to make sure the bullet glitch doesn't occur
        if self.shootLoop >= 0:
            self.shootLoop += 1
        if self.shootLoop > self.loopmax:
            self.shootLoop = 0
        # Update position
        self.hitbox = (self.x + 30, self.y + 20, 20, 20)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Clamp the rect to stay within screen bounds
        screen_rect = pygame.display.get_surface().get_rect()
        self.rect.clamp_ip(screen_rect)

        # Adjust player position based on clamped rect
        self.x, self.y = self.rect.topleft

        #JK controls   
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z] and self.shootLoop == 0:
            self.shoot()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            print(f"Moving Left: {self.x}, {self.y}")  # Debug statement

        if keys[pygame.K_RIGHT]:
            self.x += self.vel
            print(f"Moving Right: {self.x}, {self.y}")  # Debug statement

        if keys[pygame.K_UP]:
            self.y -= self.vel
            print(f"Moving Up: {self.x}, {self.y}")  # Debug statement

        if keys[pygame.K_DOWN]:
            self.y += self.vel
            print(f"Moving Down: {self.x}, {self.y}")  # Debug statement

            # Update player bullets
        for bullet in self.bullets[:]:
            if bullet.y > 0:
                bullet.y -= self.bullspeed
                bullet.rect.topleft = (bullet.x, bullet.y)
            else:
                self.bullets.remove(bullet)

        #Get her health bar
        self.bar = health_bar(self.health,200)
        #invincibility frames
        curent_time = pygame.time.get_ticks()
        if curent_time - self.timesincehit > self.immunetime:
            self.immune = False
    def draw(self,screen):
        draw_JK = True
        if self.immune:
            self.frame_num += 1
            draw_JK = self.frame_num % 4 == 0
        if draw_JK == True:
            self.hitbox = (self.x + 30, self.y + 20, 20, 20)
            pygame.draw.rect(screen, (255,0,0), self.hitbox,2) # To draw the hit box around the player
            screen.blit(self.image,(self.x,self.y))
        #Health_Bar
        #pygame.draw.rect(screen, (255,0,0), (10, 30, 300, 25))
        #pygame.draw.rect(screen, (0,255,0), (10, 30, 300, 25))
        #self.bar.draw(screen)
    def hit(self, num):
        if self.health > 0:
            hurt.play()
            self.health -= num
            self.immune = True
            self.timesincehit = pygame.time.get_ticks()
            #add flashing
    def shoot(self):
        if self.shootLoop < self.loopmax:
            shoot_sound.play()
            self.bullets.append(buster(round(self.x + 30), round(self.y -25)))
    def collided(self, sprite):
        # Check if this player's rect collides with the sprite's hitbox
        return self.rect.colliderect(sprite.hitbox)
            

#JK's Health Bar :3
class health_bar(object):
    def __init__(self,a,b):

        self.health = a
        self.max_health = b
        self.percent = (a / b)
        self.full = 1
        self.red = 0 + 255 * (1 - (255*self.percent))
        self.green = (255 * self.percent)
        self.blue = (self.full * 255)
        self.numbers = t_font.render( str(self.health) + " / " + str(self.max_health) ,1,(0,0,0))
        self.width = 300

    def update(self):
        self.percent = self.health / self.max_health
        self.percent = max(0, min(self.percent, 1))  # Ensure percent is within [0, 1]
        
        # Colors change from red (low health) to green (full health)
        self.red = int(255 * (1 - self.percent))  # Red decreases as health increases
        self.green = int(255 * self.percent)      # Green increases as health increases
        self.width = (300 * self.percent) 
        if (self.percent == 1):
            self.blue = 255
        else:
            self.blue = 0                             # Blue remains constant
        self.numbers = t_font.render( str(self.health) + " / " + str(self.max_health) ,1,(0,0,0))
        


        
    def draw(self,screen):
    #Health_Bar
        self.update()

        pygame.draw.rect(screen,(147,151,153), (0, 20, 320, 45))
        pygame.draw.rect(screen,(0,0,0), (10, 30, 300, 25))
        pygame.draw.rect(screen, (self.red,self.green,self.blue), (10, 30, self.width, 25))
        #screen.blit(self.numbers, (60, 30))

        

#Bullet Class
class buster(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.image = bullet_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self,screen):
        screen.blit(self.image,(self.x,self.y))
        self.rect.topleft = (self.x, self.y)  # Update rect position to match bullet's position
        #pygame.draw.rect(screen, (255,0,255), self.rect,2) 
    def collided(self, sprite):
        # Check if this bullet's rect collides with the sprite's hitbox
        return self.rect.colliderect(sprite.hitbox)
    

#Enemy Bullet Class
class buster_e(object):
    def __init__(self, x, y, vel_x, vel_y,angle):
        self.x = x
        self.y = y
        self.vel_x = vel_x * math.cos(math.radians(angle))
        self.vel_y = vel_y * math.sin(math.radians(angle))
        self.image = ebullet_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def draw(self, screen):
        self.x += self.vel_x
        self.y += self.vel_y
        screen.blit(self.image, (self.x, self.y))
        self.rect.topleft = (self.x, self.y)   #Update rect position to match bullet's position
        pygame.draw.rect(screen, (0, 255, 255), self.rect, 2)  # Optional hitbox visualization



    def collided(self, sprite):
        # Check if this bullet's rect collides with the sprite's hitbox
        return self.rect.colliderect(sprite.hitbox)
#Bug_Bot Class
class Bugbot(object):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.vel = 3
        self.image = image
        self.hitbox = pygame.Rect(self.x + 20, self.y + 2, 40, 60)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 50

        # Initialize the action interval and last action time
        self.action_interval = 2000
        self.last_action_time = pygame.time.get_ticks()
        
        # List to keep track of bullets fired by this Bugbot
        self.bullets = []

        self.shoot()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.hitbox = pygame.Rect(self.x + 20, self.y + 2, 40, 60)
        # pygame.draw.rect(screen, (255, 255, 0), self.hitbox, 2)  # Optional hitbox visualization

    def move(self):
        self.y += self.vel

    #def border(self):
        #if self.x <= 0 or self.x >= 1080:
         #   self.vel = -self.vel

    def update(self):
        # Check if the interval has passed
        current_time = pygame.time.get_ticks()
        if current_time - self.last_action_time > self.action_interval:
            self.shoot()
            # Set a new random interval and update the last action time
            self.action_interval = 2000
            self.last_action_time = current_time
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.y += bullet.vel_y  # Move the bullet according to its velocity in y direction
            bullet.x += bullet.vel_x  # Move the bullet according to its velocity in x direction
            bullet.rect.topleft = (bullet.x, bullet.y)
            if bullet.y > 800:
                self.bullets.remove(bullet)  # Remove bullets that go off-screen
            

    def shoot(self):

        angle = 30
        #Make a circle
        for x in range(4):
            if x == 2:
                angle += 30
            self.bullets.append(buster_e(self.x + 10, self.y + 60, -2, 4, angle))
            angle += 30
        # Create a downward bullet
        #self.bullets.append(buster_e(self.x + 10, self.y + 60, -2, 4))
        #self.bullets.append(buster_e(self.x + 10, self.y + 60, 2, 4))
        
        # Create diagonally downward bullets
        #self.bullets.append(buster_e(self.x + 20, self.y + 60, -4, 4))
        #self.bullets.append(buster_e(self.x + 20, self.y + 60, 4, 4))
    def hit(self):
        if self.health > 0:
            self.health -= 15

#Bomb_Bot Class

#Main loop

def main_game_loop():
    pygame.mixer.music.play(-1)
    global running  # Add this line to declare that we're using the global 'running'
    global score  # Add this line to declare that we're using the global 'score'

    running = True
    score = 0
    player = JK(500,700)
    

    #Bug_Bot stuff as a test
    bug_hive = []
    hive_timer = 0
    spawn_interval = 300
    #(random.randint(10,800))
    back = BG()

    while running:
        
        hive_timer+= 1

        if hive_timer >= spawn_interval:
            bug_hive.append(Bugbot((random.randint(200,800)),0,bug_img))
            hive_timer = 0
            spawn_interval = (random.randint(10,100))
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_LSHIFT:
                    player.vel = player.focus_speed
                    #loopmax = 3
                    print(f"Slowing down")
                    player.bullspeed = 25
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:  # Reset speed when key is released
                    player.vel = player.norm_speed
                    #loopmax = 5
                    player.bullspeed = 15

        #screen.blit(rogue,(R_x_pos, 300))
        #R_x_pos -= 3
        #if R_x_pos < -100 : R_x_pos = 800 

        

        # Update player bullets
        for bullet in player.bullets[:]:
            for bug in bug_hive[:]:
                if bullet.collided(bug):
                    player.bullets.remove(bullet)
                    score += 10
                    bug.hit()
                    if bug.health <= 0:
                        boom.play()
                        bug_hive.remove(bug)
                        score += 500
                    break
        # Update enemy bullets and check for collisions
        for bug in bug_hive:
            bug.update()  # Update Bugbot position and bullets 
            if player.collided(bug):
                if (player.immune == False):
                    player.hit(50)
                    if player.health <= 0:
                        running = False
                        game_over(score)
                    break
            if bug.y > 800:
                bug_hive.remove(bug)
            for bullet in bug.bullets[:]:
                if bullet.collided(player):
                    if (player.immune == False):
                        player.hit(15)  # Handle player hit by enemy bullet
                        if player.health <= 0:
                            running = False
                            game_over(score)
                        break
                    bug.bullets.remove(bullet)


        # Update game state
        #bg scroll

        back.update()
        back.render()
        player.draw(screen)
   
        for bug in bug_hive[:]:
            bug.draw(screen)
            bug.move()
            #bug.border()
            bug.update()
    
        for bullet in player.bullets[:]:
            bullet.draw(screen)

        for bullet in [b for bug in bug_hive for b in bug.bullets]:
            bullet.draw(screen)
        player.update()
        player.bar.draw(screen)
        s_board = t_font.render("Score: " + str(score),1,(0,0,0))
        screen.blit(s_board, (10, 70))
        pygame.display.update()
        clock.tick(60)
        pass

# Show title screen
show_title_screen()

# Start the main game loop
main_game_loop()

pygame.quit()
sys.exit()