import random

class Cloud:
    def __init__(self, pos, img, speed, depth) -> None:
        self.pos = list(pos) # We use a list to avoid many clouds pointing to the same position and being messed up when we alter this.
        self.img = img
        self.speed = speed
        self.depth = depth
    
    def update(self):
        self.pos[0] += self.speed # Clouds move right based on speed.
    
    def render(self, surf, offset=(0, 0)):
        # Apply offset and depth to positions. Depth changes the position of the cloud based on offset.
        # E.g. if depth = 0.5, it moves 0.5 times as much as the offset -> cool parallax effect.
        render_pos = (self.pos[0] - offset[0] * self.depth, self.pos[1] - offset[1] * self.depth)

        # Interesting math to loop couds around
        # Mod by screen width + image width (room for right side) then - image width (room for left side)
        surf.blit(self.img, (render_pos[0] % (surf.get_width() + self.img.get_width()) - self.img.get_width(), render_pos[1] % (surf.get_height() + self.img.get_height()) - self.img.get_height()))

class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = []

        for _ in range(count):
            # Random.random returns a float from 0 to 1
            # Instantiate count Cloud classes with random positions (which get modulo'd)
            # The last two integers set minimums and maximums
            self.clouds.append(Cloud((random.random() * 99999, random.random() * 99999), random.choice(cloud_images), random.random() * 0.05 + 0.05, random.random() * 0.6 + 0.2))

        # Sorting the clouds makes sure closer clouds are rendered last (in front)
        self.clouds.sort(key=lambda x: x.depth) # Custom function as a Cloud is not naturally sortable.
    
    def update(self):
        for cloud in self.clouds:
            cloud.update()
    
    def render(self, surf, offset=(0, 0)): 
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)