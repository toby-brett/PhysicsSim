import pygame, sys

WIDTH, HEIGHT = 2600, 1300
TITLE = "1984"

#pygame initialization
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

PUSH_FORCE = 100
CUBE_WIDTH = 100
GRAVITY = 9.8
MASS = 5
FLUID_DENSITY = 1.24
VEL = 0

vel = VEL
collide_vel = 0
acc = 0
net_force = 0
push_force = 0
mass = MASS
displacement = 0
collide_displacement = 800
air_resistance = 0
static_friction = 0
sliding_friction = 0
gravity = GRAVITY
normal_force = 0
coefficient_static = 1
coefficient_sliding = 0.80
fluid_density = FLUID_DENSITY
cross_sectional_area = (CUBE_WIDTH / 100)**2
direction = 0
measure = 1
measured_dist = 0
weight = mass * gravity
measured_time = 0
vel_change = 0
button_color = (200, 200, 200)
vectors = 1
passive_push_force = 0

cube_initial = pygame.image.load('finish.png').convert()
cube = pygame.transform.scale(cube_initial, (CUBE_WIDTH, CUBE_WIDTH))
cube_rect = cube.get_rect(center = (0, HEIGHT * (0.6)))

floor = pygame.image.load('floor.png')

push_vector = pygame.image.load('push_vector_right.png')
resistance_vector = pygame.image.load('resistance_vector_left.png')
friction_vector = pygame.image.load('friction vector.png')
normal_vector = pygame.image.load('normal.png')
weight_vector = pygame.image.load('gravity.png')

friction_arrow_left = pygame.image.load('friction arrow.png')
friction_arrow_right = pygame.transform.flip(friction_arrow_left, True, False)
push_arrow_left = pygame.image.load('push arrow.png')
push_arrow_right = pygame.transform.flip(push_arrow_left, True, False)
resistance_arrow_left = pygame.image.load('resistance arrow.png')
resistance_arrow_right = pygame.transform.flip(resistance_arrow_left, True, False)
normal_arrow = pygame.image.load('normal arrow.png')
gravity_arrow = pygame.image.load('gravity arrow.png')

collide_initial = pygame.image.load('finish.png').convert()
collide = pygame.transform.scale(collide_initial, (500, 500))
collide_rect = collide.get_rect(center = (400, HEIGHT * (0.6) - 200))

font = pygame.font.SysFont("Arial", 30)

# 1 pixel = 2cm

