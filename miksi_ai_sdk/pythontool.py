import subprocess
import venv
import tempfile
import os


# Global variables
env_path = None
media_path = None
python_executable = None

def initialize_environment(env_path_param):
    global env_path, media_path, python_executable
    env_path = env_path_param
    ensure_virtual_environment()

def ensure_virtual_environment():
    """Create a virtual environment if it doesn't exist."""
    global python_executable
    if not os.path.exists(env_path):
        venv.create(env_path, with_pip=True)
        install_defaults()
    else:
        # Find the Python executable within the virtual environment
        python_executable = os.path.join(env_path, 'bin', 'python')

# install defaults
def install_defaults():
    defaults = ["matplotlib", "scikit-learn", "numpy", "statsmodels", "pandas", "scipy"]
    safe_install_modules(defaults)


def safe_install_modules(module_names):
    """
    Calls install_dependencies with a list of module names and handles any errors.
    
    :param module_names: A list of strings representing the names of the modules to install.
    """
    try:
        install_dependencies(module_names)
        print("Installation successful.")
    except Exception as e:
        print(f"An error occurred during installation: {e}")


def install_dependencies(dependencies):
    """Install additional dependencies in the virtual environment."""
    for dependency in dependencies:
        subprocess.call([python_executable, '-m', 'pip', 'install', dependency])

def execute_code(code):
    """Execute Python code within the virtual environment and return the output or error."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py', mode='w') as temp_script:
        # Write the code to a temporary file
        temp_script.write(code)
        temp_script_path = temp_script.name

    env_vars = os.environ.copy()

    command = [python_executable, temp_script_path]

    try:
        # Run the script and capture its output
        result = subprocess.run(command, env=env_vars, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If an error occurs, return the error message
        return f"An error occurred--: {e.stderr}"
    finally:
        # Clean up by deleting the temporary script
        os.remove(temp_script_path)


