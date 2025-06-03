from colorama import Fore, Style, init as colorama_init

colorama_init(autoreset=True)

COLORS = {
    "user": Fore.CYAN,
    "assistant": Fore.GREEN,
    "tool": Fore.YELLOW,
    "system": Fore.MAGENTA,
    "error": Fore.RED,
    "info": Fore.BLUE,
}


def cprint(role, msg):
    """
    Imprime un mensaje colorido con un identificador de rol.
    Ejemplo: cprint("user", "Hola mundo!")
    """
    color = COLORS.get(role, Fore.WHITE)
    print(f"{color}[{role.upper()}]{Style.RESET_ALL} {msg}")