class Object:
    def __init__(self, surf, rect, mass, displacement, coefficient_sliding, coefficient_static, cross_sectional_area, active):
        global MASS
        
        self.surf = surf
        self.rect = rect
        self.mass = mass
        self.mass
        self.displacement = displacement
        self.coefficient_sliding = coefficient_sliding
        self.coefficient_static = coefficient_static
        self.cross_sectional_area = cross_sectional_area
        self.net_force = 0
        self.acc = 0
        self.vel = 0
        self.push_force = push_force
        self.active = active
        
        

    def movement_active(self):

        self.momentum = self.mass * self.vel

        if self.active == True:
        
            if self.displacement >= WIDTH:
                self.displacement = -200
            elif self.displacement <= -200:
                self.displacement = WIDTH

            self.acc = (self.net_force / self.mass ) / 50
            self.air_resistance = 0.5 * fluid_density * self.vel**2 * 1.05 * self.cross_sectional_area
            self.rect.x = self.displacement
            self.displacement += self.vel
            self.vel += self.acc
            self.weight = self.mass * gravity
            self.normal_force = gravity * self.mass  
            self.static_friction = (self.coefficient_static * self.normal_force)
            self.sliding_friction = (self.coefficient_sliding * self.normal_force)
            self.push_force = push_force

            screen.blit(self.surf, self.rect)

            if self.vel == 0:
                if self.push_force > self.static_friction:
                    self.net_force = self.push_force - self.static_friction
                elif self.push_force < -self.static_friction:
                    self.net_force = self.push_force - self.static_friction
                elif self.push_force < self.static_friction and self.push_force > -self.static_friction:
                    self.net_force = 0

            if self.vel > 0:
                self.net_force = self.push_force - (self.air_resistance + self.sliding_friction)
                if self.vel + self.acc < 0:
                    self.displacement += -vel 
                    self.vel = 0
                    self.acc = 0
                    self.net_force = 0
            elif self.vel < 0:
                self.net_force = self.push_force + (self.air_resistance + self.sliding_friction)
                if self.vel + self.acc > 0:
                    self.vel = 0
                    self.net_force = 0
                    
            if self.vel != 0:
                if self.push_force < 0:
                    if self.vel > 0:
                        self.net_force = self.push_force - (self.air_resistance + self.sliding_friction)
                    else:
                        self.net_force = self.push_force + (self.air_resistance + self.sliding_friction)
                elif self.push_force > 0:
                    if self.vel < 0:
                        self.net_force = self.push_force + (self.air_resistance + self.sliding_friction)
                    else:
                        self.net_force = self.push_force - (self.air_resistance + self.sliding_friction)

    def movement_passive(self):
        global passive_push_force

        if self.active == False:


   
            
            self.acc = (self.net_force / self.mass ) / 50
            self.vel += self.acc
            self.air_resistance = 0.5 * fluid_density * self.vel**2 * 1.05 * self.cross_sectional_area
            self.displacement += self.vel
            self.rect.x = self.displacement
            self.weight = self.mass * gravity
            self.normal_force = gravity * self.mass  
            self.static_friction = (self.coefficient_static * self.normal_force)
            self.sliding_friction = (self.coefficient_sliding * self.normal_force)
            self.push_force = passive_push_force

            screen.blit(self.surf, self.rect)

            if self.vel == 0:
                self.net_force = self.push_force - (self.air_resistance + self.sliding_friction)

            if self.vel > 0:
                self.net_force = self.push_force - (self.air_resistance + self.sliding_friction)
                if self.vel + self.acc < 0:
                    self.displacement += -vel 
                    self.vel = 0
                    self.acc = 0
                    self.net_force = 0
            elif self.vel < 0:
                self.net_force = self.push_force + (self.air_resistance + self.sliding_friction)
                if self.vel + self.acc > 0:
                    self.vel = 0
                    self.net_force = 0


    def vector_lines(self):

        if self.active == True:
            global fluid_density

            self.weight_vector_scaled = pygame.transform.scale(weight_vector, ((50, (self.weight)*3)))
            self.weight_vector_rect = self.weight_vector_scaled.get_rect(midtop = self.rect.midbottom)

            self.normal_vector_scaled = pygame.transform.scale(normal_vector, ((50, (self.normal_force)*3)))
            self.normal_vector_rect = self.normal_vector_scaled.get_rect(midbottom = self.rect.midtop)

            self.normal_arrow_rect = normal_arrow.get_rect(midbottom = (self.normal_vector_rect.midtop))
            self.gravity_arrow_rect = gravity_arrow.get_rect(midtop = (self.weight_vector_rect.midbottom))

            if self.push_force == 0:
                self.push_vector_scaled = pygame.transform.scale(push_vector, (self.push_force*3, 50))
                self.push_vector_rect = self.push_vector_scaled.get_rect(midleft = (self.rect.center))
            elif self.push_force > 0:
                self.push_vector_scaled = pygame.transform.scale(push_vector, (self.push_force*3, 50))
                self.push_vector_rect = self.push_vector_scaled.get_rect(midleft = (self.rect.center))
            elif push_force < 0:
                self.push_vector_scaled = pygame.transform.scale(push_vector, (-(self.push_force*3), 50))
                self.push_vector_rect = self.push_vector_scaled.get_rect(midright = (self.rect.center))

            if self.vel > 0 : 
                self.resistance_vector_scaled = pygame.transform.scale(resistance_vector, ((self.air_resistance)*3, 50))
                self.resistance_vector_rect = self.resistance_vector_scaled.get_rect(midright = (self.rect.centerx, self.rect.centery - 15))

                self.friction_vector_scaled = pygame.transform.scale(friction_vector, ((self.sliding_friction)*3, 50))
                self.friction_vector_rect = self.friction_vector_scaled.get_rect(midright = (self.rect.centerx, self.rect.centery + 15))
                
            elif self.vel < 0:
                self.resistance_vector_scaled = pygame.transform.scale(resistance_vector, ((self.air_resistance)*3, 50))
                self.resistance_vector_rect = self.resistance_vector_scaled.get_rect(midleft = (self.rect.centerx, self.rect.centery - 15))

                self.friction_vector_scaled = pygame.transform.scale(friction_vector, ((self.sliding_friction)*3, 50))
                self.friction_vector_rect = self.friction_vector_scaled.get_rect(midleft = (self.rect.centerx, self.rect.centery + 15))
                
            elif self.vel == 0:
                self.resistance_vector_scaled = pygame.transform.scale(resistance_vector, ((self.air_resistance)*3, 50))
                self.resistance_vector_rect = self.resistance_vector_scaled.get_rect(midright = (self.rect.center))

                self.friction_vector_scaled = pygame.transform.scale(resistance_vector, ((self.sliding_friction)*0, 50))
                self.friction_vector_rect = self.friction_vector_scaled.get_rect(midleft = (self.rect.centerx, self.rect.centery + 15))

            if self.vel < 0:
                screen.blit(friction_arrow_right, (self.friction_vector_rect.midright[0], self.friction_vector_rect.midright[1] - 25))
                screen.blit(resistance_arrow_right, (self.resistance_vector_rect.midright[0], self.resistance_vector_rect.midright[1] - 25)) 
            elif self.vel > 0:
                screen.blit(friction_arrow_left, (self.friction_vector_rect.midleft[0] - 25, self.friction_vector_rect.midleft[1] - 25))
                screen.blit(resistance_arrow_left, (self.resistance_vector_rect.midleft[0] - 25, self.resistance_vector_rect.midleft[1] - 25))
            if self.push_force > 0:
                screen.blit(push_arrow_right, (self.push_vector_rect.midright[0], self.push_vector_rect.midright[1] - 25))
            elif self.push_force < 0:
                screen.blit(push_arrow_left, (self.push_vector_rect.midleft[0] - 25, self.push_vector_rect.midleft[1] - 25))


            screen.blit(self.push_vector_scaled, self.push_vector_rect)   
            screen.blit(self.resistance_vector_scaled, self.resistance_vector_rect)
            screen.blit(self.friction_vector_scaled, self.friction_vector_rect)
            
            screen.blit(self.weight_vector_scaled, self.weight_vector_rect)
            screen.blit(self.normal_vector_scaled, self.normal_vector_rect)
            screen.blit(normal_arrow, self.normal_arrow_rect)
            screen.blit(gravity_arrow, self.gravity_arrow_rect)

    def changing_variables(self):
        global fluid_density
        global gravity

        if vel_change == 1:
           
            self.vel = VEL
        
        gravity = GRAVITY
        self.mass = MASS
        self.push_force = PUSH_FORCE
        fluid_density = FLUID_DENSITY
        self.cross_sectional_area = (CUBE_WIDTH / 100)**2
    

