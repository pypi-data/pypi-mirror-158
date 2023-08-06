# HowMonoPy

A Python wrapper for the c library from [how-monochromatic](https://github.com/SebTee/how-monochromatic).

#### If you need to cite this software, please cite the [how-monochromatic repository](https://github.com/SebTee/how-monochromatic) that this code wraps.

Currently supports Linux and Windows.

## Example

See the [how-monochromatic ParseBCG documentation](https://sebtee.github.io/how-monochromatic/how-monochromatic-0.1.0.0/ParseBCG.html#v:parse) for the input string format.

### Code

```python
import HowMonoPy

g = "1 green 2 green 1 0\n" \
    "1 blue 3 blue 1 0 \n" \
    "1 red 4 green 0 1 \n" \
    "1 red 6 red 1 0 \n" \
    "2 red 3 red 1 0 \n" \
    "2 blue 5 blue 1 0 \n" \
    "3 green 4 green 1 0 \n" \
    "3 green 6 red 0 1 \n" \
    "4 red 5 red 1 0 \n" \
    "4 red 6 green 0 1 \n" \
    "4 blue 6 blue 1 0 \n" \
    "5 green 6 green 1 0 "

print(HowMonoPy.how_mono(g))

```

### Output

```
0.5
```
