import microperf as perf
from dxfwrite import DXFEngine as dxf 

# create drawing
drawing = dxf.drawing('out.dxf')

# 60-degree hex grid
hexperf = perf.microperf_style(angle=60, grid_width=4.25, grid_height=3.25,
  border_width=8.5, border_height=8.37, tab_radius=1, suffix='A', border=True,
  label=True)
# 60-degree hex grid with much fewer points, so we can open it in AI and inspect
hexperf_tiny = perf.microperf_style(angle=60, grid_width=.25, grid_height=.25,
  border_width=8.5, border_height=8.37, tab_radius=1, suffix='A', border=True,
  label=True)

# generate microperf grids and add to drawing
perf.add_to_drawing([
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