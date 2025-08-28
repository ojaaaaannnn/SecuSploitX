# Builder
import cmd
import time
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)

class SPLoitConsole(cmd.Cmd):
    intro = Fore.GREEN + pyfiglet.figlet_format("SPLoit") + Fore.YELLOW + "Welcome to SPLoit Console"
    prompt = Fore.CYAN + "SPLoit > "
    file = None

    def do_exit(self, arg):
        print(Fore.RED + "Exiting SPLoit Console...")
        return True

    def do_help(self, arg):
        print(Fore.YELLOW + "Available commands:")
        print(Fore.CYAN + "  help     : Show this help message")
        print(Fore.CYAN + "  exit     : Exit the console")
        print(Fore.CYAN + "  banner   : Display the banner")
        print(Fore.CYAN + "  version  : Show the version info")

    def do_banner(self, arg):
        print(Fore.GREEN + pyfiglet.figlet_format("SPLoit"))
        print(Fore.YELLOW + "⚠️ WARNING ⚠️")
        print(Fore.YELLOW + "This tool is intended for educational purposes and local testing only.")
        print(Fore.YELLOW + "Unauthorized access to systems is illegal and punishable by law.")
        print(Fore.YELLOW + "You are fully responsible for any misuse of this software.")
        print(Fore.CYAN + "Always have explicit permission before testing any website or system.")
        print(Fore.GREEN + "🚀 Welcome to SPLoit Simulator!")
        print(Fore.MAGENTA + "💡 Tip: Use responsibly, never attack live systems without consent.")
        print(Fore.BLUE + "🌐 Designed for local testing on your own setups or labs.")

    def do_version(self, arg):
        print(Fore.CYAN + "SPLoit Console Version 1.0")
        print(Fore.CYAN + "Python Version: 3.x")
        print(Fore.CYAN + "SPLoit-inspired terminal UI")

    def default(self, line):
        print(Fore.RED + f"Unknown command: {line}")
        print(Fore.YELLOW + "Type 'help' for available commands.")

if __name__ == '__main__':
    SPLoitConsole().cmdloop()
