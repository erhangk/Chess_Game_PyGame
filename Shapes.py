import pygame as p

class draw:
    def __init__(self,HEIGHT,DIM,rect_colors):
        self.SQ_SIZE=HEIGHT//DIM
        self.rect_colors = rect_colors

    def draw_rect(self,screen,x,y):
        rect = (x * self.SQ_SIZE,y * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
        p.draw.rect(screen, self.rect_colors[(x+y)%2] , rect, 2)  
        
    def draw_rect_alpha(self,surface, color, rect):
        #rect = (x * self.SQ_SIZE,y * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE)
        shape_surf = p.Surface(p.Rect(rect).size, p.SRCALPHA)
        p.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)  
        

        
    def draw_circle_alpha(self,surface, color, center, radius):
        target_rect = p.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = p.Surface(target_rect.size, p.SRCALPHA)
        p.draw.circle(shape_surf, color, (radius, radius), radius)
        surface.blit(shape_surf, target_rect)
