import pygame

import pygame

def show_difficulty_screen(screen, screen_width, screen_height):
    font = pygame.font.Font("Font/monogram.ttf", 40)
    title_font = pygame.font.Font("Font/monogram.ttf", 60)
    selected_difficulty = None

    while not selected_difficulty:
        screen.fill((29, 29, 27))  
        
        # Draw title
        title_surface = title_font.render("SPACE INVADERS", True, (243, 216, 63))
        title_rect = title_surface.get_rect(center=(screen_width/2, 100))
        screen.blit(title_surface, title_rect)

        # Difficulty buttons
        easy_button = pygame.Rect(screen_width/2-100, 200, 200, 50)
        medium_button = pygame.Rect(screen_width/2-100, 300, 200, 50)
        hard_button = pygame.Rect(screen_width/2-100, 400, 200, 50)

        # Draw buttons
        pygame.draw.rect(screen, (0, 255, 0), easy_button)
        pygame.draw.rect(screen, (255, 255, 0), medium_button)
        pygame.draw.rect(screen, (255, 0, 0), hard_button)

        # Button labels
        easy_text = font.render("EASY", True, (0, 0, 0))
        medium_text = font.render("MEDIUM", True, (0, 0, 0))
        hard_text = font.render("HARD", True, (0, 0, 0))

        # Position text
        screen.blit(easy_text, (easy_button.x + 60, easy_button.y + 10))
        screen.blit(medium_text, (medium_button.x + 40, medium_button.y + 10))
        screen.blit(hard_text, (hard_button.x + 60, hard_button.y + 10))

        # Check for clicks
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(mouse_pos):
                    return "easy"
                elif medium_button.collidepoint(mouse_pos):
                    return "medium"
                elif hard_button.collidepoint(mouse_pos):
                    return "hard"

        pygame.display.update()