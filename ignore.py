# class Boss(Character):
#     def __init__(self, surf, name, cells, spawn, hits=8, behaviors=(), on_destruct = None): # added default hits value, on_destruct is unused.
#         super().__init__(surf, name, cells)
#         self.spawn = spawn
#         self.hits = hits # TYPO fixed.
#         self.behaviors = behaviors
#         self.atkdur = 256
#     def update(self):
#         global atkdur
#         if len(self.behaviors) >= 2:
#             if self.atkdur == 0:
#                 targetPos = None
#                 atk = random.choice(self.behaviors).lower()
#                 if atk['name'] == "moveleft":
#                     distance = self.position.distance_to(pygame.Vector2(-150,self.y))
#                 elif atk['name'] == "moveright":
#                     distance = self.position.distance_to(pygame.Vector2(self.surf.width + 150, self.y))
#                 elif atk['name'] == "movedown":
#                     self.targetPos = self.x, self.surf.height+150
#                     distance = self.position.distance_to(pygame.Vector2(self.x, self.surf.height+150))
#                 elif atk['name'] == "moveup":
#                     distance = self.position.distance_to(pygame.Vector2(self.x, -150))
#                 elif atk['name'] == "hover":
#                     atkdur = 120
#                 elif atk['name'] == "fireleft":
#                     self.fire(180)
#                     atkdur = 180
#                 elif atk['name'] == "fireright":
#                     self.fire(0)
#                     atkdur = 180
#                 elif atk['name'] == "firedown":
#                     self.fire(90)
#                     atkdur = 180
#                 elif atk['name'] == "fireup":
#                     self.fire(-90)
#                     atkdur = 180
#                 elif atk['name'] == "fireto":
#                     self.fire(variables.character) # type: ignore
#                 # if not targetPos == None:
#                 #     atkdur = self.position.distance_to(pygame.Vector2(*targetPos)/6) # Still figuring out how long this should take.
                
#     def fire(self, target: Character | float | int=0):
#         """This will eventually create an object"""
#         if not isinstance(target, (Character, float, int)):
#             raise TypeError("Target of Boss must be either an int or a Character.")
#         position = self.position
#         angle = 0
#         attack_speed = 60
#         if isinstance(target, Character):
#             angle = self.position.angle_to(target.position)
#             """Create the projectile and send it in the direction of the target."""
#         if isinstance(target, float):
#             angle = int(target)
        
#         make_projectile(self.position, angle, attack_speed)
