import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")

clock = pygame.time.Clock()

player_x = 370
player_y = 520
player_speed = 5

coloro = 255
colort = 0

chance = 0
give_chance = False

asteroids = []

for i in range(3):
    asteroid = {
        "x": random.randint(0, 740),
        "y": random.randint(-600, 0),
        "speed": random.randint(3,6)
    }
    asteroids.append(asteroid)

score = 0
font = pygame.font.SysFont(None, 36)
 
game_state = "PLAYING"
max_asteroids = 3
stars = []

for i in range(50):
    star = {
        "x": random.randint(0, 800),
        "y": random.randint(0, 600),
        "speed": random.randint(1,3)
    }
    stars.append(star)

bullets = []

explosions = []

explosions.append({
    "x": asteroid["x"],
    "y": asteroid["y"],
    "radius": 5
})

def explosionLoop():
    global explosions

    for e in explosions:
        e["radius"] += 2

        pygame.draw.circle(screen, (255, 165, 0), (e["x"], e["y"]), e["radius"])

        explosions = [ e for e in explosions if e["radius"] < 30]



def keyPress():
    global player_x, player_y, player_speed
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
        player_x -= player_speed

    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
        player_x += player_speed

    if (keys[pygame.K_UP] or keys[pygame.K_w]):
        player_y -= player_speed

    if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
        player_y += player_speed

def eventCont():
    global game_state, score, coloro, colort, player_x, player_y, max_asteroids, asteroids, bullets, chance, give_chance
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if True:
                if event.key == pygame.K_s and game_state == "Game Over!" and chance < 3 and score >= 51:
                    game_state = "PLAYING"
                    score -= 50
                    chance += 1

                    for asteroid in asteroids:
                        asteroid["x"] = random.randint(0, 740)
                        asteroid["y"] = random.randint(-600, 0)
            elif chance>3 and game_state == "PLAYING" and score <= 51:
                continue
            
            if event.key == pygame.K_r and game_state == "Game Over!":
                game_state = "PLAYING"

                score = 0

                coloro = 255
                colort = 0

                player_x = 370
                player_y = 520

                max_asteroids = 3

                chance = 0

                for asteroid in asteroids:
                    asteroid["x"] = random.randint(0, 740)
                    asteroid["y"] = random.randint(-600, 0)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and game_state == "PLAYING":
                bullet = {
                    "x": player_x + 30,
                    "y": player_y
                }

                bullets.append(bullet)

def playerBoundry():
    global player_x, player_y
    player_x = max(0, min(player_x, 740))
    player_y = max(0, min(player_y, 580))

def bulletCont():
    global bullets
    for bullet in bullets:
        bullet["y"] -= 8

    bullets = [ b for b in bullets if b["y"] > 0]

def highScore():
    global score, max_asteroids, coloro, colort
    if score > 300 and max_asteroids < 5:
        asteroid = {
            "x": random.randint(0, 740),
            "y": random.randint(-600, 0),
            "speed": random.randint(3,6)
        }

        asteroids.append(asteroid)
        max_asteroids += 1

        coloro = 0
        colort = 255

def bulletStar():
    global bullets, game_state, stars
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), (bullet["x"], bullet["y"], 5, 10))

    for star in stars:
        if game_state == "PLAYING":
            star["y"] += star["speed"]

        if star["y"] > 600:
            star["y"] = 0
            star["x"] = random.randint(0, 800)

        pygame.draw.circle(screen, (255, 255, 255), (star["x"], star["y"]), 2)

def asteroidLoop():
    global asteroids, score,game_state, coloro, colort, bullets, player_x, player_y
    for asteroid in asteroids:
        if game_state == "PLAYING":
            asteroid["y"] += asteroid["speed"] + score*0.02

        if asteroid["y"] > 600:
            asteroid["y"] = random.randint(-200, -50)
            asteroid["x"] = random.randint(0, 740) 

        pygame.draw.circle(screen, (coloro, 0, colort), (asteroid["x"], asteroid["y"]), 20)
    
        for bullet in bullets:
            if (bullet["x"] > asteroid["x"] - 20 and bullet["x"] < asteroid["x"] + 20 and bullet["y"] > asteroid["y"] - 20 and bullet["y"] < asteroid["y"] + 20):
                x = asteroid["x"]
                y = asteroid["y"]

                explosions.append({
                "x": asteroid["x"],
                "y": asteroid["y"],
                "radius": 5
                })

                asteroid["y"] = random.randint(0, 200)
                asteroid["x"] = random.randint(0, 740)

                bullets.remove(bullet)

                score += 10

                

        if (player_x < asteroid["x"] + 20 and player_x + 60 > asteroid["x"] - 20 and player_y < asteroid["y"] + 20 and player_y + 20 > asteroid["y"] - 20):
            game_state = "Game Over!"

def drawPlayer():
    global player_x, player_y
    pygame.draw.polygon(screen, (0, 255, 0), [(player_x, player_y+20), (player_x + 60, player_y + 20), (player_x + 30, player_y - 20) ])
    pygame.draw.rect(screen, (0, 255, 0), (player_x , player_y + 20, 60, 30))

def gameOver():
    global game_state, score, i
    if game_state == "Game Over!":
        if chance<3 and score >= 51:
            resume_text = font.render(f"Resume press S (50 points will be taken), chance{3-chance}", True, (255, 255, 255))
            screen.blit(resume_text, (100, 250))

        text = font.render("Game Over - Press R", True, (255, 255, 255))
        screen.blit(text, (250, 300))

        score_text = font.render("Score" + str(int(score)), True, (255, 255, 255))
        screen.blit(score_text, (250, 340))

def scorePrint():
    global score
    score_text = font.render("Score" + str(int(score)), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))


while True:

    eventCont()
    if game_state == "PLAYING":
        keyPress()

    playerBoundry() 
    bulletCont()
    highScore()

    screen.fill((0, 0, 0))

    bulletStar()
    asteroidLoop()

    if game_state == "PLAYING":
        score += 0.1
    
    drawPlayer()

    explosionLoop()

    gameOver() 
    scorePrint()
    
    pygame.display.update()
    clock.tick(60)



