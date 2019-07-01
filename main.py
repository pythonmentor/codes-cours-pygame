from importlib import import_module

import click


@click.group()
def cli():
    pass

@click.command()
@click.option('--iteration', default=3, help="Start modules from chapter 2")
def chapter2(iteration):
    module = import_module(f'course.chapter2.example.iteration{iteration}')
    module.main()

@click.command()
@click.option('--iteration', default=5, help="Start modules from chapter 3")
def chapter3(iteration):
    module = import_module(f'course.chapter3.example.iteration{iteration}')
    module.main()

cli.add_command(chapter2)
cli.add_command(chapter3)

if __name__ == "__main__":
    cli()