# import pygame

# pygame.init()
# screen = pygame.display.set_mode((300, 300))
# clock = pygame.time.Clock()

# def blitRotate(surf, image, pos, originPos, angle):

#     # calcaulate the axis aligned bounding box of the rotated image
#     w, h       = image.get_size()
#     box        = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
#     box_rotate = [p.rotate(angle) for p in box]
#     min_box    = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
#     max_box    = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])

#     # calculate the translation of the pivot 
#     pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
#     pivot_rotate = pivot.rotate(angle)
#     pivot_move   = pivot_rotate - pivot

#     # calculate the upper left origin of the rotated image
#     origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])

#     # get a rotated image
#     rotated_image = pygame.transform.rotate(image, angle)

#     # rotate and blit the image
#     surf.blit(rotated_image, origin)
  
#     # draw rectangle around the image
#     pygame.draw.rect(surf, (255, 0, 0), (*origin, *rotated_image.get_size()),2)

# def blitRotate2(surf, image, topleft, angle):

#     rotated_image = pygame.transform.rotate(image, angle)
#     new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

#     surf.blit(rotated_image, new_rect.topleft)
#     pygame.draw.rect(surf, (255, 0, 0), new_rect, 2)

# try:
#     image = pygame.image.load('AirPlaneFront1-128.png')
# except:
#     text = pygame.font.SysFont('Times New Roman', 50).render('image', False, (255, 255, 0))
#     image = pygame.Surface((text.get_width()+1, text.get_height()+1))
#     pygame.draw.rect(image, (0, 0, 255), (1, 1, *text.get_size()))
#     image.blit(text, (1, 1))
# w, h = image.get_size()

# start = False
# angle = 0
# done = False
# while not done:
#     clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
        
#     pos = (screen.get_width()/2, screen.get_height()/2)
    
#     screen.fill(0)
#     blitRotate(screen, image, pos, (w/2, h/2), angle)
#     # blitRotate2(screen, image, pos, angle)
#     angle += 1
    
#     pygame.draw.line(screen, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
#     pygame.draw.line(screen, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
#     # pygame.draw.circle(screen, (0, 255, 0), pos, 7, 0)

#     pygame.display.flip()
    
# pygame.quit()
# exit()

