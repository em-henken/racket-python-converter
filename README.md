# Racket to Python converter

## Parsing Racket
My parser recognizes a subset of the racket built-ins. No need to explain because we all know racket now! :) the subset I handled is listed here:
- math expressions (+, -, *, /)
- boolean expressions (<, >, <=, >=, null?, eq?)
- list
- car and cdr
- cond (each conditon always returned something)
- if statements (checked if data was 'returnable' or not, i.e. another if statement)
- define
- lambda

## Interesting things
I have my parser save functins defined by (define ...)
These are saved into a dictionary. the structure of the dictinary is:
{name of function: [definition name and parameters, definition body]}
the parser will recognize if a var is a function by seeing if the data is in the dictionary. Then it will call it as a function and not just a random variable.

my translate() function handles python indentation. it takes a parameter to maintain each line at a proper indentation level depending where in the tree it is.

if you want to run python code, you may need the library.py file, which provides definitions for car cdr and cond.

## How to run
1. run "python3 racket2python.py" in command line.
2. you will be promted to enter a racket program. Copy and paste one of the sample programs.
3. python code will print out in the command line
4. take python code and run elsewhere 
