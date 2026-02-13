"""Main CLI entry point for Research Agent."""

import sys
from pathlib import Path
from datetime import datetime
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

from src.config import Config
from src.collectors import XCollector, WebCollector
from src.analyzers import ClaudeAnalyzer, GeminiAnalyzer
from src.generators import MarkdownGenerator
from src.utils import get_logger, validate_topic, validate_sources, validate_depth
from src.utils.validators import validate_max_items

console = Console()
logger = get_logger("main")


@click.command()
@click.option(
    "--topic",
    required=True,
    help="Research topic to investigate",
    callback=lambda ctx, param, value: validate_topic(value) if value else None
)
@click.option(
    "--sources",
    default=Config.DEFAULT_SOURCES,
    help="Data sources to use: x, web, or all (default: all)",
    callback=lambda ctx, param, value: validate_sources(value)
)
@click.option(
    "--max-items",
    default=Config.DEFAULT_MAX_ITEMS,
    type=int,
    help=f"Maximum items to collect per source (default: {Config.DEFAULT_MAX_ITEMS})",
    callback=lambda ctx, param, value: validate_max_items(value)
)
@click.option(
    "--output",
    default=None,
    help="Output filename (default: auto-generated)",
    type=str
)
@click.option(
    "--depth",
    default=Config.DEFAULT_DEPTH,
    help="Analysis depth: quick or detailed (default: detailed)",
    callback=lambda ctx, param, value: validate_depth(value)
)
@click.option(
    "--model",
    default=Config.DEFAULT_MODEL,
    type=click.Choice(["claude", "gemini"], case_sensitive=False),
    help=f"AI model to use: claude or gemini (default: {Config.DEFAULT_MODEL})"
)
@click.version_option(version="0.1.0", prog_name="Research Agent")
def cli(topic: str, sources: list, max_items: int, output: str, depth: str, model: str):
    """
    Research Agent - AI-powered research automation tool.

    Automatically collects data from X and web search, analyzes it with AI,
    and generates comprehensive Markdown reports.

    Example:

        research-agent --topic "AI agents 2024"

        research-agent --topic "Anthropic Claude" --sources x,web --max-items 30 --model gemini
    """
    console.print("\n[bold cyan]🔬 Research Agent[/bold cyan]")
    console.print(f"[dim]Topic: {topic}[/dim]")
    console.print(f"[dim]Sources: {', '.join(sources)}[/dim]")
    console.print(f"[dim]Max items per source: {max_items}[/dim]")
    console.print(f"[dim]Analysis depth: {depth}[/dim]")
    console.print(f"[dim]AI Model: {model}[/dim]\n")

    try:
        # Validate configuration
        Config.validate(model=model)
        Config.ensure_output_dir()

        # Initialize components
        collectors = {
            "x": XCollector() if "x" in sources else None,
            "web": WebCollector() if "web" in sources else None,
        }

        # Select analyzer based on model choice
        if model.lower() == "claude":
            analyzer = ClaudeAnalyzer()
            model_display = "Claude AI"
        else:  # gemini
            analyzer = GeminiAnalyzer()
            model_display = "Gemini AI"

        generator = MarkdownGenerator()

        # Step 1: Collect data
        all_data = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:

            if collectors["x"]:
                task = progress.add_task(
                    f"🔍 Collecting X data... (0/{max_items})",
                    total=max_items
                )
                x_data = collectors["x"].collect(topic, max_items)
                all_data.extend(x_data)
                progress.update(task, completed=len(x_data))
                console.print(f"[green]✓[/green] Collected {len(x_data)} X posts")

            if collectors["web"]:
                task = progress.add_task(
                    f"🌐 Collecting web data... (0/{max_items})",
                    total=max_items
                )
                web_data = collectors["web"].collect(topic, max_items)
                all_data.extend(web_data)
                progress.update(task, completed=len(web_data))
                console.print(f"[green]✓[/green] Collected {len(web_data)} web results")

        if not all_data:
            console.print("[red]❌ No data collected. Exiting.[/red]")
            sys.exit(1)

        console.print(f"\n[cyan]Total items collected: {len(all_data)}[/cyan]\n")

        # Step 2: Analyze with AI
        with console.status(f"[bold yellow]🤖 Analyzing with {model_display}...[/bold yellow]"):
            analysis_result = analyzer.analyze(topic, all_data, depth)

        if not analysis_result.get("success"):
            console.print(f"[red]❌ Analysis failed: {analysis_result.get('error')}[/red]")
            sys.exit(1)

        metadata = analysis_result.get("metadata", {})
        console.print(f"[green]✓[/green] Analysis completed")
        console.print(f"[dim]  Tokens used: {metadata.get('tokens_used', 'N/A')}[/dim]\n")

        # Step 3: Generate report
        with console.status("[bold yellow]📝 Generating report...[/bold yellow]"):
            # Determine output path
            if output:
                output_path = Config.OUTPUT_DIR / output
                if not output_path.suffix:
                    output_path = output_path.with_suffix(".md")
            else:
                filename = generator.generate_filename(topic)
                output_path = Config.OUTPUT_DIR / filename

            # Organize sources
            sources_organized = analyzer.summarize_sources(all_data)

            # Generate report
            success = generator.generate_report(
                topic,
                analysis_result,
                sources_organized,
                output_path
            )

        if success:
            console.print(f"[green]✓[/green] Report generated successfully!\n")
            console.print(f"[bold]📄 Report saved to:[/bold] [cyan]{output_path}[/cyan]\n")
            console.print("[dim]You can open it with any Markdown viewer or editor.[/dim]")
        else:
            console.print("[red]❌ Failed to generate report[/red]")
            sys.exit(1)

    except ValueError as e:
        console.print(f"[red]❌ Configuration error: {e}[/red]")
        console.print("\n[yellow]💡 Tip:[/yellow] Make sure to:")
        console.print("  1. Copy .env.example to .env")
        console.print("  2. Add your API keys to .env file")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Operation cancelled by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        console.print(f"[red]❌ Unexpected error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
