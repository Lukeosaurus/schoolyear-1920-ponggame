import arcade
import os
import time
import random
SPRITE_SCALING = 0.1
big_ball = 0.1


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 690
SCREEN_TITLE = "pong"

MOVEMENT_SPEED = 10
def printhowtouse():
    #dit is een functie voor het maken van het how to use scherm word gebruikt bij de class van het startmenu en van het pausemenu 
    arcade.draw_rectangle_filled(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 120, 1500, 275,
                          arcade.color.BLACK)    
    arcade.draw_text("how to play", SCREEN_WIDTH/2,
                     SCREEN_HEIGHT -150, arcade.color.WHITE, font_size=30,anchor_x="center",)
    arcade.draw_text("left player", SCREEN_WIDTH/4,
                     SCREEN_HEIGHT/2+150, arcade.color.WHITE, font_size=30,anchor_x="center",)
    arcade.draw_text("right player", SCREEN_WIDTH/4*3,
                     SCREEN_HEIGHT/2+150, arcade.color.WHITE, font_size=30,anchor_x="center",)
    arcade.draw_text("press space to start or reset the ball in game", SCREEN_WIDTH/2,
                     SCREEN_HEIGHT/2, arcade.color.WHITE, font_size=30,anchor_x="center",)    
  

class Player(arcade.Sprite):
    #dit zijn wat van de ijgenschapen van de speelpaneeltjes de bewegingen staan bij class mygame

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
        


class Ball(arcade.Sprite):
    def __init__(self, pict, radius, left, right,):
        super().__init__(pict, radius)
        #dit is de informatie zodat de bal weet waar de players zijn en zodat hij een scoren kan toevoegen aan het scoreboard
        self.left_player = left
        self.right_player = right
        self.move_speed_xy = 10
        self.left_player.score = 0
        self.right_player.score = 0
        self.big_ball = big_ball
        #hier wordt de hit_sound en de lose_sound aangemaakt
        self.hit_sound = arcade.load_sound("jump5.wav")
        self.lose_sound = arcade.load_sound("beep-03.wav")
        
    def update(self):
        #dit update de locatie van de ball met de verandering van de ball```
        self.center_x += self.change_x
        self.center_y += self.change_y
        if self.bottom < 0:
            #dit zoorgt ervoor dat de bal aan de onderkant terug stuiterd
            if self.change_y < 0:
                self.change_y = self.change_y *-1
            
        elif self.top > SCREEN_HEIGHT - 1:
            #dit zoorgt ervoor dat de bal van de bovenkant terug stuiterd
            if self.change_y > 0:
                self.change_y = self.change_y *-1
           
        if self.right > SCREEN_WIDTH + 5:
            arcade.play_sound(self.lose_sound)
            #dit meet of de bal de rechterkant van het scherm raakt en voegt dan een scoren toe aan left_player.score
            self.center_x = SCREEN_WIDTH / 2
            self.center_y = SCREEN_HEIGHT / 2
            self.change_y = 0
            self.change_x = 0
            self.started = False
            self.left_player.score += 1
            self.left_player.center_y = SCREEN_HEIGHT/2
            self.right_player.center_y = SCREEN_HEIGHT/2
            time.sleep(0.5)
        elif self.left < -5:
            arcade.play_sound(self.lose_sound)
            #dit meet of de bal de linkerkant van het scherm raakt en voegt dan een scoren toe aan right_player.score
            self.center_x = SCREEN_WIDTH / 2
            self.center_y = SCREEN_HEIGHT / 2
            self.change_y = 0
            self.change_x = 0
            self.started = False
            self.right_player.score += 1
            self.left_player.center_y = SCREEN_HEIGHT/2
            self.right_player.center_y = SCREEN_HEIGHT/2
            time.sleep(0.5)
        #daarna reset hij de bal naar het midden 
        elif self.left < self.left_player.right and self.center_x > self.left_player.right:
            #botsing of er voorbij x as             #hij is er nog niet voorbij X as
            if self.left_player.top > self.bottom and self.left_player.bottom < self.top:
                #zelfde hoogte Y as
                #hit
                #hier wordt de hit_sound afgespeeld
                arcade.play_sound(self.hit_sound)
                
                self.change_x = 10    
                if self.center_y < self.left_player.center_y:
                    #raakt de bal het paneeltje aan de boven of onderkant 
                    if self.change_y > -5:
                        #is de snelhijd voor y niet te groot  
                        self.change_y = self.change_y - 2.5
                        if self.change_y <= 5 and self.change_y >= -5:
                            #als de change van y te dicht bij nul licht veranderen dan de change van x
                            self.change_x = 12.5
                            if self.change_y <= 2.5 and self.change_y >= -2.5:
                                #als de change y nog dichter bij nul licht verander dan de change van x nog een keer
                                self.change_x = 14
                                #14 is de max x snelhijd anders kan het zijn dat de bal dwars door het paneeltje heen gaad
                        else:
                            self.change_x = 10
                            #als de snelhijd van y niet te dicht bij nul licht reset de snelhijd dan naar 10 

                elif self.center_y > self.left_player.center_y:
                    #dit is het zelfde als de vorigen aleen dan al je de onderkant raakt in plaats van de bovenkant 
                    if self.change_y < 5:
                        self.change_y = self.change_y + 2.5
                        if self.change_y <= 5 and self.change_y >= -5:
                            self.change_x = 12.5
                            if self.change_y <= 2.5 and self.change_y >= -2.5:
                                self.change_x = 14
                        else:
                            self.change_x = 10
                        
                        
        elif self.right > self.right_player.left and self.center_x < self.right_player.left :
            #dit is het zelfden aleen dan voor de right player en niet de left player
            if self.right_player.top > self.bottom and self.right_player.bottom < self.top:
                arcade.play_sound(self.hit_sound)                   
                self.change_x = -10
                if self.center_y < self.right_player.center_y:
                    if self.change_y > -5:
                        self.change_y = self.change_y - 2.5
                        if self.change_y <= 5 and self.change_y >= -5:
                            self.change_x = -12.5
                            if self.change_y <= 2.5 and self.change_y >= -2.5:
                                self.change_x = -14
                        else:
                            self.change_x = -10
                    
                elif self.center_y > self.right_player.center_y:
                    if self.change_y < 5:
                        self.change_y = self.change_y + 2.5
                        if self.change_y <= 5 and self.change_y >= -5:
                            self.change_x = -12.5
                            if self.change_y <= 2.5 and self.change_y >= -2.5:
                                self.change_x = -14
                        else:
                            self.change_x = -10
        

