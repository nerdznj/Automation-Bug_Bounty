from rich.console import Console
from rich.panel import Panel

console = Console()

def notify(title, message, style="bold green"):
    console.print(Panel(message, title=title, style=style))