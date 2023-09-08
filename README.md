# SPGExpand
### Sphere's Pygame Expandable Surface Tool

This is a very simple tool for making expandable surfaces with a border. The surface will maintain its pattern as long 
as it is repeatable.

## [Example Program](example.py)

## Documentation

```py
SPGExpandableSurface(self,
                 source_img: pygame.Surface,
                 width: int,
                 height: int,
                 corner_size: tuple[int, int],
                 background: bool = True,
                 gen_on_load: bool = True) -> None
```
Arguments:
 - `source_img` = Source image for your surface. this should be structured like [Example Surface](example_surface.png).
 - `width` = Width of surface (including border)
 - `height` = Height of surface (including border)
 - `corner_size` = Width and height of corners
 - `background` = Toggle filling the background.
 - `gen_on_load` = Toggle generating on load.

```py
gen_surface(self)
```
 - Creates empty surface of size `(width, height)` with `pygame.SRCALPHA` as a default flag.
 - Early return if width and height equal source image.
 - Creates subsurfaces for all four corners.
 - Depending on parameters, top, bottom, left, and right slices are created from `source_img`
 - Slices are blitted to surface until they fill up the necessary space.