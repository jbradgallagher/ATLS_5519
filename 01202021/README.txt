House of Dust Ideas:

Building from the example in permPoem.py, add command line processing to
"House Of Dust." The idea would be to allow the program to toggle between 
the two output modes we defined functions for in class: 

"printPoem" and "printPoemByLetter"

When it is ran without arguments: "python3 HouseOfDust.py," it should print
out a single instance all at once.

When it is ran like the following: "python3 HouseOfDust.py -t 20," it should
print out an instance one letter at a time at 1/20th of a second.

Another idea could be to add a "situations" list and change the "buildPoem" function
to randomly choose between "situations" and "places"

Finally, try playing with the duration and format of the output. How does it function if it
runs indefinitely? How does it function if you don't use line breaks or randomize the numbers
passed to the "makeSomeSpace" function? In general what are some creative ways you can
play with the format of the ouput?

Permutation Poem Ideas:

Experiment with the format of the output. You could take the makeSomeSpace function
from "House of Dust" and play around with randomly spacing each word in a permutation.
Can you think of a creative way to print a single permutation on multiple lines?

Using "global" variables in python is generally discouraged. Can you figure out a way to get
rid of the global "frequency" variable that is used in the "printPermutations" function?
