import time
import pygame.freetype  # For better text rendering

class Stats:
    def __init__(self, fps):
        self.font = pygame.freetype.SysFont("Arial", 16)
        self.fps = fps  # Frames per second
        self.start_time = 0
        self.end_time = 0
        self.loop_time = 0  # Time for the last simulation loop
    
    def start_loop(self):
        self.start_time = time.perf_counter()  # Start time of the loop

    def end_loop(self):
        # Update and display stats
        self.end_time = time.perf_counter()  # End time of the loop
        self.loop_time = (self.end_time - self.start_time) * 1000  # Convert to milliseconds
    
    def draw(self, screen):
        # Display stats on the screen
        stats_text = [
            f"Loop Time: {self.loop_time:.2f} ms",
            f"FPS: {int(self.fps)}",
        ]
        for i, text in enumerate(stats_text):
            self.font.render_to(screen, (10, 10 + i * 20), text, (255, 255, 255))