import sys
import pygame

pygame.init()

clock = pygame.time.Clock()
screen_width = 600
screen_height = 399
screen = pygame.display.set_mode((screen_width,screen_height))
Title = pygame.display.set_caption("Ping Pong")
background_image = pygame.image.load("assets/field.jpg")
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)

class BALL:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.ball_speed_x = 3
        self.ball_speed_y = 3
        self.paddle_hit = 0
        self.ball_img = pygame.image.load("assets/football.png")
    
    def draw_ball(self):
        self.ball = pygame.Rect(screen_width//2,screen_height//2,20,20)
        screen.blit(self.ball_img,(self.x-10,self.y-10))

    def move_ball(self):
        self.x += self.ball_speed_x
        self.y += self.ball_speed_y

class PADDLE:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.paddle_width = 23
        self.paddle_height = 150
        self.direction = 0
        self.speed = 25
        self.score = 0
        self.paddle_img = pygame.image.load("assets/paddle_1.jpg")
    
    def draw_paddle(self):
        self.paddle_rect = pygame.Rect(self.x ,self.y ,self.paddle_width ,self.paddle_height)
        screen.blit(self.paddle_img, self.paddle_rect)
    
    def rotate_img(self):
        self.angle = 90
        self.paddle_img = pygame.transform.rotate(self.paddle_img, self.angle)

    def move_paddle(self):
        self.y += self.direction
        self.direction = 0

class MAIN:
    def __init__(self):
        self.paddle_1 = PADDLE()
        self.paddle_2 = PADDLE()
        self.ball = BALL()
        self.sound = pygame.mixer.Sound("sound/ball-hits-paddle.mp3")
        self.place_arguements()

    def place_arguements(self):
        self.paddle_1.x = 0
        self.paddle_1.y = screen_height//2 - self.paddle_1.paddle_height
        self.paddle_1.paddle_img = pygame.image.load("assets/paddle_1.jpg")
        self.paddle_1.rotate_img()

        self.paddle_2.x = 602 - self.paddle_2.paddle_width
        self.paddle_2.y = screen_height//2 - self.paddle_2.paddle_height
        self.paddle_2.paddle_img = pygame.image.load("assets/paddle_2.jpg")
        self.paddle_2.rotate_img()

    def update(self):
        self.draw_objects()
        self.move_objects()
        self.check_paddle_collision()
        self.scoreInc()
        self.check_sideWall_fail()
        self.draw_result()

    def draw_objects(self):
        self.paddle_1.draw_paddle()
        self.paddle_2.draw_paddle()
        self.ball.draw_ball()

    def move_objects(self):
        self.paddle_1.move_paddle()
        self.paddle_2.move_paddle()
        self.ball.move_ball()

    def check_paddle_collision(self):
        horizon_p1 = self.paddle_1.paddle_width
        low_limit_p1 = self.paddle_1.y
        max_limit_p1 = self.paddle_1.paddle_height + low_limit_p1
        
        horizon_p2 = self.paddle_2.x - self.paddle_2.paddle_width
        low_limit_p2 = self.paddle_2.y
        max_limit_p2 = self.paddle_2.paddle_height + low_limit_p2

        if (self.ball.x <= horizon_p1) and (low_limit_p1 <= self.ball.y <= max_limit_p1):
            self.sound.play()
            self.ball.ball_speed_x = -1*self.ball.ball_speed_x
            self.ball.y += 2
            self.ball.paddle_hit += 1
        elif (self.ball.x >= horizon_p2) and (low_limit_p2 <= self.ball.y <= max_limit_p2):
            self.sound.play()
            self.ball.ball_speed_x = -1*self.ball.ball_speed_x
            self.ball.y += 2
            self.ball.paddle_hit += 1

    def check_sideWall_fail(self):
        if self.ball.y <= 0 or self.ball.y >= screen_height:
            self.ball.ball_speed_y = -self.ball.ball_speed_y
        elif (self.ball.x >= screen_width or self.ball.x <= 0):
            self.ball.ball_speed_x = -self.ball.ball_speed_x

    def scoreInc(self):
        if self.ball.paddle_hit != 0 and self.ball.x >= screen_width:
            self.paddle_1.score += 1
            self.ball.x = screen_width//2
            self.ball.y = screen_height//2
        elif self.ball.paddle_hit != 0 and self.ball.x <= (self.paddle_1.paddle_width//2):
            self.paddle_2.score += 1
            self.ball.x = screen_width//2
            self.ball.y = screen_height//2

    def draw_result(self):
        score_text = " SCORE A : "+str(self.paddle_1.score) + " || " +"SCORE B : " +str(self.paddle_2.score) +" "
        text_surface = game_font.render(score_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect()

        bg_surface = pygame.Surface(text_rect.size)
        bg_surface.fill((115,209,61))
        bg_surface.blit(text_surface, (0, 0))
        bg_rect = bg_surface.get_rect()
        bg_rect.center = (screen_width//2, 30)
        screen.blit(bg_surface, (bg_rect.centerx - bg_rect.width // 2, bg_rect.centery - bg_rect.height // 2))

main = MAIN()
while True:
    screen.fill((234,218,184))
    screen.blit(background_image, (0, 0))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                main.paddle_1.direction = -1*main.paddle_1.speed
            if event.key == pygame.K_s:
                main.paddle_1.direction = 1*main.paddle_1.speed
            if event.key == pygame.K_UP:
                main.paddle_2.direction = -1*main.paddle_2.speed
            if event.key == pygame.K_DOWN:
                main.paddle_2.direction = 1*main.paddle_2.speed

    main.update()
    pygame.display.update()