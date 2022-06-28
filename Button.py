import pygame


class Button:

    def __init__(self, btn_type, imgs_or_colors, size, txt, show_txt, font_size, font_clrs, center):
        self.btn_type = btn_type
        self.size = size
        self.center = center
        self.font_size = font_size
        self.txt = txt
        self.font_clrs = font_clrs
        self.mode_index = 0
        self.show_txt = show_txt
        self.dark_mode = False
        if self.btn_type == 'img':
            self.imgs = imgs_or_colors
            self.dark_imgs = []
            i = 0
            for img_src in self.imgs:
                img = pygame.image.load(img_src).convert_alpha()
                img = pygame.transform.scale(img, (self.size[0], self.size[1]))
                self.imgs.pop(i)
                self.imgs.insert(i, img)
                dark = pygame.Surface(img.get_size(), flags=pygame.SRCALPHA)
                dark.fill((50, 50, 50, 0))
                self.dark_imgs.append(dark)
                i += 1
            self.img = self.imgs[self.mode_index]
            self.rect = self.img.get_rect()
        elif self.btn_type == 'rect':
            self.rect_clrs = imgs_or_colors
            self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.rect.center = center
        self.corner_radius = 3
        self.font = pygame.font.Font('freesansbold.ttf', self.font_size)

    # Resizing the image and/or text
    def resize(self, new_img_size, new_font_size):
        self.size = new_img_size
        self.img = pygame.transform.scale(self.img, (self.size[0], self.size[1]))
        self.rect = self.img.get_rect()
        self.rect.center = self.center
        self.font_size = new_font_size

    def set_corner_radius(self, radius):
        self.corner_radius = radius

    def set_font(self, font):
        self.font = font

    def move(self, new_center):
        self.center = new_center
        self.rect.center = self.center

    def toggle_show(self):
        self.show_txt = not self.show_txt

    # Drawing a button
    def draw_button(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hover_mode()
        else:
            self.dormant_mode()
        if self.btn_type == 'img':
            if self.dark_mode:
                copy_img = self.img.copy()
                copy_img.blit(self.dark_imgs[self.mode_index], (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
                screen.blit(copy_img, self.rect)
            else:
                screen.blit(self.img, self.rect)
        elif self.btn_type == 'rect':
            pygame.draw.rect(screen, self.rect_clrs[self.mode_index], self.rect, 0, self.corner_radius)
        if self.show_txt:
            text = self.font.render(self.txt, True, self.font_clrs[0])
            if self.btn_type == 'rect':
                text = self.font.render(self.txt, True, self.font_clrs[self.mode_index])
            text_rect = text.get_rect()
            text_rect.center = self.rect.center
            if self.btn_type == 'img':
                text_rect.top = self.rect.top + self.size[1] + 5
            screen.blit(text, text_rect)

    def hover_mode(self):
        if self.btn_type == 'rect':
            self.switch_mode(1)
        elif self.btn_type == 'img':
            self.dark_mode = True

    def dormant_mode(self):
        self.switch_mode(0)

    def switch_img(self, index):
        self.mode_index = index
        self.img = self.imgs[self.mode_index]

    def switch_mode(self, index):
        if self.btn_type == 'rect':
            self.mode_index = index
        elif self.btn_type == 'img':
            self.dark_mode = False
