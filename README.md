# SimplyStressTest

A very simple CLI program used to stress-test a problem solution against another solution given a test generator that generates a single test.

The script:

- Only supports C++
- Assumes you have a C++ compiler installed locally that you can use from your terminal (to make sure, run ```g++ --version```.)
- Assumes your generator outputs the generated test to standard output when run

### Usage

Locations to the three necessary files are passed to the program as parameters.

Example (powershell):

```powershell
python3 .\simplystresstest.py --code_correct ".\correctCode.cpp" --code_to_test ".\tobetested.cpp" --code_generator ".\generator.cpp"
```

In this example, the program script, and the three files, all exist at the same directory from which the command is run.

Also, the names of the files in the example are:

```correctCode.cpp``` , ```tobetested.cpp```, and ```generator.cpp```.

They can be anything.

If you ever forget the exact names of the three parameteres which are necessary to use the script, you can see them in the command help by running this (from the same directory as the script):

```powershell
python3 .\simplystresstest.py --help
```

How the result of the stress-test looks like in the terminal:

```
+----------------------+
     Iteration 38
Generated test case:
1
2
158

Outputs differ!

Correct output:
15

Tested code's output:
158

+----------------------+
```

Enough documentation for such an atomic script (jk)