def detect_collision(self, staticBodies, *args):
    KinematicCollision = False
    x_collision = False
    net_x = self.x_velo
    net_y = self.y_velo
    difference_x = self.x_velo
    difference_y = self.y_velo
    prev_difference_x = self.prev_x_velo
    prev_difference_y = self.prev_y_velo

    for body in list(args) + staticBodies:
        body_parameters = body.get_body_parameters()
        super().detect_collision(body_parameters)
        material_type = body.get_material_type()
        self.sides = {"top": self.y_pos, "bottom": self.y_pos + self.height, "left": self.x_pos, "right": self.x_pos + self.width}
        body_sides = {"top": body_parameters[1], "bottom": body_parameters[1] + body_parameters[3], "left": body_parameters[0], "right": body_parameters[0] + body_parameters[2]}

        if self.collision == True:
            bodyMaterial = body.get_material_list()
            side_collisions = {	"b": abs(self.sides["bottom"] - body_sides["top"]),
                            "t": abs(self.sides["top"] - body_sides["bottom"]),
                            "l": abs(self.sides["left"] - body_sides["right"]),
                            "r": abs(self.sides["right"] - body_sides["left"])
                            }

            if type(body).__name__ !=  "KinematicBody":

                if abs(self.x_velo) > KinematicBody.MIN_BOUNCE_VELO:
                    self.bounce_x = abs(self.x_velo) * body_parameters[5]
                else:
                    self.bounce_x = 0

                if abs(self.y_velo) > KinematicBody.MIN_BOUNCE_VELO:
                    self.bounce_y = abs(self.y_velo) * body_parameters[5]
                else:
                    self.bounce_y = 0

                if self.bounce_x > body_parameters[6]:
                    self.bounce_x = body_parameters[6]

                if self.bounce_y > body_parameters[6]:
                    self.bounce_y = body_parameters[6]

                if material_type != "Fluid":
                    if side_collisions["t"] < side_collisions["b"] and side_collisions["t"] < side_collisions["l"] and side_collisions["t"] < side_collisions["r"]:
                        self.temp_max_y_vector("max", 0)
                        self.set_y_pos(body_parameters[1] + body_parameters[3])
                        self.temp_x_friction(body_parameters[4])
                        self.y_velo += -self.bounce_y
                        self.collision_records["t"] = True
                    elif side_collisions["b"] < side_collisions["t"] and side_collisions["b"] < side_collisions["l"] and side_collisions["b"] < side_collisions["r"]:	
                        self.temp_max_y_vector("min", 0)				
                        self.set_y_pos(body_parameters[1] - self.height)
                        self.temp_x_friction(body_parameters[4])		
                        self.y_velo += self.bounce_y	
                        self.collision_records["b"] = True
                    elif side_collisions["l"] < side_collisions["r"] and side_collisions["l"] < side_collisions["t"] and side_collisions["l"] < side_collisions["b"]:
                        self.temp_max_x_vector("min", 0)
                        self.set_x_pos(body_parameters[0] + body_parameters[2])
                        self.temp_y_friction(body_parameters[4])
                        self.x_velo += self.bounce_x
                        self.collision_records["l"] = True
                    elif side_collisions["r"] < side_collisions["l"] and side_collisions["r"] < side_collisions["t"] and side_collisions["r"] < side_collisions["b"]:
                        self.temp_max_x_vector("max", 0)
                        self.set_x_pos(body_parameters[0] - self.width)
                        self.temp_y_friction(body_parameters[4])
                        self.x_velo += -self.bounce_x
                        self.collision_records["r"] = True

                else:
                    self.temp_x_friction(body_parameters[4])
                    self.temp_y_friction(body_parameters[4])
            else:

                KinematicCollision = True
                mass = body.get_mass()
                net_mass = self.mass + mass
                self.systemic_mass = self.mass / net_mass

                if side_collisions["t"] < side_collisions["b"] and side_collisions["t"] < side_collisions["l"] and side_collisions["t"] < side_collisions["r"]:
                    if body.get_y_velo() < self.prev_y_velo:
                        if body.collision_records["b"] == False:
                            net_y = self.y_velo + body.get_y_velo()
                            difference_x = self.x_velo - body.get_x_velo()
                            prev_difference_x = self.prev_x_velo - body.get_prev_x()
                            self.y_velo = net_y * (1 - self.systemic_mass)
                        else:
                            self.y_velo = 0
                        self.y_pos = body_parameters[1] + body_parameters[3]
                elif side_collisions["b"] < side_collisions["t"] and side_collisions["b"] < side_collisions["l"] and side_collisions["b"] < side_collisions["r"]:				
                    if body.get_y_velo() > self.prev_y_velo:
                        if body.collision_records["t"] == False:
                            net_y = self.y_velo + body.get_y_velo()
                            difference_x = self.x_velo - body.get_x_velo()
                            prev_difference_x = self.prev_x_velo - body.get_prev_x()
                            self.y_velo = net_y * (1 - self.systemic_mass)
                        else:
                            self.y_velo = 0
                        self.y_pos = body_parameters[1] - self.height
                elif side_collisions["l"] < side_collisions["r"] and side_collisions["l"] < side_collisions["t"] and side_collisions["l"] < side_collisions["b"]:
                    x_collision = True
                    if body.get_x_velo() > self.prev_x_velo:
                        if body.collision_records["r"] == False:
                            net_x = self.x_velo + body.get_x_velo()
                            difference_y = self.y_velo - body.get_y_velo()
                            prev_difference_y = self.prev_y_velo - body.get_prev_y()		
                            self.x_velo = net_x * (1 - self.systemic_mass)
                        else:
                            self.x_velo = 0
                        self.x_pos = body_parameters[0] + body_parameters[2]
                elif side_collisions["r"] < side_collisions["l"] and side_collisions["r"] < side_collisions["t"] and side_collisions["r"] < side_collisions["b"]:
                    x_collision = True
                    if body.get_x_velo() < self.prev_x_velo:
                        if body.collision_records["l"] == False:
                            net_x = self.x_velo + body.get_x_velo()
                            difference_y = self.y_velo - body.get_y_velo()
                            prev_difference_y = self.prev_y_velo - body.get_prev_y()				
                            self.x_velo = net_x * (1 - self.systemic_mass)
                        else:
                            self.x_velo = 0
                        self.x_pos = body_parameters[0] - self.width

    if KinematicCollision == True:
        KinematicCollision = False
        if x_collision == True:
            self.apply_force(0, self.friction_y(difference_y, prev_difference_y, body_parameters[4], False))
        else:
            self.apply_force(self.friction_x(difference_x, prev_difference_x, body_parameters[4], False), 0)