import pathlib

import click

from . import download_data


@click.group()
def main():
    pass


@click.command()
def download():
    click.echo("downloading...")
    output_path = pathlib.Path("data")
    output_path.mkdir(exist_ok=True)

    download_data.download_skills(output_path / "skills.json")
    download_data.download_classes(output_path / "classes.json")
    download_data.download_items(output_path / "items.json")


main.add_command(download)
