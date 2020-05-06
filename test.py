from my_utils.SqlUtils import get_result
from my_models.color import Color

colors = get_result('call get_colors(7)', Color)

for color in colors:
    print(color.__dict__)
