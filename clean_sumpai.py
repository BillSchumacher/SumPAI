import glob
import os

import click


@click.command()
@click.option("--extension", default="sumpai", help="File extension to delete.")
@click.option("--path", default=".", help="Directory path to start the search.")
def delete_files(extension, path):
    files_to_delete = glob.glob(f"{path}/**/*.{extension}", recursive=True)
    for file in files_to_delete:
        try:
            os.remove(file)
            print(f"Deleted: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")


if __name__ == "__main__":
    delete_files()
