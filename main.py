from collections import defaultdict
from decimal import Decimal

import click


def _calculate_all_points_in_line(x1: int, y1: int, x2: int, y2: int) -> defaultdict[int, list]:
    points: defaultdict[int, list] = defaultdict(list)
    # special handling for vertical line
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            points[y].append(x1)
        return points

    # swap coordinates for negative slopes
    if x1 > x2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    slope = (y2 - y1) / (x2 - x1)

    # calculate all points in line (rounding to nearest int)
    for x in range(x1, x2 + 1):
        points[round(y1 + slope * (x - x1))].append(x)

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

    chart_x_start = min(x1, x2, 0)
    chart_y_end = min(y1, y2, 0)  # y is printed in reverse
    max_x = max(x1, x2)
    max_y = max(y1, y2)
    points = _calculate_all_points_in_line(x1, y1, x2, y2)
    y_iter = max(max_y, 10)
    for y_iter in range(max(max_y, 10), chart_y_end - 1, -1):
        click.echo(f"{y_iter:2d} ", nl=False)
        # loop through each row
        x_points = points.get(y_iter, set())
        for x in range(chart_x_start, max(max_x, 10) + 1):
            click.echo(" ● " if x in x_points else " ○ ", nl=False)

        # newline
        click.echo("")

    click.echo("   ", nl=False)
    for x in range(chart_x_start, max(max_x, 10) + 1):
        click.echo(f"{x:2d} ", nl=False)
    click.echo("\n")


@click.command()
@click.argument('point1', type=str)
@click.argument('point2', type=str)
def main(point1: str, point2: str):
    return _generate_graph(point1, point2)


TESTS = [
    ("1,1", "5,5"),
    ("5,5", "1,1"),
    ("1,1", "7,2"),
    ("1,1", "8,1"),
    ("1,1", "1,10"),
    ("10,3", "2,6"),
    ("1,10", "8,3"),
    ("-1,-1", "12,12")
]


if __name__ == '__main__':
    for xpos, ypos in TESTS:
        click.echo(f'({xpos}) -> ({ypos})\n')
        _generate_graph(xpos, ypos)
