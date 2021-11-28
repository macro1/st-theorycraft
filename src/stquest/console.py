import click

from . import optimize_hero


@click.group()
def main():
    pass


@click.command()
@click.option("--class", "hero_class", default="dancer", help="Hero class to optimize")
@click.option("--level", "hero_level", default=40, help="Hero level")
@click.option("--quality", "gear_quality", default="superior", help="Gear quality")
@click.option("--skill", "skills", multiple=True)
def optimize(hero_class, hero_level, gear_quality, skills):
    hero = optimize_hero.run(
        hero_class_name=hero_class,
        hero_level=hero_level,
        gear_quality=gear_quality,
        override_skills=skills,
    )
    skill_names = [s.name for s in hero.skills]
    click.echo(
        f"""Class: {hero.hero_class.name} ({hero.hero_class.class_type})
Stats:
  HP: {hero.stat_hp}
  ATK: {hero.stat_atk}
  DEF: {hero.stat_def}
  EVA: {hero.stat_eva}
Skills: {skill_names}
Items: {[i.blueprint.name for i in hero.items]}"""
    )


main.add_command(optimize)
