from typing import Callable, Union
from time import time, sleep
from datetime import datetime
from threading import Thread
from multiprocessing import Process
from functools import wraps
from json import load as json_load, dump
from yaml import safe_load as yaml_load
from math import sqrt
from requests import get
from statistics import mean, median
from hashlib import sha256
from js2py import run_file

def get_time() -> dict:
    """
    Info:
        Returns the time in different ways via a dictionary/

    Usage;
        get_time()

    Returns:
        dict
    """
    time = datetime.now()
    return {
        'millisecond': time.microsecond, 
        'second': time.second, 
        'minute': time.minute, 
        'hour': time.hour, 
        'day': time.day, 
        'month': time.month, 
        'year': time.year, 
        'date': time.strftime("%m/%d/%Y %H:%M")
    }

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

def prime_factors(number: int) -> list:
    """
    Info:
        Generates a list of prime numbers that are factors of the given number.

    Paramaters:
        number: int - The number to get prime factors of.

    Usage:
        prime_facotrs(100)

    Returns:
        list
    """
    factors = []
    if is_prime(number) or number < 3:
        return factors
        
    for i in range(2, number):
        if number % i == 0 and is_prime(i):
            factors.append(i)
            
    return factors
    
def convert_list_items(old_list: list, convert_type: type):
    """
    Info:
        Converts each list item to the type specified
    
    Paramaters:
        old_list: list - List to convert
        convert_type: type - The type to convert to.

    Usage:
        convert_list_items(old_list, convert_type)

    Returns:
        list
    """
    new_list = []
    for item in old_list:
        new_list.append(convert_type(item))
    return new_list

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
        @timer(raw_format=False)
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

def no_error(view: bool =False) -> Callable:
    """
    Info:
        Ignores errors thrown in a function.

    Paramaters:
        [Optional]view: bool -> False - To view the simplified error.
    
    Usage:
        @no_error(view=False)
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
        @thread()
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
        @multiprocess()
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
        @wait(before_time=1, after_time=1)
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

def average_time(amount: int) -> Callable:
    """
    Info:
        Runs the function x amount of times and then collects how long it took to run, after that gets the mean of the list of times to run.

    Paramaters:
        amount: int - The amount of times you want calculated.

    Usage:
        @average_time(amount=1)
        def my_function(a: int, b: str) -> None:
    """
    def decorator(function: Callable, *args, **kwargs) -> Callable:

        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            times = []
            for i in range(amount):
                start_time = time()
                function(*args, **kwargs)
                end_time = time()
                times.append(end_time - start_time)
            print(f"{function.__name__}: {amount} loops\nTotal time: {sum(times)}\nAverage time: {get_mean(times)}\nLowest Time: {min(times)}\nHighest Time: {max(times)}\nAll times: {', '.join(convert_list_items(times, str))}\n")

        return wrapper_function
    return decorator
            

def repeat(amount: int = 1, time: int = None) -> Callable:
    """
    Info:
        Repeats the function specified times and waits after each function call.

    Paramaters:
        [Optional]amount: int -> 1 - Amount of times to repeat.
        [Optional]time: int -> 1 - How long to wait after each function call

    Usage:
        repeat(amount=1, time=1)
        def my_function(a: int, b: str) -> None:
    """
    
    def decorator(function: Callable, *args, **kwargs) -> Callable:
        
        @wraps(function)
        def wrapper_function(*args, **kwargs) -> None:
            for i in range(amount):
                function(*args, **kwargs)
                if time:
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
        color(text, styles=[], foreground='', background='')

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
        Log().function(text)

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
            Log().warn(text)

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
            Log().error(text)

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
            Log().log(text)

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
            Log().alert(text)

        Returns:
            None
        """
        print(f'{color(text="ALERT:", foreground="yellow", styles=["underline"])}\n    {color(text=text, foreground="yellow", styles=["bold"])}')


def load_json(file_name: str):
    """
    Info:
        Loads the given json file and returns its value.

    Paramaters:
        file_name: str - File name, ending with .json.

    Usgae:
        load_json(file)

    Returns:
        dict
    """
    
    with open(file_name, 'r') as my_file_raw:
        my_file = json_load(my_file_raw)
        return my_file

def load_yaml(file_name: str):
    """
    Info:
        Loads the given yaml file and returns its value.

    Paramaters:
        file_name: str - File name, ending with .yaml or .yml.

    Usgae:
        load_yaml(file)

    Returns:
        dict
    """
    
    with open(file_name, 'r') as my_file_raw:
        my_file = yaml_load(my_file_raw)
        return my_file

def square_root(number: int) -> int:
    """
    Info:
        Returns the square root of a number.

    Paramaters:
        number: int - The number to get the square root of.

    Usage:
        square_root(number)

    Returns:
        int
    """
    
    return sqrt(number)

