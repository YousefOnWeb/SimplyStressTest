import subprocess
import argparse
import os


# Function to clear the terminal screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to print a box with text inside
def print_box(text, border_color='\033[0m', reset_color='\033[0m'):
    clear_screen()
    lines = text.splitlines()
    max_length = max(len(line) for line in lines)
    
    top_bottom_border = f'{border_color}+' + '-' * (max_length + 2) + '+'+f'{reset_color}'
    print(top_bottom_border)
    first_line = lines[0]
    print(f'{border_color}| {first_line.center(max_length)} |{reset_color}')
    for line in lines[1:]:
        print(f'{border_color}| {line.ljust(max_length)} |{reset_color}')
    print(top_bottom_border)

def compile_cpp(file_path, output_path):
    """Compiles a C++ file."""
    print(f"Compiling {file_path}...")
    subprocess.run(["g++", file_path, "-o", output_path], check=True)
    print(f"Compiled {file_path} to {output_path}")

def run_executable(executable_path, input_data):
    """Runs the executable with the provided input and returns the output."""
    process = subprocess.Popen(executable_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate(input=input_data.encode())
    return stdout.decode(), stderr.decode()

def main():
    parser = argparse.ArgumentParser(description="Stress test C++ solutions")
    parser.add_argument("--code_correct", required=True, help="Path to the correct C++ solution")
    parser.add_argument("--code_to_test", required=True, help="Path to the C++ solution to test")
    parser.add_argument("--code_generator", required=True, help="Path to the C++ test case generator")

    args = parser.parse_args()

    correct_exe = "./correct_solution"
    test_exe = "./test_solution"
    generator_exe = "./test_generator"

    compile_cpp(args.code_correct, correct_exe)
    compile_cpp(args.code_to_test, test_exe)
    compile_cpp(args.code_generator, generator_exe)

    iteration = 0
    while True:
        # Example multiline string
        multiline_text =""
        
        iteration += 1
        multiline_text += f"Iteration {iteration}"
        print_box(multiline_text)
        
        test_input, _ = run_executable(generator_exe, "")
        multiline_text += "\n" + f"Generated test case:\n{test_input}"
        print_box(multiline_text)

        correct_output, _ = run_executable(correct_exe, test_input)
        
        test_output, _ = run_executable(test_exe, test_input)

        if correct_output != test_output:
            multiline_text += "\n" + "Outputs differ!\n"
            multiline_text += "\n" + "Correct output:\n"+ str(correct_output)
            multiline_text += "\n" + "Test output:\n"+ str(test_output)
            print_box(multiline_text)
            break
        else:
            multiline_text += "\n" + "Outputs match."
            print_box(multiline_text)

if __name__ == "__main__":
    main()
