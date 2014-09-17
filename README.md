# simple simplex method solver for max or min optimization.


all you have to do is download the file simplex.py (by cloning this repo) and make the file executable.

## make it executable:

in linux this should be as simple as:

```sh
$ chmod u+x simplex.py
```

in windows, no frickin clue.

## run the program:

i built in an argument parser to deal with inputs in a decent way. I'm sure there are better ways to interface with the terminal, and if you have any siggestions I'd love to hear them.

run the help message to see what you're gettings yourself into:

```sh
$ ./simplex.py --help
```

which should display enough info for you to use the thing, but here's an example:

```sh
$ ./simplex.py 3 -1 -1 1 0 0 -6 -2 -1 0 1 0 -9 6 5 0 0 1 0 -m
```

in the above code, the first number (3) is the number of equations in the tableau. the following numbers make up the tableau. read the code if that's confusing. the optional argument -m or --min tells the program to find the minimum optimization instead of the max. 

any input/confusion/wtf's, just let me know!
