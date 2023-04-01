import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True 
End_state=False #to show game over page 
player = 0 # alternates between 0 and 1 during the course of the game
player_colours = ["red", "green"]
player_lead=0

dot_posns = [] * 25 # positions of each of the dots on the 5*5 grid 
for x in range(0, 5):
    for y in range(0, 5):
        dot_posns.append(((x+1) * screen.get_width() / 6, (y+1) * screen.get_height() / 6))

dot_clicked = None
lines = [] # stores lines already drawn 
potential_boxes = [] # all possible boxes
score = [0, 0] # the scoreboard
x=score[0]
y=score[0]
#text and fonts for points,score cards are created on screen 
font=pygame.font.Font("assets\OdibeeSans-Regular.ttf",20)
p1_point=font.render("Player 1:"+str(x),True,"white","black")
p2_point=font.render("Player 2:"+str(y).format(y),True,"white","black")
#text for game over screen
Font=pygame.font.Font("assets\DeliciousHandrawn-Regular.ttf",50)
p1_wins=Font.render("Player 1 Wins !",True,"red","black")
p2_wins=Font.render("Player 2 Wins !",True,"green","black")


for i in range(4):
    for j in range(4):
        potential_boxes.append([{dot_posns[5*i+j], dot_posns[5*i+j+1]}, {dot_posns[5*i+j+5], dot_posns[5*i+j]},
                                {dot_posns[5*i+j+5], dot_posns[5*i+j+6]}, {dot_posns[5*i+j+1], dot_posns[5*i+j+6]}])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    dots = []
    for dot_posn in dot_posns:
        dots += [pygame.draw.circle(screen, "blue", pygame.Vector2(*dot_posn), 10)]
    
    for i in range(25):
        mouse_pos = pygame.mouse.get_pos()
        if dots[i].collidepoint(mouse_pos):
            dots[i] = pygame.draw.circle(screen, "white", pygame.Vector2(*dot_posns[i]), 10)
            if pygame.mouse.get_pressed()[0]:
                if dot_clicked == None:
                    dot_clicked = i
                elif i in {dot_clicked + 1, dot_clicked - 1, dot_clicked + 5, dot_clicked - 5}:
                    if {dot_posns[dot_clicked], dot_posns[i]} not in lines:
                        line = {dot_posns[dot_clicked], dot_posns[i]}
                        lines.append(line)
                        for potential_box in potential_boxes:
                            if line in potential_box:
                                potential_box.remove(line)
                            if potential_box == []:
                                score[player] += 1
                                potential_boxes.remove([])
                                print(score)
                   
                    dot_clicked = None
                    player = (player + 1) % 2
                    pygame.mouse.set_pos(mouse_pos[0] - 20, mouse_pos[1])
        
    if dot_clicked != None:
        dots[dot_clicked] = pygame.draw.circle(screen, player_colours[player], pygame.Vector2(*dot_posns[dot_clicked]), 10)
        pygame.draw.line(screen, "white", dot_posns[dot_clicked], pygame.mouse.get_pos())

    for line in lines:
        pygame.draw.line(screen, "white", *line)
    p1_point=font.render("Player 1:"+str(score[0]),True,"red","black") #Code for updating score 
    p2_point=font.render("Player 2:"+str(score[1]),True,"green","black")
    screen.blit(p1_point,(50,50))
    screen.blit(p2_point,(700,50))
    
    if score[0]>score[1]:
        player_lead=1
    elif score[0]<score[1]:
        player_lead=2
    else:
        player=0
 
    if End_state == True:
        screen.fill("black")
        if player_lead==0:
            pass
        elif player_lead==1:
            screen.blit(p1_wins,(285,280)) 
        elif player_lead==2:
            screen.blit(p2_wins,(285,280))

        
                    

    pygame.display.flip()

pygame.quit()
#eof
