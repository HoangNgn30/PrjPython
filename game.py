import pygame, sys, random
#Tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop =(500,random_pipe_pos-650))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
	for pipe in pipes :
		pipe.centerx -= 5
	return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 : 
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if shin_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if shin_rect.top <= -75 or shin_rect.bottom >= 650:
            return False
    return True 
def rotate_shin(shin1):
	new_shin = pygame.transform.rotozoom(shin1,-shin_movement*3,1)
	return new_shin
def shin_animation():
    new_shin = shin_list[shin_index]
    new_shin_rect = new_shin.get_rect(center = (100,shin_rect.centery))
    return new_shin, new_shin_rect
def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,630))
        screen.blit(high_score_surface,high_score_rect)
def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen= pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',35)
#Tạo các biến cho trò chơi
gravity = 0.3
shin_movement = 0
game_active = True
score = 0
high_score = 0
#chèn background
bg = pygame.image.load('assets/background.png').convert()
bg = pygame.transform.scale2x(bg)
#chèn sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
#tạo shin
shin_down = pygame.image.load('assets/downflap.png').convert_alpha()
shin_mid = pygame.image.load('assets/midflap.png').convert_alpha()
shin_up = pygame.image.load('assets/upflap.png').convert_alpha()
shin_list= [shin_down,shin_mid,shin_up] #0 1 2
shin_index = 0
shin = shin_list[shin_index]
#shin= pygame.image.load('assets/yellowshin-midflap.png').convert_alpha()
#shin = pygame.transform.scale2x(shin)
shin_rect = shin.get_rect(center = (100,384))

#tạo timer cho shin
shinflap = pygame.USEREVENT + 1
pygame.time.set_timer(shinflap,200)
#tạo ống
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list =[]
#tạo timer
spawnpipe= pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200,300,400]
#Tạo màn hình kết thúc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(216,384))
#Chèn âm thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
#while loop của trò chơi
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                shin_movement = 0
                shin_movement =-8
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True 
                pipe_list.clear()
                shin_rect.center = (100,384)
                shin_movement = 0 
                score = 0 
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == shinflap:
            if shin_index < 2:
                shin_index += 1
            else:
                shin_index =0 
            shin, shin_rect = shin_animation()    
            
    screen.blit(bg,(0,0))
    if game_active:
        #shin
        shin_movement += gravity
        rotated_shin = rotate_shin(shin)       
        shin_rect.centery += shin_movement
        screen.blit(rotated_shin,shin_rect)
        game_active= check_collision(pipe_list)
        #ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display('game_over')
    #sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
    
    pygame.display.update()
    clock.tick(60)
