import argparse
import numpy as np
from dxfwrite import DXFEngine as dxf 

def microperf(diameter, spacing, angle=0, border_width=None, border_height=None,
  tab_radius=0, grid_width=4.25, grid_height=3.25, offset_x=0, offset_y=0,
  suffix='', border=False, label=False):

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

  # if border is not specified, just outline the grid
  border_width = border_width or (grid_width + 2 * hole_radius)
  border_height = border_height or (grid_height + 2 * hole_radius)

  # calculate number of holes
  nx = int(grid_width/dx + 1)
  ny = int(grid_height/dy + 1)

  # draw grid. for odd rows where angle>0, offset by xoff
  holes = [[
    dxf.circle(hole_radius, (x(i, j), y(j)), layer='holes') \
    for i in xrange(nx-1 if j%2 and angle else nx)] for j in xrange(ny) ]

  # get boundaries
  left, right, top, bot = \
    -1 * border_width/2 + offset_x, border_width/2 + offset_x, \
    border_height/2 + offset_y, -1 * border_height/2 + offset_y

  # draw the outline
  borders = []
  if border:
    borders.append(dxf.line((left, bot), (left, top), layer='border'))   # left
    borders.append(dxf.line((right, bot), (right, top), layer='border')) # right
    borders.append(dxf.line((left, bot), (right, bot), layer='border'))  # bottom

    # top and tab
    if tab_radius:
      borders.append(dxf.line((left, top), (-1*tab_radius+offset_x, top),
        layer='border') )
      borders.append(dxf.line((tab_radius+offset_x, top), (right, top),
        layer='border') )
      borders.append(dxf.arc(tab_radius, (offset_x, top), 0, 180, layer='border'))
    else:
        borders.append(dxf.line((left, top), (right, top), layer='border') )

  # draw text
  text = []
  if label: text.append(dxf.text(str(diameter)+'-'+str(spacing)+' '+suffix,
    (left+0.5, bot+0.5), layer='text', height=1.0))

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

if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  # these arguments are required
  parser.add_argument('diameter', type=float, help='hole diameter')
  parser.add_argument('spacing', type=float, help='hole spacing')

  # these are optional
  parser.add_argument('-a', metavar='angle', type=float,
    help='angle between holes (ex. 60 for hexagonal grid)', default=0.0)
  parser.add_argument('-gw', metavar='grid width', type=float,
    help='horizontal distance that holes should span', default=1.0)
  parser.add_argument('-gh', metavar='grid height', type=float,
    help='vertical distance that holes should span', default=1.0)
  parser.add_argument('-bw', metavar='border width', type=float,
    help='rectangular border around grid (width)', default=None)
  parser.add_argument('-bh', metavar='border height', type=float,
    help='rectangular border around grid (height)', default=None)
  parser.add_argument('-o', metavar='destination', type=str,
    help='name of output file', default='out.dxf')

  args = parser.parse_args()

  # if no border params were passed, border is False. If just one was passed,
  # border is a square -- set width equal to height or vice versa
  border = True if args.bw or args.bh else False
  args.bw = args.bw or args.bh
  args.bh = args.bh or args.bw

  drawing = drawing = dxf.drawing(args.o)
  add_to_drawing( microperf(args.diameter, args.spacing, angle=args.a,
    border_width=args.bw, border_height=args.bh, grid_width=args.gw,
    grid_height=args.gh, border=border), drawing )
  drawing.save()