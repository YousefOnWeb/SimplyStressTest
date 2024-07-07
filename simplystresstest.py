import subprocess
import argparse
from blessed import Terminal
from datetime import datetime

# Initialize blessed terminal
term = Terminal()

def compile_cpp(file_path, output_path):
    """Compiles a C++ file."""
    subprocess.run(["g++", file_path, "-o", output_path], check=True)
    print(f"Compiled {file_path} to {output_path}")

def run_executable(executable_path, input_data):
    """Runs the executable with the provided input and returns the output."""
    process = subprocess.Popen(executable_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=input_data.encode())
    return stdout.decode(), stderr.decode()

def print_box(term, text, halted=False):
    with term.location(x=0, y=0):
        print(term.clear_eos())  # Clear from cursor to end of screen
        lines = text.splitlines()
        max_length = max(len(line) for line in lines)
        
        top_bottom_border = '+'+'-' * (max_length + 1) + '+'
        print(term.white_on_black(top_bottom_border))
        first_line = lines[0]
        print(term.white_on_black(f'{first_line.center(max_length)}'))
        for line in lines[1:]:
            print(term.white_on_black(f'{line.ljust(max_length)}'))
        print(term.white_on_black(top_bottom_border))
        
        result=""
        result+='+'+'-' * (max_length + 1) + '+'+"\n"
        result+=f'{first_line.center(max_length)}'
        result+="\n"+'\n'.join(lines[1:])+"\n"
        result+='+'+'-' * (max_length + 1) + '+'
        
        if halted:
            # Print exit message below the box
            exit_message = "Press Enter to exit..."
            print(term.move_y(term.height - 3) + exit_message,end="")
            input()
            
        return result

def main():
    parser = argparse.ArgumentParser(description="Stress test C++ solutions")
    parser.add_argument("--code_correct", required=True, help="Path to the correct C++ solution")
    parser.add_argument("--code_to_test", required=True, help="Path to the C++ solution to test")
    parser.add_argument("--code_generator", required=True, help="Path to the C++ test case generator")

    args = parser.parse_args()

    correct_exe = "./correct_solution"
    test_exe = "./test_solution"
    generator_exe = "./test_generator"
    
    now = datetime.now()

    compile_cpp(args.code_correct, correct_exe)
    compile_cpp(args.code_to_test, test_exe)
    compile_cpp(args.code_generator, generator_exe)

    iteration = 0
    result=""
    with term.fullscreen():
        while True:
            iteration += 1
            multiline_text = f"Iteration {iteration}\n"
            print_box(term, multiline_text)

            test_input, _ = run_executable(generator_exe, "")
            multiline_text += f"Generated test case:\n{test_input}\n"
            print_box(term, multiline_text)

            correct_output, _ = run_executable(correct_exe, test_input)
            test_output, _ = run_executable(test_exe, test_input)

            if correct_output != test_output:
                multiline_text += "Outputs differ!\n\n"
                multiline_text += f"Correct output:\n{correct_output}\n"
                multiline_text += f"Tested code's output:\n{test_output}\n"
                result=print_box(term, multiline_text, halted=True)
                #input("Press any key to exit...")
                break
            else:
                multiline_text += "Outputs match."
                print_box(term, multiline_text)
    print(result)
    print("Time of test:",now.strftime("%Y-%m-%d %H:%M:%S"))

if __name__ == "__main__":
    main()
