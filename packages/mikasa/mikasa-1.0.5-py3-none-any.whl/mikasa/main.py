import typer
import os
from .db import delete, draw,fetch,drop
from .db import insert as insert_data



# draw the database 
draw()

print("-"*20,"\n")

app = typer.Typer()


@app.command()
def dropall():
    drop()

@app.command()
def insert(name,path):
    insert_data(name,path)

@app.command()
def mostaql():
    os.chdir("E:\\mostaql")

@app.command()
def get(name):
    fetch(name)

@app.command()
def go(project_name):
    
    if not fetch(project_name):
        
        exit()
    
    os.chdir(fetch(project_name))
    os.system("code .")

@app.command()
def remove(name):
    delete(name)




if __name__ == '__main__':
    app()