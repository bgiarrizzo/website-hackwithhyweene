import subprocess

import click


@click.group()
def cli():
    """CLI utilitaire pour gérer l'application."""

@cli.command()
def build():
    """Exécute le build principal"""
    subprocess.run(["python", "src/main.py"])

@cli.command()
def dev():
    """Lance le serveur de développement"""
    subprocess.run(["python", "-m", "http.server", "8000", "--directory", "build/"])

@cli.command()
def html5validator():
    """Validateur HTML5"""
    subprocess.run(["html5validator", "--root", "build/"])

@cli.command()
def generate_docstrings():
    """Génère les docstrings des fonctions & classes"""
    subprocess.run(["pyment", "-f", "false", "-o", "numpydoc", "-w", "src"])

if __name__ == "__main__":
    cli()
