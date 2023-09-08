import pygame

class SPGExpandableSurface:
    '''
    Sphere's Pygame Expandable Surface

    Simple tool for making expandable surfaces with borders.
    '''
    def __init__(self,
                 source_img: pygame.Surface,
                 width: int,
                 height: int,
                 corner_size: tuple[int, int],
                 background: bool = True,
                 gen_on_load: bool = True
                 ) -> None:
        self.source_img = source_img
        self.corner_size = corner_size
        self.width = width
        self.height = height
        self.background = background

        if gen_on_load:
            self.gen_surface()
    def gen_surface(self) -> None:
        '''
         - Divides source image into 9 slices
         - Creates empty canvas
         - Blits corners in new position
         - Blit edges repeating until edge is filled
         - Blit center until center is filled
        '''
        source_width = self.source_img.get_width()
        source_height = self.source_img.get_height()

        if self.width == source_width and self.height == source_height:
            return self.source_img

        # getting the corner surfaces

        topleft_corner = self.source_img.subsurface(pygame.Rect(0,0,*self.corner_size))
        topright_corner = self.source_img.subsurface(pygame.Rect(source_width - self.corner_size[0],0,*self.corner_size))
        bottomleft_corner = self.source_img.subsurface(pygame.Rect(0,source_height - self.corner_size[1],*self.corner_size))
        bottomright_corner = self.source_img.subsurface(pygame.Rect(source_width - self.corner_size[0],source_height - self.corner_size[1],*self.corner_size))

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        width_larger_than_corners = self.width > self.corner_size[0]*2
        height_larger_than_corners = self.height > self.corner_size[1]*2

        # getting column and row slices
        if width_larger_than_corners:
            top_column_slice = self.source_img.subsurface(pygame.Rect(self.corner_size[0], 
                                                                      0, 
                                                                      source_width - (self.corner_size[0]*2),
                                                                      self.corner_size[1]))


            bottom_column_slice = self.source_img.subsurface(pygame.Rect(self.corner_size[0], 
                                                                      source_height - self.corner_size[1], 
                                                                      source_width - (self.corner_size[0]*2),
                                                                      self.corner_size[1]))
            slice_width = top_column_slice.get_width()
            step = slice_width
            for x in range(self.corner_size[0], (self.surface.get_width()-self.corner_size[0])):
                if step == slice_width:
                    difference = self.surface.get_width()-self.corner_size[0] - x
                    if difference < slice_width:
                        self.surface.blit(top_column_slice.subsurface(pygame.Rect(0, 0, difference, self.corner_size[1])),
                                    (x, 0))
                        self.surface.blit(bottom_column_slice.subsurface(pygame.Rect(0, 0, difference, self.corner_size[1])),
                                    (x, self.height - self.corner_size[1]))
                    else:
                        self.surface.blit(top_column_slice, (x, 0))
                        self.surface.blit(bottom_column_slice, (x, self.height - self.corner_size[1]))
                    step = 0
                step += 1
        
        if height_larger_than_corners:
            left_row_slice = self.source_img.subsurface(pygame.Rect(0, 
                                                                    self.corner_size[1],
                                                                    self.corner_size[0],
                                                                    source_height - (self.corner_size[1]*2)))
            

            right_row_slice = self.source_img.subsurface(pygame.Rect(source_width - self.corner_size[0], 
                                                                    self.corner_size[1],
                                                                    self.corner_size[0],
                                                                    source_height - (self.corner_size[1]*2)))
            
            slice_height = left_row_slice.get_height()
            step = slice_height

            for y in range(self.corner_size[1], (self.surface.get_height() - self.corner_size[1])):
                if step == slice_height:
                    difference = self.surface.get_height() - self.corner_size[1] - y
                    if difference < slice_height:
                        self.surface.blit(left_row_slice.subsurface(pygame.Rect(0, 0, self.corner_size[0], difference)),
                                    (0, y))
                        self.surface.blit(right_row_slice.subsurface(pygame.Rect(0, 0, self.corner_size[0], difference)),
                                    (self.surface.get_width()-self.corner_size[0], y))
                    else:
                        self.surface.blit(left_row_slice, (0, y))
                        self.surface.blit(right_row_slice, (self.surface.get_width()-self.corner_size[0], y))
                    step = 0
                step += 1

        if width_larger_than_corners and height_larger_than_corners and self.background:
            middle_slice = self.source_img.subsurface(pygame.Rect(
                self.corner_size[0],
                self.corner_size[1],
                source_width - (self.corner_size[0]*2),
                source_height - (self.corner_size[1]*2)
            ))

            slice_width, slice_height = middle_slice.get_size()

            x_step = slice_width
            y_step = slice_height
            for x in range(self.corner_size[0], self.surface.get_width()-self.corner_size[0]):
                
                if x_step == slice_width:
                    x_step = 0
                    x_difference = self.surface.get_width()-self.corner_size[0] - x

                    for y in range(self.corner_size[1], self.surface.get_height()-self.corner_size[1]):
                        if y_step == slice_height:
                            y_step = 0
                            y_difference = self.surface.get_height()-self.corner_size[1] - y
                            
                            if x_difference < slice_width or y_difference < slice_height:
                                self.surface.blit(middle_slice.subsurface(pygame.Rect(0, 0, min(x_difference, slice_width), min(y_difference, slice_height))),
                                            (x,y))
                            else:
                                self.surface.blit(middle_slice, (x, y))
                        y_step += 1
                    y_step = slice_height
                x_step += 1
        
        # drawing corners on the canvas

        self.surface.blit(topleft_corner, (0,0))
        self.surface.blit(topright_corner, (self.surface.get_width() - topright_corner.get_width(),0))
        self.surface.blit(bottomleft_corner, (0,self.surface.get_height() - bottomleft_corner.get_height()))
        self.surface.blit(bottomright_corner, (self.surface.get_width() - bottomright_corner.get_width(),self.surface.get_height() - bottomleft_corner.get_height()))