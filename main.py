from decimal import Decimal

import click


def _calculate_all_points_in_line(x1: int, y1: int, x2: int, y2: int) -> dict[int, int]:
    points: dict[int, int] = {}
    slope = (y2 - y1) / (x2 - x1)
    b = y1 - slope * x1
    current_x = x1
    while current_x <= x2:
        y = int(round(Decimal(slope * current_x + b), 0))
        points[y] = current_x
        current_x += 1
    return points


def _generate_graph(point1: str, point2: str):
    click.echo('parsing inputs')
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
    click.echo(f'max x {max_x} max y {max_y}')
    points = _calculate_all_points_in_line(x1, y1, x2, y2)
    click.echo(f'got points {points}')
    y_iter = max_y
    while y_iter >= 0:
        # skip columns with no line
        line_x = points.get(y_iter, None)
        if line_x is None:
            y_iter -= 1
            continue

        # loop through each row
        x_iter = 0
        while x_iter <= max_x:
            is_line = x_iter == line_x
            x_iter += 1
            if is_line:
                click.echo("X", nl=False)
                continue
            click.echo(" ", nl=False)

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
        click.echo(f'{xpos} -> {ypos}')
        _generate_graph(xpos, ypos)
