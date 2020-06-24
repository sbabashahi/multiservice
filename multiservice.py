"""Multiservice"""

__version__ = '1.0.0'


import os
import subprocess
from typing import Any, Dict, List, Optional

import typer
import yaml
from rich import print

REQUIRED_KEYS = ['root', 'wrapper', 'services', 'commands']

app = typer.Typer()


def validate_config(config: Dict[str, Any]) -> None:
    missing_keys = [key for key in REQUIRED_KEYS if key not in config]
    if missing_keys:
        raise typer.BadParameter(f'Config misses required keys: {missing_keys}')


def parse_config(path: str) -> Dict[str, Any]:
    with open(path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    validate_config(config)
    return config


def execute_for_services(command: str, services: List[str], config: Dict[str, Any]) -> None:
    wrapper = config['wrapper'].strip()

    if command not in config['commands']:
        raise typer.BadParameter(f'Unknown command: "{command}"')

    command_from_config = config['commands'][command].strip()

    for service in services:
        service_dir = config['services'][service.upper()]
        print(f'[bold cyan]Running `{command}` for:[/bold cyan] [bold green]{service_dir}[/bold green]')

        path = os.path.join(config['root'], service_dir)
        wrapped_command = wrapper.format(PATH=path, COMMAND=command_from_config)

        subprocess.call(wrapped_command, shell=True, executable=os.environ.get('SHELL', '/bin/sh'))

        print('\n')


@app.command()
def multiservice(
    config_path: str = typer.Option('multiservice.yml', '--config', '-c'),  # noqa
    command: str = typer.Argument(...),  # noqa
    services: Optional[List[str]] = typer.Argument(None),  # noqa
) -> None:
    config = parse_config(config_path)

    services = services or list(config['services'])
    execute_for_services(command=command, services=services, config=config)


if __name__ == '__main__':
    app()
