from typing import Callable, Union
from time import time
from threading import Thread
from multiprocessing import Process
from functools import wraps
from time import sleep

def replace_str_index(text: str, index: int, replacement: Union[str, int]) -> str:
    """
    Info:
        Replaces the indexed part of the string with the replacement then returns the new string.
    
    Paramaters: 
        text: str - The string of text.
        index: int - Index of the character to replace.
        replacement: str - The replacement character(s)

    Usage:
        replace_str_index(text, index, replacement)

    Returns:
        str
    """
    return f'{text[:index]}{replacement}{text[index+1:]}'


def is_even(number: int) -> bool:
    """
    Info:
        Check if a number is even, if so return True if not return False
    
    Paramaters:
        number: int - The number to check if is even.

    Usage:
        is_even(number)

    Returns:
        bool
    """
    return number % 2 == 0

def is_prime(number: int) -> bool:
    """
    Info:
        Check if a number is prime, if so return True if not return False
    
    Paramaters:
        number: int - The number to check if is prime.

    Usage:
        is_prime(number)

    Returns:
        bool
    """
    if number <= 0: return False
        
    for i in range(2, number):
        if number % i == 0: return False

    return True

def remove_list_duplicates(list: list, amount: int = 1) -> list:
    """
    Info:
        Removes any duplicates from the list given with the amount, then retursn that list
    
    Paramaters:
        list: list - The list to remove duplicates from.
        [Optional]amount: int -> 1 - Amount of duplicates wanted

    Usage:
        remove_list_duplicates(list)

    Returns:
        list
    """
    clean_list = []
    for item in list:
        if clean_list.count(item) < amount:
            clean_list.append(item)
    return clean_list

def timer(raw_format: bool = False) -> Callable:
    """
    Info:
        Times the function and logs how long it takes in seconds.

    Paramaters:
        [Optional]raw_format: bool -> False - If true, prints out the seconds the function took only.

    Usage:
        @timer(*args)
        def my_function(a: int, b: str) -> None:
    """
    
    def decorator(function: Callable, *args, **kwargs) -> Callable:
        
        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            start_time = time()
            function(*args, **kwargs)
            end_time = time()
            if raw_format: 
                print(end_time - start_time)
                return

            print(f'Function {function.__name__} ran in {end_time - start_time} seconds.')
            return

        return wrapper_function
    return decorator

def no_error(view=False) -> Callable:
    """
    Info:
        Ignores errors thrown in a function.

    Paramaters:
        [Optional]view: bool -> False - To view the simplified error.
    
    Usage:
        @no_error(*args)
        def my_function(a: int, b: str) -> None:
    """

    def decorator(function: Callable, *args, **kwargs) -> Callable:

        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            try:
                function(*args, **kwargs)
            except Exception as error:
                if view: print(f'{function.__name__}: error "{error}"')
                pass
                
        return wrapper_function
    return decorator
    

def thread() -> Callable:
    """
    Info:
        Threads the given function and passes its paramaters
    
    Usage:
        @thread(*args)
        def my_function(a: int, b: str) -> None:
    """
    
    def decorator(function: Callable, *args, **kwargs) -> Callable:
        
        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            Thread(target=function, args=args, kwargs=kwargs).start()

        return wrapper_function
    return decorator

def multiprocess() -> Callable:
    """
    Info:
        processes the given function and passes its paramaters
    
    Usage:
        @multiprocess(*args)
        def my_function(a: int, b: str) -> None:
    """
    
    def decorator(function: Callable, *args, **kwargs) -> Callable:
        
        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            Process(target=function, args=args, kwargs=kwargs).start()

        return wrapper_function
    return decorator

def wait(before_time: int, after_time: int) -> Callable:
    """
    Info:
        Waits time before and after calling the function.

    Paramaters:
        before_time: int - Time to wait before calling the function.
        after_time: int - Time to wait after calling the function

    Usage:
        @wait(*args)
        def my_function(a: int, b: str) -> None:
    """

    def decorator(function: Callable, *args, **kwargs) -> Callable:

        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            sleep(before_time)
            function(*args, **kwargs)
            sleep(after_time)

        return wrapper_function
    return decorator

def repeat(amount: int = 1, time: int = 0) -> Callable:
    """
    Info:
        Repeats the function specified times and waits after each function call.

    Paramaters:
        [Optional]amount: int -> 1 - Amount of times to repeat.
        [Optional]time: int -> 1 - How long to wait after each function call

    Usage:
        repeat(*args)
        def my_function(a: int, b: str) -> None:
    """
    
    def decorator(function: Callable, *args, **kwargs) -> Callable:
        
        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            for i in range(amount):
                function(*args, **kwargs)
                sleep(time)
                
        return wrapper_function
    return decorator

