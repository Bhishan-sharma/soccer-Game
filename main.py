import pygame

pygame.init()

FPS = 60
clock = pygame.time.Clock()

stroke = 0

screen_width = 600
screen_height = 399

screen = pygame.display.set_mode((screen_width,screen_height))
Title = pygame.display.set_caption("Ping Pong")

background_image = pygame.image.load("assets/field.jpg")
paddle_1_img = pygame.image.load("assets/paddle_1.jpg")
paddle_2_img = pygame.image.load("assets/paddle_2.jpg")
ball_img = pygame.image.load("assets/football.png")
sound = pygame.mixer.Sound("sound/ball-hits-paddle.mp3")

angle = 90
paddle_1_img = pygame.transform.rotate(paddle_1_img, angle)
paddle_2_img = pygame.transform.rotate(paddle_2_img, angle)

font = pygame.font.Font(None, 36)

scoreA = 0
scoreB = 0
player = ""

text = font.render("ScoreA: {} || ScoreB: {}".format(scoreA,scoreB), True,(255, 255, 255))
resultText = font.render("PLAYER {} WON".format(player),True,(0,0,0))

paddle_width = 23
paddle_height = 150

paddle_1_x = 0
paddle_1_y = screen_height//2 - paddle_height

paddle_2_x = 600 - paddle_width
paddle_2_y = screen_height//2 - paddle_height

paddle_1 = pygame.Rect(paddle_1_x ,paddle_1_y ,paddle_width ,paddle_height)
paddle_2 = pygame.Rect(paddle_2_x ,paddle_2_y ,paddle_width ,paddle_height)
ball = pygame.Rect(screen_width//2,screen_height//2,20,20)

ball_speed_x = 3
ball_speed_y = 3

def movUp(a):
    if a == "w":
        paddle_1.y -= 40
    if a == "up":
        paddle_2.y -= 40

def movDown(a):
    if a == "s":
        paddle_1.y += 40
    if a == "Down":
        paddle_2.y += 40

def result():
    screen.blit(resultText, (screen_width // 2 - resultText.get_width() // 2,screen_height // 2 - resultText.get_height() // 2))
    run = False

def scoreBoard():
    text = font.render("ScoreA: {} || ScoreB: {}".format(scoreA,scoreB), True,(255, 255, 255))
    screen.blit(text, (screen_width // 2 - text.get_width() // 2,10))

def drawPaddles():
    pygame.draw.rect(screen,(0,0,0),paddle_1)
    pygame.draw.rect(screen,(0,0,0),paddle_2)
    screen.blit(paddle_1_img, paddle_1)
    screen.blit(paddle_2_img, paddle_2)

def drawBall():
    pygame.draw.ellipse(screen,(45,30,60),ball)
    screen.blit(ball_img,(ball.x-10,ball.y-10))

def ballMove():
    ball.x += ball_speed_x
    ball.y += ball_speed_y

def drawScreen():
    screen.fill((234,218,184))
    screen.blit(background_image, (0, 0))

run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                movUp("w")
            if event.key == pygame.K_s:
                movDown("s")
            if event.key == pygame.K_UP:
                movUp("up")
            if event.key == pygame.K_DOWN:
                movDown("Down")

    if ball.colliderect(paddle_1) or ball.colliderect(paddle_2):
        sound.play()
        stroke += 1
        ball_speed_x = -ball_speed_x
        ball.y += 2

    if ball.x >= screen_width and stroke > 0:
        scoreA += 1
        ball.x = screen_width//2
        ball.y = screen_height//2
    elif ball.x <= 10 and stroke > 0:
        scoreB += 1
        ball.x = screen_width//2
        ball.y = screen_height//2
    elif ball.y <= 0 or ball.y >= screen_height:
        ball_speed_y = -ball_speed_y
    elif stroke == 0 and (ball.x >= screen_width or ball.x <= 0):
        ball_speed_x = -ball_speed_x

    if scoreA == 10:
        player = "A"
        result()
    elif scoreB == 10:
        player = "B"
        result()

    ballMove()
    drawScreen()
    scoreBoard()
    drawPaddles()
    drawBall()
    pygame.display.update()

pygame.quit()