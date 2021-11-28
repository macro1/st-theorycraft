import invoke


@invoke.task
def lint(c):
    for command in ["isort", "black", "mypy", "flake8"]:
        print(f"Running {command}...")
        c.run(f"{command} .", pty=True)
