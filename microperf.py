import numpy as np
from dxfwrite import DXFEngine as dxf 

def microperf(diameter, spacing, border_width=8.5, border_height=8.37,
  tab_radius=1, grid_width=.25, grid_height=.25, offset_x=0, offset_y=0):

  # convert from microns to mm
  hole_radius = diameter / 2 * 1e-3
  dx = spacing * 1e-3
  dy = np.sin(np.radians(60)) * spacing * 1e-3
  xoff = dx / 2

  print dx, dy, xoff

  # translate row/column to x and y coordinates
  def x(i, j):
    return i * dx + (j%2 and xoff) - grid_width/2 + offset_x

  def y(j):
    return j * dy - grid_height/2 + offset_y

  # calculate number of holes
  nx = int(grid_width/dx + 1)
  ny = int(grid_height/dy + 1)

  # draw grid
  holes = [[
    dxf.circle(hole_radius, (x(i, j), y(j)), layer='holes') \
    for i in xrange(nx-1 if j%2 else nx)] for j in xrange(ny) ]

  for j in xrange(ny):
    for i in xrange(nx-1 if j%2 else nx):
      print (x(i, j), y(j))

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

# create drawing
drawing = dxf.drawing('out.dxf')

# generate elements
elements = [
  microperf(5, 25, offset_x=20, offset_y=80),
  microperf(5, 20, offset_x=20, offset_y=60),
  microperf(5, 15, offset_x=20, offset_y=40),
  microperf(5, 10, offset_x=20, offset_y=20),

  microperf(10, 25, offset_x=40, offset_y=80),
  microperf(10, 20, offset_x=40, offset_y=60),
  microperf(10, 15, offset_x=40, offset_y=40),

  microperf(15, 25, offset_x=60, offset_y=80),
  microperf(15, 20, offset_x=60, offset_y=60),

  microperf(20, 25, offset_x=80, offset_y=80)
]

for element in elements:
  for i in element[0]:
    drawing.add(i)
  print element[0][0]
  for i in element[1]:
    for j in i:
      drawing.add(j)
  print element[1][0][0]
  drawing.add(element[2])
  print element[2]

# add 10mmx10mm square
drawing.add(dxf.rectangle((75, 20), 10, 10, layer='ref'))
drawing.add(dxf.text('10mmx10mm', (75, 18), height=1, layer='text'))

drawing.save()