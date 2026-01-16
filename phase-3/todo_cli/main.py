#!/usr/bin/env python3
"""
Todo CLI Application Entry Point

This is the main entry point for the Todo CLI application.
It initializes the application and starts the CLI interface.
"""

from todo.cli.cli_app import TodoCLIApp


def main():
    """Main entry point for the Todo CLI application."""
    app = TodoCLIApp()
    app.run()


if __name__ == "__main__":
    main()