class Colors:
    """
    Info:
        Contains sub classes to add styling and colors to your string.

    Options:
        Styles
        Foreground
        Background

    Usage:
        Colors.Style.Color
    """
    class Styles:
        """
        Info: 
            Styles your text in different ways.

        Usage:
            Colors.Styles.Style

        Options:
            reset
            bold
            disable
            underline
            reverse
            strikethrough
            invisible

        Returns:
            str
        """
        styles: dict = {
            'reset': '\033[0m',
            'bold': '\033[01m',
            'disable': '\033[02m',
            'underline': '\033[04m',
            'reverse': '\033[07m',
            'strikethrough': '\033[09m',
            'invisible': '\033[08m'
        }
        reset='\033[0m'
        bold='\033[01m'
        disable='\033[02m'
        underline='\033[04m'
        reverse='\033[07m'
        strikethrough='\033[09m'
        invisible='\033[08m'
    
    class Foreground:
        """
        Info: 
            Colors your text.

        Usage:
            Colors.Foreground.Color

        Options:
            black
            red
            green
            orange
            blue
            purple
            cyan
            lightgray
            darkgrey
            lightred
            lightgreen
            yellow
            lightblue
            pink
            lightcyan
        
        Returns:
            str
        """
        foregrounds: dict = {
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'orange': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'lightgray': '\033[37m',
            'darkgray': '\033[90m',
            'lightred': '\033[91m',
            'lightgreen': '\033[92m',
            'yellow': '\033[93m',
            'lightblue': '\033[94m',
            'pink': '\033[95m',
            'lightcyan': '\033[96m'
        }
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
        
    class Background:
        """
        Info: 
            Colors the background of your text.

        Usage:
            Colors.Background.Color

        Options:
            black
            red
            green
            orange
            blue
            purple
            cyan
            lightgray

        Returns:
            str
        """
        backgrounds: dict = {
            'black': '\033[40m',
            'red': '\033[41m',
            'green': '\033[42m',
            'orange': '\033[43m',
            'blue': '\033[44m',
            'purple': '\033[45m',
            'cyan': '\033[46m',
            'lightgray': '\033[47m'
        }
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'


def color(text: str, styles: list = None, foreground: str = None, background: str = None) -> str:
    """
    Info: 
        Takes in different styles to color or style given text with ascii.

    Paramaters:
        text: str - The text to color.
        [Optional]styles: list -> None - Different styles for the text.
        [Optional]foreground: str -> None - The foreground color.
        [Optional]background: str -> None - The background color.

    Usage:
        color(*args)

    Returns:
        str
    """
    if not text:
        return
        
    if styles:
        for style in styles:
            if style in Colors.Styles.styles:
                text = f'{Colors.Styles.styles[style]}{text}'
                
    if foreground:
        if foreground in Colors.Foreground.foregrounds:
            text = f'{Colors.Foreground.foregrounds[foreground]}{text}'
            
    if background:
        if background in Colors.Background.backgrounds:
            text = f'{Colors.Background.backgrounds[background]}{text}'    

    text = f'{text}{Colors.Styles.reset}'

    return text

class Log:
    """
    Info:
        Has several functions to log out information to the user.

    Functions:
        warn: Callable - Warns the user with given text.
        error: Callable - Sends the user a error with given text.
        log: Callable - Logs information to the user with given text.
        alert: Callable - Alerts the user with given text.

    Usage:
        Log().function(*args)

    Returns:
        None
    """
    def warn(self, text: str) -> None:
        """
        Info:
            Warns the user via the terminal.

        Paramaters:
            text: str - Text to warn the user with.

        Usage:
            Log().warn(*args)

        Returns:
            None
        """
        print(f'{color(text="WARNING:", foreground="orange", styles=["underline"])}\n    {color(text=text, foreground="orange", styles=["bold"])}')

    def error(self, text: str) -> None:
        """
        Info:
            Prints a error via the terminal.

        Paramaters:
            text: str - Text to print the user with.

        Usage:
            Log().error(*args)

        Returns:
            None
        """
        print(f'{color(text="ERROR:", foreground="red", styles=["underline"])}\n    {color(text=text, foreground="red", styles=["bold"])}')

    def log(self, text: str) -> None:
        """
        Info:
            Displays information via the terminal.

        Paramaters:
            text: str - Text to display the user with.

        Usage:
            Log().log(*args)

        Returns:
            None
        """
        print(f'{color(text="INFO:", foreground="lightgray", styles=["underline", "disable"])}\n    {color(text=text, foreground="lightgray", styles=["bold", "disable"])}')

    def alert(self, text: str) -> None:
        """
        Info:
            Alerts the user via the terminal.

        Paramaters:
            text: str - Text to alert the user with.

        Usage:
            Log().alert(*args)

        Returns:
            None
        """
        print(f'{color(text="ALERT:", foreground="yellow", styles=["underline"])}\n    {color(text=text, foreground="yellow", styles=["bold"])}')
    