cube_class = Object(cube, cube_rect, 5, 0, 0.8, 1, 1, True)
#collide_class = Object(collide, collide_rect, 1, 200, 0.2, 1, 1, False)
                           


class Inputs:
    def __init__(self, variable, posx, posy, typed_in, name, unit):
        self.variable = variable
        self.posx = posx
        self.posy = posy
        self.typed_input = str(typed_in)
        self.name = name
        self.active = False
        self.unit = unit

    def variable_replace(self):
        self.input_text = self.typed_input
        self.input_rect = pygame.Rect(self.posx, self.posy, 80, 32)
        self.active_color = pygame.Color('black')
        self.passive_color = (20, 20, 20)
        if self.active == True:
            self.color = (225, 20, 20)
        if self.active == False:
            self.color = (225, 220, 220)

    def draw(self):   
        self.text_request = font.render(str(self.name)+ ' =  ' , True, (0, 0, 0))
        self.unit_text = font.render(str(self.unit), True, (0, 0, 0))
        self.input_text = font.render(self.typed_input, True, (0, 0, 0))
        self.input_rect.w = max(20, self.input_text.get_width() + 10)
        screen.blit(self.unit_text, ((self.input_rect.x + self.input_rect.w + 10), self.input_rect.y))
        screen.blit(self.text_request, (self.posx - self.text_request.get_width(), self.posy))
        screen.blit(self.input_text, (self.posx + 3, self.posy))
        pygame.draw.rect(screen, self.color, self.input_rect, 2)

    
    
            
    
        
gravity_in = Inputs(gravity, 600, 50, '9.8', 'gravity', 'N')
force_in = Inputs(push_force, 600, 100, '100', 'force', 'N')
mass_in = Inputs(mass, 600, 150, '5', 'mass', 'Kg')
fluid_density_in = Inputs(fluid_density, 600, 200, '1.23', 'fluid density', 'Kg/m³')
velocity_in = Inputs(vel, 600, 250, str(vel), 'velocity', 'm/s')



