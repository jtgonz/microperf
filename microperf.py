import numpy as np
from dxfwrite import DXFEngine as dxf 

def microperf(diameter, spacing, angle=0, border_width=8.5, border_height=8.37,
  tab_radius=1, grid_width=4.25, grid_height=3.25, offset_x=0, offset_y=0):

  # translate row/column to x and y coordinates
  def x(i, j):
    return i * dx + (j%2 and xoff) - grid_width/2 + offset_x

  def y(j):
    return j * dy - grid_height/2 + offset_y

  # calculate horizontal/vertical spacing, convert from microns to mm
  hole_radius = diameter / 2 * 1e-3
  if angle > 0:
    dx = spacing * round(2*np.cos(np.radians(angle)), 2) * 1e-3
    dy = spacing * round(np.sin(np.radians(angle)), 2) * 1e-3
    xoff = dx / 2   # horizontal offset for odd rows
  else:
    dx = dy = spacing * 1e-3
    xoff = 0

  # calculate number of holes
  nx = int(grid_width/dx + 1)
  ny = int(grid_height/dy + 1)

  # draw grid. for odd rows where angle>0, offset by xoff
  holes = [[
    dxf.circle(hole_radius, (x(i, j), y(j)), layer='holes') \
    for i in xrange(nx-1 if j%2 and angle else nx)] for j in xrange(ny) ]

  # draw the outline
  left, right, top, bot = \
    -1 * border_width/2 + offset_x, border_width/2 + offset_x, \
    border_height/2 + offset_y, -1 * border_height/2 + offset_y

  borders = []
  borders.append( dxf.line((left, bot), (left, top), layer='border') )    # left
  borders.append( dxf.line((right, bot), (right, top), layer='border') )  # right
  borders.append( dxf.line((left, bot), (right, bot), layer='border') )   # bottom

  # top and tab
  borders.append( dxf.line((left, top), (-1*tab_radius+offset_x, top),
    layer='border') )
  borders.append( dxf.line((tab_radius+offset_x, top), (right, top),
    layer='border') )
  borders.append( dxf.arc(tab_radius, (offset_x, top), 0, 180, layer='border') )

  # draw text
  text = dxf.text(str(diameter)+'-'+str(spacing)+' A',
    (left+0.5, bot+0.5), layer='text', height=1.0)

  return borders, holes, text

# when we have lists/tuples of geometries, recursively add to drawing
def add_to_drawing(geom, drawing):
  if hasattr(geom, '__iter__'):
    [add_to_drawing(g, drawing) for g in geom]
  else:
    drawing.add(geom)

# create microperf functions with specific styles (so we don't have to retype 
# keyword args every time)
def microperf_style(**kwargs):
  return lambda *args, **kwargs2: microperf(*args, **concat_dict(kwargs, kwargs2))

# util for concatenating dicts
def concat_dict(a, b):
  d = a.copy(); d.update(b); return d

# create drawing
drawing = dxf.drawing('out.dxf')

# 60-degree hex grid
hexperf = microperf_style(angle=60)
# 60-degree hex grid with much fewer points, so we can open it in AI and inspect
hexperf_tiny = microperf_style(angle=60, grid_width=.25, grid_height=.25)

# generate microperf grids and add to drawing
add_to_drawing([
  hexperf_tiny(5, 25, offset_x=20, offset_y=80),
  hexperf_tiny(5, 20, offset_x=20, offset_y=60),
  hexperf_tiny(5, 15, offset_x=20, offset_y=40),
  hexperf_tiny(5, 10, offset_x=20, offset_y=20),

  hexperf_tiny(10, 25, offset_x=40, offset_y=80),
  hexperf_tiny(10, 20, offset_x=40, offset_y=60),
  hexperf_tiny(10, 15, offset_x=40, offset_y=40),

  hexperf_tiny(15, 25, offset_x=60, offset_y=80),
  hexperf_tiny(15, 20, offset_x=60, offset_y=60),

  hexperf_tiny(20, 25, offset_x=80, offset_y=80)
], drawing)

# add 10mmx10mm square for reference
drawing.add(dxf.rectangle((75, 20), 10, 10, layer='ref'))
drawing.add(dxf.text('10mmx10mm', (75, 18), height=1, layer='text'))

drawing.save()