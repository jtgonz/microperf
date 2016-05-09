# microperf.py

```
$ python microperf.py 50 100 -o 'grid.dxf'
```
Creates a file `grid.dxf`. This is a 1mm x 1mm grid with 50 um holes spaced 100 um apart.

```
$ python microperf.py 100 300 -a 60 -gw 20 -gh 20
```
Creates a file `out.dxf`. This is a 20mm x 20mm hexagonal grid with 100 um holes spaced 300 um apart.

```
usage: microperf.py [-h] [-a angle] [-gw grid width] [-gh grid height]
                    [-bw border width] [-bh border height] [-o destination]
                    diameter spacing

positional arguments:
  diameter           hole diameter
  spacing            hole spacing

optional arguments:
  -h, --help         show this help message and exit
  -a angle           angle between holes (ex. 60 for hexagonal grid)
  -gw grid width     horizontal distance that holes should span
  -gh grid height    vertical distance that holes should span
  -bw border width   rectangular border around grid (width)
  -bh border height  rectangular border around grid (height)
  -o destination     name of output file
```