while True:
   
    gravity_in.variable_replace()
    force_in.variable_replace()   
    mass_in.variable_replace()
    fluid_density_in.variable_replace()
    velocity_in.variable_replace()  
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if vector_on_button_rect.collidepoint(event.pos):
                    vectors = 1
                elif vector_off_button_rect.collidepoint(event.pos):
                    vectors = 0
                if gravity_in.input_rect.collidepoint(event.pos):
                    gravity_in.active = True 
                else:
                    gravity_in.active = False
                    GRAVITY = float(gravity_in.typed_input)
                if force_in.input_rect.collidepoint(event.pos):
                    force_in.active = True 
                else:
                    force_in.active = False
                    PUSH_FORCE = float(force_in.typed_input)
                if velocity_in.input_rect.collidepoint(event.pos):
                    velocity_in.active = True
                else:
                    velocity_in.active = False
                if vel_button_rect.collidepoint(event.pos):
                    button_pressed = True
                    vel_change = 1
                    VEL = float(velocity_in.typed_input)
                else:
                    button_pressed = False
                    vel_change = 0                    
                if mass_in.input_rect.collidepoint(event.pos):
                    mass_in.active = True 
                else:
                    mass_in.active = False
                    MASS = float(mass_in.typed_input)                    
                if fluid_density_in.input_rect.collidepoint(event.pos):
                    fluid_density_in.active = True 
                else:
                    fluid_density_in.active = False
                    FLUID_DENSITY = float(fluid_density_in.typed_input)



            if event.type == pygame.KEYDOWN:
                if gravity_in.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        gravity_in.typed_input = gravity_in.typed_input[:-1]
                    else:
                        gravity_in.typed_input += event.unicode
                if force_in.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        force_in.typed_input = force_in.typed_input[:-1]
                    else:
                        force_in.typed_input += event.unicode
                if velocity_in.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        velocity_in.typed_input = velocity_in.typed_input[:-1]
                    else:
                        velocity_in.typed_input += event.unicode
                if mass_in.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        mass_in.typed_input = mass_in.typed_input[:-1]
                    else:
                        mass_in.typed_input += event.unicode
                if fluid_density_in.active == True:
                    if event.key == pygame.K_BACKSPACE:
                        fluid_density_in.typed_input = fluid_density_in.typed_input[:-1]
                    else:
                        fluid_density_in.typed_input += event.unicode

            if event.type == pygame.KEYDOWN:                     
                if event.key == pygame.K_d:
                    push_force = PUSH_FORCE
                    pushing = True
                if event.key == pygame.K_a:
                    push_force = -PUSH_FORCE
                    pushing = True
                if event.key == pygame.K_SPACE:
                    measure = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    push_force = 0
                    pushing = False
                if event.key == pygame.K_a:
                    push_force = 0
                    pushing = False




   # all text

    

    acc_text = font.render('acceleration = ' + str(round(acc * 50, 5)) + 'm/s²', True, (0, 0, 0))
    vel_text = font.render('velocity = ' + str(round(vel, 1)) + 'm/s', True, (0, 0, 0))
    arrows_text = font.render('force vectors ', True, (0, 0, 0))
    
    screen.fill((225, 255, 255))
    gravity_in.draw()
    force_in.draw()
    mass_in.draw()
    fluid_density_in.draw()
    velocity_in.draw()
    screen.blit(vel_text, (50, 50))
    screen.blit(acc_text, (50, 100))
    screen.blit(floor, (0, (HEIGHT* (0.6)) + CUBE_WIDTH / 2))
    screen.blit(arrows_text, (900, 50))

    cube_class.changing_variables() 
    cube_class.movement_active()
    cube_class.movement_passive()

    if vectors == 1:
        cube_class.vector_lines()
        

    

    vector_on_button = pygame.image.load('button.png')
    vector_off_button = pygame.image.load('stop_button.png')
    vector_on_button_rect = vector_on_button.get_rect(topleft = (1100, 50))
    vector_off_button_rect = vector_off_button.get_rect(topleft = (1160, 50))

    screen.blit(vector_on_button, vector_on_button_rect)
    screen.blit(vector_off_button, vector_off_button_rect)
    
    vel_button = pygame.image.load('button.png')
    vel_stop_button = pygame.image.load('stop_button.png')
    vel_button_rect = vel_button.get_rect(topleft = (velocity_in.posx + velocity_in.input_rect.w + 80, velocity_in.posy))

    screen.blit(vel_button, vel_button_rect)
    screen.blit(vel_stop_button, (vel_button_rect[0] + 60, vel_button_rect[1]))

    
    
    pygame.display.flip()
    clock.tick(50)
