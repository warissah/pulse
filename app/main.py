# This is the main entry point for the Pulse FastAPI application
# 
# importing fastapi class from the package we installed
from fastapi import FastAPI

app = FastAPI() #creates the application 

@app.get("/") #connects a web address to a python function
def root():
    return {"message": "Pulse is alive"}