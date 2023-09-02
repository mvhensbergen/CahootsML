import pygame
import os
from colors import Color


class Visuals:
    card_margin = 50
    card_width = 25
    card_height = 50

    screen_width = 550
    screen_height = 400

    def __init__(self, outdir):
        # A sequence number to label the screenshots
        self.p = 0
        self.outdir = outdir
        self.pygame_inited = False

    def initialize_pygame(self):
        # Initializes pygame
        pygame.init()

        self.screen = pygame.display.set_mode(
            (Visuals.screen_width, Visuals.screen_height)
        )

        self.pygame_inited = True

    def render_missions(self, missions):
        # Renders all missions on the deck
        font = pygame.font.SysFont(None, 24, bold=False)

        x = Visuals.card_margin
        y = 20

        for mission in missions:
            description = "-" if not mission else mission
            img = font.render(f"{description}", True, "black")
            self.screen.blit(img, (x + Visuals.card_width / 3, y))
            y += 30

    def render_player_card(self, positionx, color, number):
        # Renders a player card
        self.render_card(positionx, 2, color, number)

    def render_deck_card(self, positionx, color, number):
        # Renders a deck card
        self.render_card(positionx, 1, color, number)

    def _color_to_gamecolor(self, color):
        # Mapping of card color to pygame color
        if color == Color.Pink:
            return "pink"
        if color == Color.Orange:
            return "orange"
        if color == Color.Green:
            return "darkgreen"
        if color == Color.Purple:
            return "purple"

    def render_card(self, positionx, positiony, color, number):
        # Makes a nice rounded card with the number in it
        x = Visuals.card_margin * (positionx + 1) + positionx * Visuals.card_width
        y = Visuals.card_margin * (positiony + 1) + positiony * Visuals.card_height

        font = pygame.font.SysFont(None, 24, bold=True)
        pygame.draw.rect(
            self.screen,
            self._color_to_gamecolor(color),
            [x, y, Visuals.card_width, Visuals.card_height],
            0,
            border_radius=5,
        )

        # For readibility, change the font color for some cards
        fontcolor = "black"
        if color == Color.Green or color == Color.Purple:
            fontcolor = "white"

        img = font.render(f"{number}", True, fontcolor)
        self.screen.blit(img, (x + Visuals.card_width / 3, y + Visuals.card_height / 2))

    def render_description(self, desc):
        # Generic info line to be rendered at the bottom of the screen
        positionx = 0
        positiony = 3
        x = Visuals.card_margin * (positionx + 1) + positionx * Visuals.card_width
        y = Visuals.card_margin * (positiony + 1) + positiony * Visuals.card_height

        font = pygame.font.SysFont(None, 24, bold=False)
        img = font.render(desc, True, "black")
        self.screen.blit(img, (x + Visuals.card_width / 3, y + Visuals.card_height / 2))

    def draw(self, missions, table_cards, player_cards, description):
        if not self.pygame_inited:
            self.initialize_pygame()

        self.screen.fill("white")
        self.render_missions(missions)
        for i, c in enumerate(table_cards):
            self.render_deck_card(i, c.color, c.number)
        for i, c in enumerate(player_cards):
            if c:
                self.render_player_card(i, c.color, c.number)

        self.render_description(description)

        # Draw and screenshot
        pygame.display.flip()
        pygame.event.get()

        if self.outdir:
            pygame.image.save(
                self.screen, os.path.join(self.outdir, f"screenshot-{self.p}.jpeg")
            )

        self.p += 1
