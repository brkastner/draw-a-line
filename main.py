from collections import defaultdict
from decimal import Decimal

import click


def _calculate_all_points_in_line(x1: int, y1: int, x2: int, y2: int) -> defaultdict[int, list]:
    points: defaultdict[int, list] = defaultdict(list)
    # special handling for vertical line
    if (start_x := min(x1, x2)) == (end_x := max(x1, x2)):
        for y in range(min(y2, y1), max(y2, y1) + 1):
            points[y].append(start_x)
        return points

    # solve for y = mx + b
    slope = (y2 - y1) / (end_x - start_x)
    b = int(round(y1 - slope * x1, 0))

    current_x = start_x
    while current_x <= end_x:
        points[int(round(slope * current_x, 0) + b)].append(current_x)
        current_x += 1
    return points


def _generate_graph(point1: str, point2: str):
    try:
        x1, y1 = point1.split(',')
        x1 = int(x1)
        y1 = int(y1)
        x2, y2 = point2.split(',')
        x2 = int(x2)
        y2 = int(y2)
    except:
        click.echo('invalid inputs! please use the format x,y x,y')
        return

    max_x = max(x1, x2)
    max_y = max(y1, y2)
    points = _calculate_all_points_in_line(x1, y1, x2, y2)
    y_iter = max(max_y, 10)
    while y_iter >= 0:
        # loop through each row
        x_points = points.get(y_iter, set())
        x_iter = 0
        while x_iter <= max(max_x, 10):
            click.echo(" ● " if x_iter in x_points else " ○ ", nl=False)
            x_iter += 1

        # newline
        click.echo("")
        y_iter -= 1


@click.command()
@click.argument('point1', type=str)
@click.argument('point2', type=str)
def main(point1: str, point2: str):
    return _generate_graph(point1, point2)


TESTS = [
    ("1,1", "5,5"),
    ("5,5", "1,1"),
    ("1,1", "5,2"),
    ("1,1", "5,1"),
    ("1,1", "1, 10")
]


if __name__ == '__main__':
    for xpos, ypos in TESTS:
        click.echo(f'({xpos}) -> ({ypos})')
        _generate_graph(xpos, ypos)
