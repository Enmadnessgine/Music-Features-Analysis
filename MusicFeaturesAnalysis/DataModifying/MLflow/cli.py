import typer

app = typer.Typer()

from DataModifying.MLflow.registry_train import get_trainer

@app.command()
def train(model: str = typer.Argument(..., help="genre | subgenre | mood"),
          grid: bool = False,
          save: bool = False,
          macrogenre: str = typer.Argument(False, help="vocal | energetic | acoustic | calm")):
    trainer = get_trainer(model)
    trainer(grid, save, macrogenre)


if __name__ == "__main__":
    app()