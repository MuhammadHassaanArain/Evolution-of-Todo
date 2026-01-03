def main():
    """Main entry point for the Todo CLI application."""
    from src.todo.cli.cli_app import TodoCLIApp
    app = TodoCLIApp()
    app.run()


if __name__ == "__main__":
    main()
