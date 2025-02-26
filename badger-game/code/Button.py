import pygame, sys

class Button:
    def __init__(self, win, x, y, width, height, text, font, text_colors, bg_colors, border_colors, opacity=255):
        self.win = win
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_colors = text_colors  # Normal, hover, clicked
        self.bg_colors = bg_colors      # Normal, hover, clicked
        self.border_colors = border_colors  # Normal, hover, clicked
        self.hovered = False
        self.clicked = False
        self.opacity = opacity  # Opacity level (0 = fully transparent, 255 = fully opaque)

        # Create a surface for the button background to apply opacity
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.set_alpha(self.opacity)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = True
                return True  # Button clicked
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.clicked and self.rect.collidepoint(event.pos):
                self.clicked = False
                return True  # Button released
            self.clicked = False
        return False

    def draw(self):
        # Determine button state (normal, hover, clicked)
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)

        if self.clicked:
            bg_color = self.bg_colors[2]
            border_color = self.border_colors[2]
            text_color = self.text_colors[2]
        elif self.hovered:
            bg_color = self.bg_colors[1]
            border_color = self.border_colors[1]
            text_color = self.text_colors[1]
        else:
            bg_color = self.bg_colors[0]
            border_color = self.border_colors[0]
            text_color = self.text_colors[0]

        # Draw button background with opacity
        self.surface.fill(bg_color)
        self.win.blit(self.surface, self.rect.topleft)

        # Draw button border
        pygame.draw.rect(self.win, border_color, self.rect, 2)

        # Draw button text
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.win.blit(text_surface, text_rect)



    def handle_event(self, event):
        """Handle mouse events on the button."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = "clicked"
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.state == "clicked":
                self.state = "normal"
        elif event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.state = "hover"
            else:
                self.state = "normal"
        return False
