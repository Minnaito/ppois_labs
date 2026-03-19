#!/usr/bin/env python3
"""Main entry point for the Product Management System."""
from controllers.main_controller import MainController


def main():
    """Main function to start the application."""
    app = MainController()
    app.run()


if __name__ == "__main__":
    main()