def true_or_false() -> dict:
    """
    Info:
        Returns a dict that contains two list, containing words if its true/false acceptance.
    
    Usage:
        true_or_false()

    Returns:
        dict
    """
    
    return {
        'true': [
            'true',
            'y',
            'ye',
            'yes',
            'yeah',
            'yup',
            'accept',
            'confirm',
            'mhmm',
            'ok',
            'sure',
            'alright'
        ], 
        'false': [
            'false',
            'no',
            'nah',
            'nope',
            'never',
            'n',
            'deny',
            'negative'
        ]}

def scrape_website(url: str) -> str:
    """
    Info:
        Returns the html of a website.

    Paramaters:
        url: str - The url to fetch and return the html of.

    Usage:
        scrape_website(url)

    Returns:
        str        
    """
    result = get(url)
    result_txt = result.text
    return result_txt

def get_mean(numbers: list) -> int:
    """
    Info:
        Gets the mean of a list of ints.

    Paramaters:
        numbers: list - The list of numbers to get the mean from.

    Usage:
        get_mean(numbers)

    Returns:
        int
    """
    return mean(numbers)

def get_median(numbers: list) -> int:
    """
    Info:
        Gets the median of a list of ints.

    Paramaters:
        numbers: list - The list of numbers to get the median from.

    Usage:
        get_median(numbers)

    Returns:
        int
    """
    return median(numbers)

class Database:
    """
    Info: 
        Cretes a simple database using JSON

    Options:
        add - Adds a key and value
        remove -  Removes a key and value
        fetch - Fetches a key and value
        reset - Resets the database
        update - Updates the database

    Usage:
        my_databse = Database()
        my_database.add(key, value)
    """
    
    def __init__(self, create_new_database: bool = True) -> None:
        """
        Info:
            Creates the database when called

        Paramaters:
            create_new_database: bool - Whether or not to rewrite the database.
        
        Usage:
            my_database = Database()
        
        Returns:
            None
        """
        self.database = {}
        
        if create_new_database:
            self.reset()

        self.load()
        
    def add(self, key: str, value: Union[str, int, list, dict, tuple]) -> None:
        """
        Info:
            Adds a key and value to the database

        Paramaters:
            key: str- the key of the item
            value: Union[str, int, list, dict, tuple] - The value of the key

        Usage:
            my_database.add(key, value)

        Returns:
            None
        """
        
        self.database[key] = value
        self.update()

    def remove(self, key: str) -> None:
        """
        Info:
            Removes a key and value from the database

        Paramaters:
            key: str- the key of the item
            value: Union[str, int, list, dict, tuple] - The value of the key

        Usage:
            my_database.remove(key, value)

        Returns:
            None
        """
        
        del database[key]
        self.update()

    def fetch(self, key: str) -> Union[str, int, list, dict, tuple, None]:
        """
        Info:
            Fetches the keys item and returns it

        Paramaters:
            key: str - The key to fetch and return

        Usage:
            my_database.fetch(key)

        Returns:
            Union[str, int, list, dict, tuple]
        """
        
        try:
            return self.database[key]
        except Exception:
            return None

    def reset(self) -> None:
        """
        Info:
            Resets the database

        Usage:
            my_database.reset()

        Returns:
            None
        """
        
        self.database = {}
        self.update()
    
    def update(self) -> None:
        """
        Info:
            Updates the database

        Usage:
            my_database.update()

        Returns:
            None
        """
        
        with open('database.json', 'w') as my_file:
            dump(self.database, my_file)

    def load(self) -> None:
        """
        Info:
            Loads the database

        Usage:
            my_database.load()

        Returns:
            None
        """
        
        with open('database.json', 'r') as my_file:
            self.database = json_load(my_file)

def hash_item(item: Union[str, bytes]) -> bytes:
    """
    Info:
        Hashes the given string and returns the hash in bytes

    Paramaters:
        item: Union[str, bytes] - The item to hash
    
    Usage:
        hash_item(item)

    Returns:
        bytes
    """
    
    return sha256(item.encode()).hexdigest()


def call_js_function(file: str, function: str, args: tuple = ()) -> Union[str, int, float, dict, list, tuple, Callable]:
    """
    Info:
        Calls a javascript function in a js file.
    
    Paramaters:
        file: str - The js file to use.
        function: str - The function to call.
        args: tuple - Arguments to pass to the function.
        requirements: list - Requirements that the js file needs to run.

    Usage:
        call_js_function(file, function, args=(arg1,))
  
    Returns:
       Union[str, int, float, dict, list, tuple, Callable]
    """
    
    eval_result, js_function = run_file(file)
    result = js_function[function](*args)
    
    return result

