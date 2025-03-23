import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

class Game:
	def __init__(self, screen_width, screen_height, offset,difficulty= "medium"):
		self.screen_width = screen_width
		self.screen_height = screen_height
		self.offset = offset
		self.spaceship_group = pygame.sprite.GroupSingle()
		self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
		self.obstacles = self.create_obstacles()
		self.aliens_group = pygame.sprite.Group()
		self.aliens_direction = 1
		self.alien_lasers_group = pygame.sprite.Group()
		self.mystery_ship_group = pygame.sprite.GroupSingle()
		self.lives = 3
		self.run = True
		self.score = 0
		self.highscore = 0
		self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
		self.load_highscore()
		pygame.mixer.music.load("Sounds/music.ogg")
		pygame.mixer.music.play(-1)
		self.level = 1  
		self.alien_speed = 1
		self.vertical_direction = 1
		self.base_y_positions = {}
		self.vertical_steps = 0
		self.vertical_target = 5
		self.create_aliens()  
		self.difficulty = difficulty
		self.set_difficulty()

	def set_difficulty(self):
		difficulties = {"easy": {"alien_speed": 0.5, "laser_frequency": 600},"medium": {"alien_speed": 1.0, "laser_frequency": 400},"hard": {"alien_speed": 1.5, "laser_frequency": 300}}
		params = difficulties.get(self.difficulty, difficulties["medium"])
		self.alien_speed = params["alien_speed"]
		self.laser_frequency = params["laser_frequency"]

	def reset(self):
		self.run = True
		self.lives = 3
		self.level = 1  
		self.alien_speed = 1  
		self.spaceship_group.sprite.reset()
		self.set_difficulty()

		self.aliens_group.empty()
		self.create_aliens()

		self.alien_lasers_group.empty()
		self.mystery_ship_group.empty()
		self.obstacles = self.create_obstacles()  
		self.score = 0	
		self.vertical_steps = 0
		self.vertical_direction = 1
		
		for alien in self.aliens_group.sprites():
			if alien not in self.base_y_positions:
				print(f"Missing alien in base_y_positions: {alien}")

		

	def game_over(self):
		self.run = False  

	def create_obstacles(self):
		obstacle_width = len(grid[0]) * 3
		gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
		obstacles = []
		for i in range(4):
			offset_x = (i + 1) * gap + i * obstacle_width
			obstacle = Obstacle(offset_x, self.screen_height - 100)
			obstacles.append(obstacle)
		return obstacles
	
	def create_aliens(self):
		self.base_y_positions.clear()
		self.aliens_group.empty()
		for row in range(5):
			for column in range(11):
				x = 75 + column * 55
				y = 110 + row * 55  
				if row == 0:
					alien_type = 3
				elif row in (1,2):
					alien_type = 2
				else:
					alien_type = 1

				alien = Alien(alien_type, x + self.offset/2, y)
				self.aliens_group.add(alien)
				self.base_y_positions[alien] = y  

				

	def move_aliens(self):
		self.aliens_group.update(self.aliens_direction * self.alien_speed)
		edge_hit = False
		new_direction = self.aliens_direction
    
		for alien in self.aliens_group.sprites():
			if alien.rect.right >= self.screen_width + self.offset/2:
				edge_hit = True
				new_direction = -1  
			elif alien.rect.left <= self.offset/2:
				edge_hit = True
				new_direction = 1  

		if edge_hit:
			self.aliens_direction = new_direction
			self.alien_move_down(10 * self.vertical_direction)
			self.vertical_steps += 1

			if self.vertical_steps >= self.vertical_target:
				self.vertical_direction *= -1
				self.vertical_steps = 0

		

	def alien_move_down(self, distance):
		for alien in self.aliens_group.sprites():
			alien.rect.y += distance
			if alien.rect.top < 90:  
				alien.rect.top = 90

	def alien_shoot_laser(self):
		if self.aliens_group.sprites():
			random_alien = random.choice(self.aliens_group.sprites())
			laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
			self.alien_lasers_group.add(laser_sprite)

	def create_mystery_ship(self):
		self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))

	def check_for_collisions(self):

		#Spaceship
		if self.spaceship_group.sprite.lasers_group:
			for laser_sprite in self.spaceship_group.sprite.lasers_group:
				
				aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
				if aliens_hit:
					self.explosion_sound.play()
					for alien in aliens_hit:
						self.score += alien.type * 100
						self.check_for_highscore()
						laser_sprite.kill()

				if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
					self.score += 500
					self.explosion_sound.play()
					self.check_for_highscore()
					laser_sprite.kill()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()

		


		#Alien Lasers
		if self.alien_lasers_group:
			for laser_sprite in self.alien_lasers_group:
				if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
					laser_sprite.kill()
					self.lives -= 1
					if self.lives == 0:
						self.game_over()

				for obstacle in self.obstacles:
					if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
						laser_sprite.kill()

		if self.aliens_group:
			for alien in self.aliens_group:
				for obstacle in self.obstacles:
					pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

				if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
					self.game_over()

		if not self.aliens_group and self.run:
			self.level_up()

	

	def check_for_highscore(self):
		if self.score > self.highscore:
			self.highscore = self.score

			with open("highscore.txt", "w") as file:
				file.write(str(self.highscore))

	def load_highscore(self):
		try:
			with open("highscore.txt", "r") as file:
				self.highscore = int(file.read())
		except FileNotFoundError:
			self.highscore = 0


	def level_up(self):
		self.level += 1
		self.alien_speed += 0.15  
		self.aliens_direction = 1  
		self.mystery_ship_group.empty()  
		self.create_aliens()  

	