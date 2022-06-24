# Pathfinding algorithm for Amazon’s self-driving delivery vehicles
import random


class SquareItem(object):
	def __init__(self, pt):
		super(SquareItem, self).__init__()
		self.x = pt[0]
		self.y = pt[1]
		self.G = 0
		self.H = 0
		self.F = self.G + self.H

	def update(self, G, H, F=None):
		self.G = G # The path lenth from the starting point
		self.H = H # The estimated path lenth from the delivery point
		self.F = G + H if F is None else F # The sum of G and H

	def position(self):
		return (self.x, self.y)

	def data(self):
		return (self.G, self.H, self.F)

class PathfindingAlgorithm(object):
	"""Pathfinding Algorithm"""
	def __init__(self, world_size):
		super(PathfindingAlgorithm, self).__init__()
		self.world_size = world_size

	def get_neighbours(self, pt):
		vector = []
		for i in [-1, 0, 1]:
			for j in [-1, 0, 1]:
				vector.append((i, j))
		results = []
		for v in vector:
			result = (pt[0] + v[0], pt[1] + v[1])
			if result[0] >= self.world_size[0] or result[0] < 0 or result[1] >= self.world_size[1] or result[1] < 0:
				continue
			results.append(result)

		# print("neighbour_pt:",  results)
		return results

	def distance(self, pt_1, pt_2):
		d = ((pt_1[0] - pt_2[0]) ** 2 + (pt_1[1] - pt_2[1]) ** 2) ** 0.5
		return d

	def show(self, path, obstacles_pt_list):
		for j in range(world_size[0]):
			line = ""
			for i in range(world_size[1]):
				if (i, j) in obstacles_pt_list:
					line += "x "
				elif (i, j) == path[0]:
					line += "s "
				elif (i, j) == path[-1]:
					line += "d "
				elif (i, j) in path:
					line += "- "
				else:
					line += ". "
			print(line)

	def find(self, starting_pt, delivery_pt, obstacles_pt_list):
		item_list = []
		starting_pt_item = SquareItem(starting_pt)
		starting_pt_item.update(G=0, H=self.distance(starting_pt, delivery_pt))
		item_list.append(starting_pt_item)
		step = 0
		while True:
			best_pt = None
			best_pt_G = float('inf')
			best_pt_H = float('inf')
			best_pt_F = float('inf')
			for current_item in reversed(item_list):
				for neighbour_pt in self.get_neighbours(current_item.position()):
					if neighbour_pt in obstacles_pt_list:
						continue
					if neighbour_pt in [pt_item.position() for pt_item in item_list]:
						continue
					neighbour_pt_G = current_item.data()[0] + 1
					neighbour_pt_H = self.distance(neighbour_pt, delivery_pt)
					neighbour_pt_F = neighbour_pt_G + neighbour_pt_H
					# print(neighbour_pt, ":", neighbour_pt_G, neighbour_pt_H, neighbour_pt_F)
					if neighbour_pt_F < best_pt_F:
						best_pt = neighbour_pt
						best_pt_G = neighbour_pt_G
						best_pt_H = neighbour_pt_H
						best_pt_F = neighbour_pt_F
						# print("Find point: ", best_pt)
			if best_pt is None:
				print("Unable to reach delivery point.")
				item_list = []
				break
			best_pt_item = SquareItem(best_pt)
			best_pt_item.update(best_pt_G, best_pt_H, best_pt_F)
			item_list.append(best_pt_item)

			# print([pt_item.position() for pt_item in item_list])

			temp_path = [pt_item.position() for pt_item in item_list]
			temp_path.append(delivery_pt)

			print("Step %d:" % step)
			self.show(temp_path, obstacles_pt_list)
			step += 1

			if best_pt_H == 0:
				break

		if len(item_list) == 0:
			return

		final_path = [delivery_pt]
		last_G = item_list[-1].data()[0]
		item_list = item_list[:-1]

		while True:
			for i, current_item in enumerate(reversed(item_list)):
				if current_item.data()[0] == last_G - 1 and self.distance(current_item.position(), final_path[-1]) < 2 ** 0.5 + 0.00001:
					final_path.append(current_item.position())
					del item_list[-i-1]
					last_G = current_item.data()[0]
					break
			
			if final_path[-1] == starting_pt:
				break
			
		final_path = final_path[::-1]
		print("Final path:")
		self.show(final_path, obstacles_pt_list)
		print("The obstacles are: ", obstacles_pt_list)
		print("The path is: ", final_path)



world_size = (10, 10)
starting_pt = (0, 0)
delivery_pt = (9, 9)
obstacles_pt_list = [(9, 7), (8, 7), (7, 7), (7, 8)]

random_obstacles = []
while len(random_obstacles) < 20:
	random_obstacle = (random.randint(0, world_size[0]), random.randint(0, world_size[1]))
	if random_obstacle != starting_pt and random_obstacle != delivery_pt and random_obstacle not in obstacles_pt_list and random_obstacle not in random_obstacles:
		random_obstacles.append(random_obstacle)
obstacles_pt_list += random_obstacles
print("The obstacles are: ", obstacles_pt_list)
PA = PathfindingAlgorithm(world_size)
PA.find(starting_pt, delivery_pt, obstacles_pt_list)

