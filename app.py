import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess
import asyncio

app = FastAPI()

# Serve static files like CSS/JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates folder for rendering HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit_prompt(request: Request):
    form = await request.form()
    prompt = form.get("prompt", "")

    os.environ["MCP_PROMPT"] = prompt
    process = await asyncio.create_subprocess_exec(
        "python", "main.py",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )
    stdout, _ = await process.communicate()
    output = stdout.decode()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "prompt": prompt,
        "output": output
    })
