import math
import click
from rich.console import Console
from rich.table import Table
import math

def get_interval_numbers(interval: str):
  p1 = float(interval.split(',')[0].split('[')[1])
  p2 = float(interval.split(',')[1].split(']')[0])
  return p1, p2


def get_parsed_func(function: str):
  return lambda x: eval(function)


def secant_method(p1, p2, func):
  return (p2 - ((func(p2) * (p2 - p1)) / (func(p2) - func(p1))))


def percentage_error(current, previous) -> float:
  return abs(((current - previous) / current) * 100)


def set_table(func: str):
  table = Table(title=f'Secant Method: {func}')

  table.add_column("Iteration", justify="center", style="cyan")
  table.add_column("Interval", justify="center", style="cyan")
  table.add_column("f(P1)", justify="center", style="cyan")
  table.add_column("f(P2)", justify="center", style="cyan")
  table.add_column("Secant Method Result", justify="center", style="cyan")
  table.add_column("f(x) result", justify="center", style="cyan")
  table.add_column("Percentage Error", justify="center", style="cyan")
  return table


def get_number_sign(n: float) -> str:
  return '+' if n >= 0 else '-'


def add_row(table: Table, iteration: int, a: float, b: float, result: float,
            error: float, func):
  table.add_row(str(iteration), f'[{round(a,8)},{round(b,8)}]',
                str(round(func(a), 8)), str(round(func(b), 8)),
                str(round(result, 8)), str(round(func(result), 8)),
                f'{round(error, 5)}%')


@click.command()
@click.option('--interval', help='function interval', type=str, required=True)
@click.option('--function',
              help='function to do the calculus',
              type=str,
              required=True)
@click.option('--error', help='error', type=float, required=True)
def run(interval: str, function: str, error: str):
  console = Console()
  table = set_table(function)
  func = get_parsed_func(function)
  p1, p2 = get_interval_numbers(interval)
  current_error = 100
  iteration = 1
  previous_result = 0
  while current_error > error:
    current_result = secant_method(p1, p2, func)
    current_error = percentage_error(current_result, previous_result)
    add_row(table, iteration, p1, p2, current_result, current_error, func)
    if func(current_result) < p2:
      p1 = current_result
    else:
      p2 = current_result

    previous_result = current_result
    iteration += 1
  console.print(table)


if __name__ == '__main__':
  run()