class Startmenu(arcade.View):
    def on_show(self):
        #als deze view word geopend dan word de achtergrond kleur naar wit gezet 
        arcade.set_background_color(arcade.color.WHITE)
        self.experimental = False
    def on_draw(self):
        #word het start menu getekend
        arcade.start_render()
        arcade.draw_text("pong", SCREEN_WIDTH/2,
                         SCREEN_HEIGHT-75, arcade.color.BLACK, font_size=60,anchor_x="center",)
        printhowtouse()
        #hier gebruik ik de functie printhowtouse die aan het begin is gemaakt 
        arcade.draw_text("press enter to start", SCREEN_WIDTH/2,
                         175, arcade.color.BLACK, font_size=30,anchor_x="center",)
        arcade.draw_rectangle_outline(SCREEN_WIDTH/2, 195, 300, 50,
                          arcade.color.BLACK)   
        arcade.draw_text("press Q to quit", SCREEN_WIDTH/2,
                         75, arcade.color.BLACK, font_size=30,anchor_x="center",)
        arcade.draw_rectangle_outline(SCREEN_WIDTH/2, 95, 240, 50,
                          arcade.color.BLACK)
        arcade.draw_text("press C for credits", SCREEN_WIDTH/2,
                         125, arcade.color.BLACK, font_size=30,anchor_x="center",)
        arcade.draw_text("play with sound", SCREEN_WIDTH/2,
                         275, arcade.color.BLACK, font_size=30,anchor_x="center",)

        #maak gebruik van self.ecperimental om te schijfen of experimentelen functies aan staan 
        if self.experimental == False:
            arcade.draw_text("press X for experimental functions", SCREEN_WIDTH/2,
                         225, arcade.color.BLACK, font_size=30,anchor_x="center",)
            arcade.draw_text("W S ", SCREEN_WIDTH/4,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
            arcade.draw_text("arrow keys", SCREEN_WIDTH/4*3,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
        elif self.experimental == True:
            arcade.draw_text("press X to turn off experimental functions", SCREEN_WIDTH/2,
                         225, arcade.color.BLACK, font_size=30,anchor_x="center",)
            arcade.draw_text("W A S D ", SCREEN_WIDTH/4,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
            arcade.draw_text("arrow keys", SCREEN_WIDTH/4*3,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
    
    def on_key_press(self, key, _modifiers):
        #als een van de keys word ingedrukt gaat hij naar een anderen view
        if key == arcade.key.ENTER:
            gameView = MyGame(self.experimental)
            gameView.setup()
            self.window.show_view(gameView)
        if key== arcade.key.C:
            creditView = Credits()
            self.window.show_view(creditView)
        if key == arcade.key.Q:
            arcade.close_window()
        if key == arcade.key.X:
            #maak gebruik van experimental om experimental te veranderen 
            if self.experimental == True:
                self.experimental = False
                
            elif self.experimental == False:
                self.experimental = True
                
                

class Credits(arcade.View):
    def on_show(self):
        #als deze view word geopend dan word de achtergrond kleur naar wit gezet
        arcade.set_background_color(arcade.color.WHITE)
    def on_draw(self):
        #hier worden de credits getekent 
        arcade.start_render()
        arcade.draw_text("credits", SCREEN_WIDTH/2 ,SCREEN_HEIGHT - 100, arcade.color.BLACK,
                         font_size=50, anchor_x="center")
        arcade.draw_text("by: Luuk Schukkink", SCREEN_WIDTH/2 ,SCREEN_HEIGHT - 150, arcade.color.BLACK,
                         font_size=30, anchor_x="center")
        arcade.draw_text("special tanks to:", SCREEN_WIDTH/2 ,SCREEN_HEIGHT - 200, arcade.color.BLACK,
                         font_size=30, anchor_x="center")
        arcade.draw_text("Lex Verheesen", SCREEN_WIDTH/2 ,SCREEN_HEIGHT - 250, arcade.color.BLACK,
                         font_size=30, anchor_x="center")
        arcade.draw_text("and Hans Schukkink", SCREEN_WIDTH/2 ,SCREEN_HEIGHT - 300, arcade.color.BLACK,
                         font_size=30, anchor_x="center")
        arcade.draw_text("Press any key to go to the menu", SCREEN_WIDTH/2, 100, arcade.color.BLACK,
                         font_size=20, anchor_x="center")

    def on_key_press(self, key, _modifiers):
        #hier word als er een random key word geprest weer naar het menuview gegaan 
        menuView = Startmenu()
        self.window.show_view(menuView)

class Pause(arcade.View):
    def __init__(self, view):
        super().__init__()
        self.gameView = view
        #hier word de kenis van de gameView megegeven zodat als je weer terug gaat naar je game het spel is bewaard
        #hier word ook experimental megegeven 
    def on_show(self):
        #als deze view word geopend dan word de achtergrond kleur naar wit gezet
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        #hier word het pausemenu gemaakt en word er weer gebuik gemaakt van printhowtouse
        arcade.start_render()
        arcade.draw_text("pause", SCREEN_WIDTH/2, SCREEN_HEIGHT - 75, arcade.color.BLACK,
                         font_size=60, anchor_x="center")
        arcade.draw_text("press M to Exit to menu", SCREEN_WIDTH/2, 75, arcade.color.BLACK,
                         font_size=40, anchor_x="center")
        arcade.draw_text("press enter to continue", SCREEN_WIDTH/2, 150, arcade.color.BLACK,
                         font_size=50, anchor_x="center")
        arcade.draw_text("(your score wont be saved)", SCREEN_WIDTH/2, 50, arcade.color.BLACK,
                        font_size=15, anchor_x="center")
        arcade.draw_text(str(self.gameView.player_left.score), SCREEN_WIDTH/2 - 25, 225, arcade.color.BLACK,
                        font_size=50, anchor_x="right")
        arcade.draw_text(str(self.gameView.player_right.score), SCREEN_WIDTH/2 + 25, 225, arcade.color.BLACK,
                        font_size=50, anchor_x="left")
        arcade.draw_text("-", SCREEN_WIDTH/2 , 225, arcade.color.BLACK,
                        font_size=50, anchor_x="center")

        printhowtouse()

        if self.gameView.experimental == False:
            #kijk naar gameView of experimental true of False is 
            arcade.draw_text("W S ", SCREEN_WIDTH/4,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
            arcade.draw_text("arrow keys", SCREEN_WIDTH/4*3,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
        elif self.gameView.experimental == True:
            arcade.draw_text("W A S D ", SCREEN_WIDTH/4,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
            arcade.draw_text("arrow keys", SCREEN_WIDTH/4*3,
                             SCREEN_HEIGHT/2+100, arcade.color.WHITE, font_size=30,anchor_x="center",)
        
        
    def on_key_press(self, key, _modifiers):
        #dit zijn de knopjes om terug te gaan naar he menu en om verder te gaan met de game
        if key == arcade.key.ENTER:
            self.window.show_view(self.gameView) 
            #hier word geen niewe game gemaakt maar gebuik gemaakt van de opgeslagen game
        if key == arcade.key.M:
            menuView = Startmenu()
            self.window.show_view(menuView)


class MyGame(arcade.View):
    def __init__(self, experimental):        
        super().__init__()
        #hier worden de startsounds gedefinierd 
        self.start_sound1 = arcade.load_sound("beep-01a.wav")
        self.start_sound2 = arcade.load_sound("beep-02.wav")
        self.epic_sound = arcade.load_sound("start_sound.mp3")
        self.up_pressed = False
        self.down_pressed = False
        self.started = False
        #gebruik experimental van startmenu om self.experimental te maken
        self.experimental = experimental


    def on_show(self):
        #als deze view word geopend dan word de achtergrond kleur naar zwart gezet
        arcade.set_background_color(arcade.color.BLACK)
    def setup(self):
        #hier word de spritelist aangemaakt en worden de players en de bal toegevoegt 
        self.player_list = arcade.SpriteList()
        #hier word player left gemaakt 
        self.player_left = Player("plaatje1.png", SPRITE_SCALING)
        self.player_left.center_x = 100
        self.player_left.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_left)

        #hier word player right gemaakt 
        self.player_right = Player("plaatje1.png", SPRITE_SCALING)
        self.player_right.center_x = SCREEN_WIDTH - 100
        self.player_right.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.player_right)

        #hier word de ball gemaakt 
        self.pong_ball = Ball("pongball.png", big_ball, self.player_left, self.player_right)
        self.pong_ball.center_x = SCREEN_WIDTH / 2
        self.pong_ball.center_y = SCREEN_HEIGHT / 2
        self.player_list.append(self.pong_ball)
        self.pong_ball.started = False

    def on_draw(self):
        #hier word het scoreboard getekent 
        arcade.start_render()    
        self.player_list.draw()
        arcade.draw_text("press esc to pause",
             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 120, arcade.color.WHITE, 20 , anchor_x="center")
        arcade.draw_text("press R to Reset score",
             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 150, arcade.color.WHITE, 20 , anchor_x="center")
        arcade.draw_text(str(self.player_left.score),
             SCREEN_WIDTH / 2 - 60, SCREEN_HEIGHT - 90, arcade.color.WHITE, 60 , anchor_x="right")
        arcade.draw_text( "  -  " ,
             SCREEN_WIDTH / 2, SCREEN_HEIGHT - 90, arcade.color.WHITE, 60 , anchor_x="center")
        arcade.draw_text(str(self.player_right.score,),
             SCREEN_WIDTH / 2 + 60, SCREEN_HEIGHT - 90, arcade.color.WHITE, 60 , anchor_x="left")
             

    def on_update(self, delta_time):
        self.player_list.update()
        #hier word er gezoorgt dat dat de paneeltjes niet uit het scherm bewegen en niet over de midelijn gaan voor de x ass
        #dit is een expirimentelen functie die je aan of uit kan hebben staan 
        if self.experimental == True:
            if self.player_left.center_x < 0:
                self.player_left.center_x = 0
            if self.player_left.center_x > SCREEN_WIDTH/2:
                self.player_left.center_x = SCREEN_WIDTH/2
            if self.player_right.center_x > SCREEN_WIDTH :
                self.player_right.center_x = SCREEN_WIDTH 
            if self.player_right.center_x < SCREEN_WIDTH/2 :
                self.player_right.center_x = SCREEN_WIDTH/2 

    
    def on_key_press(self, key, modifiers):
        #dit zijn de bewegingen van de players/paneeltjes
        if key == arcade.key.W:
            self.player_left.change_y = self.player_left.change_y + MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_left.change_y = self.player_left.change_y - MOVEMENT_SPEED
        #dit is een expirimentelen functie die je aan of uit kan hebben staan 
        if self.experimental == True:
            if key == arcade.key.A:
                self.player_left.change_x = self.player_left.change_x - (MOVEMENT_SPEED* 1.2)
            elif key == arcade.key.D:
                self.player_left.change_x = self.player_left.change_x + (MOVEMENT_SPEED* 1.2)
        if key == arcade.key.UP:
            self.player_right.change_y = self.player_right.change_y + MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_right.change_y = self.player_right.change_y - MOVEMENT_SPEED
        #dit is een expirimentelen functie die je aan of uit kan hebben staan 
        if self.experimental == True:
            if key == arcade.key.LEFT:
                self.player_right.change_x = self.player_right.change_x - (MOVEMENT_SPEED* 1.2)
            elif key == arcade.key.RIGHT:
                self.player_right.change_x = self.player_right.change_x + (MOVEMENT_SPEED* 1.2)
        if key == arcade.key.SPACE:
            if self.pong_ball.started:
                #als de bal al is gestart dan word de bal gereset naar het miden en word de snelhijd 0
                self.pong_ball.change_y = 0
                self.pong_ball.change_x = 0
                self.pong_ball.center_y = SCREEN_HEIGHT / 2
                self.pong_ball.center_x = SCREEN_WIDTH / 2
                self.player_left.center_y = SCREEN_HEIGHT/2
                self.player_right.center_y = SCREEN_HEIGHT/2
                self.pong_ball.started = False
                
            else:
                #als de bal nog niet is gestart word de bal gestart met een snelhijd van 10 voor x en y 
                if self.experimental == True:
                    arcade.play_sound(self.epic_sound)
                    time.sleep (3.5)
                else: 
                    for _ in [3, 2, 1]:
                        arcade.play_sound(self.start_sound2)
                        time.sleep(0.75)

                    arcade.play_sound(self.start_sound1)
                    time.sleep(0.1)
                #bepaal naar welken kant de bal de vorigen keer is geweest
                if self.started:
                    self.pong_ball.change_x = 10
                    self.started = False
                    #gebruik random om de richting van de bal te bepalen voor de y as
                    richting = random.randrange(2)                    
                    if richting == 0:
                        self.pong_ball.change_y = 10
                    else:
                        self.pong_ball.change_y = -10    

                else:
                    self.pong_ball.change_x = -10
                    self.started = True
                    #gebruik random om de richting van de bal te bepalen voor de y as
                    richting = random.randrange(2)
                    if richting == 0:
                        self.pong_ball.change_y = 10
                    else:
                        self.pong_ball.change_y = -10    
                self.pong_ball.started = True
        if key == arcade.key.R:
            #als R word geprest word de scoren gereset
            self.player_right.score = 0
            self.player_left.score = 0
        if key == arcade.key.ESCAPE:
            #als esc word geprest word het pause menu geopend die mee heeft gekregen wat de gameView is zodat hij die daarna kan gebruiken om de game weer te maken 
            pauseView = Pause(self)
            self.window.show_view(pauseView)

    def on_key_release(self, key, modifiers):
        #hier worden de snelheden gereset als de knopen los worden gelaten 
        if key == arcade.key.W:
            self.player_left.change_y = self.player_left.change_y - MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_left.change_y = self.player_left.change_y + MOVEMENT_SPEED
        #dit is een expirimentelen functie die je aan of uit kan hebben staan 
        if self.experimental == True:
            if key == arcade.key.A:
                self.player_left.change_x = self.player_left.change_x + (MOVEMENT_SPEED* 1.2)
            elif key == arcade.key.D:
                self.player_left.change_x = self.player_left.change_x - (MOVEMENT_SPEED* 1.2)
        if key == arcade.key.UP:
            self.player_right.change_y = self.player_right.change_y - MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_right.change_y = self.player_right.change_y + MOVEMENT_SPEED
        #dit is een expirimentelen functie die je aan of uit kan hebben staan
        if self.experimental == True:
            if key == arcade.key.LEFT:
                self.player_right.change_x = self.player_right.change_x + (MOVEMENT_SPEED* 1.2)
            elif key == arcade.key.RIGHT:
                self.player_right.change_x = self.player_right.change_x - (MOVEMENT_SPEED* 1.2)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    # hier word megegeven hoe de window gemaakt moet worden 
    menuView = Startmenu()
    #hier word de eersten View geopend 
    window.show_view(menuView)
    window.set_mouse_visible(False)
    #maak de muis onzigbaar
    arcade.run()
    


if __name__ == "__main__":
    main()