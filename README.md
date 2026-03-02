# HPC Hello World

This is a "Hello World" application designed to demonstrate the best practices for running Python workflows on an HPC Slurm cluster.

## Exercises

### Exo 1: The HPC-Compatible Environment

We want to build a Python environment that uses the exact Python version and dependencies declared in our `pyproject.toml`.

While using `uv` (and `uv sync` in particular) locally would perform all the necessary steps in one go, deploying that standard virtual environment on an HPC cluster is not ideal for several reasons:

* **Metadata Hammering:** The generated `.venv` directory will contain thousands of individual files. Reading/writing these small files severely degrades the performance of HPC shared network filesystems (like CephFS or Lustre).
* **Portability Issues:** Within the `.venv` directory, various configurations and scripts use absolute paths, effectively breaking the virtual environment whenever the project folder is moved or renamed.
* **Strictly Limited to Python:** A standard virtual environment does not include any information on system-level packages (like C++ compilers or external libraries like GDAL). If the cluster is missing a system dependency, your code will fail.

Therefore, we are going to create a "containerized environment," relying on [Apptainer's "Integration First" philosophy](https://www.google.com/search?q=https://apptainer.org/docs/user/latest/introduction.html%23integration-over-isolation).

#### Your Tasks:

* [ ] Make sure the resulting binary container files (`*.sif`) are ignored and not accidentally tracked by Git (add them to your `.gitignore`).
* [ ] Create a `container/env.def` file in the repository.
* [ ] Declare a container recipe that sets up our environment properly (use `uv` inside the `%post` section of the container for this).
* [ ] Build the `env.sif` file locally on your machine and try it out with the [`apptainer shell`](https://www.google.com/search?q=%5Bhttps://apptainer.org/docs/user/latest/cli/apptainer_shell.html%5D(https://apptainer.org/docs/user/latest/cli/apptainer_shell.html)) command.
* [ ] Log in to the cluster, check out your repository, and try building the `env.sif` file directly on the cluster.
* [ ] "Enter" the created container environment on the cluster using `apptainer shell container/env.sif`. Once inside:
* Run `which python`. Which Python executable are you using now?
* Verify the `numpy` version specified in your `pyproject.toml` is indeed installed (e.g., run `python -c "import numpy; print(numpy.__version__)"`).


* [ ] Run the `scripts/drafts/say_hello.py` script interactively from inside the container shell.
* [ ] Exit the container (type `exit`), and try running the exact same script non-interactively from your host terminal using the `apptainer exec` command.

#### Hints & Best Practices:

* **Respect the Login Node:** Avoid running heavy builds or computational workloads on the login nodes. Grab an interactive session on a compute node first:
  ```bash
  srun --cpus-per-task=1 --mem=4G --time=00:20:00 --pty bash
  ```

* **Check your Environment:** The `which python` command is your best friend to verify whether you are using the host's default Python or the container's baked-in Python.
* **Manage Secrets:** Use the `--env-file .env` flag with your Apptainer commands to securely pass environment variables (like API keys or paths) from a local `.env` file into the context of the container.
* **Bypassing Cluster Build Errors:** If your `apptainer build` command crashes on the cluster with a `fakeroot` or similar error, try adding the `--ignore-fakeroot-command` flag.
  If that still fails, build the `.sif` on your laptop and `scp` it to the cluster!

### Exo 2: Automating with a Slurm Batch Script

Now that we have a working, HPC-compatible Apptainer environment, we need to transition from running interactive tests to submitting asynchronous "batch" jobs.
This is how actual research is done on an HPC cluster.

We have a script located at `scripts/drafts/say_hello.py`.
If you look at the source code, you will notice it requires two pieces of information to run: a configuration file path and an output directory.
It is designed to look for these in the environment variables (`CONFIG_PATH` and `OUTPUT_DIR`).

We need to write a Slurm submission script that sets up this environment, binds our project directory into the container, and executes the code.

#### Your Tasks:

* **Create the Configuration File:** Create a simple JSON file (e.g., `config.json` inside a `config/` directory) that contains `{"name": "Your Name"}`.
* **Create the `.env` File:** In the root of your project repository on the cluster, create a file named `.env`.
* Add the line `CONFIG_PATH=config/config.json`.
* Add the line `OUTPUT_DIR=results/`.


* **Create the Slurm Script:** Create a file named `submit_hello.sh` inside the `scripts/slurm/` directory.
* **Write the Slurm Directives:** At the top of `submit_hello.sh`, add your `#SBATCH` headers.
  Request 1 CPU, 4GB of memory, and 10 minutes of runtime.
  Make sure to define an output log file (e.g., `#SBATCH --output=results/hello_%j.log`).
* **Write the Execution Command:** In the Slurm script, write the `apptainer exec` command to run the Python script.
* You must use the `--env-file .env` flag to inject the variables so `hello.py` doesn't crash.
* You must use the `--bind "$(pwd):/app"` and `--pwd /app` flags.
  This ensures the container has permission to read your live `config.json` file and write to the `results/` folder on the host system.
* Call the script naturally: `python scripts/drafts/hello.py`.

* **Submit the Job:** From the root of your project, submit the script to the scheduler using:
  ```bash
  sbatch scripts/slurm/submit_hello.sh
  
  ```

* **Verify:** Use `squeue -u $USER` to check if your job is running.
  Once it finishes, check the `results/` folder to see if your output file and the Slurm `.log` file were successfully generated.

#### Hints & Best Practices:

* **Seamless Imports:** Because your `container.def` installed the project defined in your `pyproject.toml`, `mypkgs` is treated as a native Python package inside the container. You don't need any messy `PYTHONPATH` hacks or module flags; the container's Python environment already knows exactly where `mypkgs` is.
* **Directory Creation:** The `hello.py` script relies on a utility `prepare_output_dir` to make the `results/` folder if it doesn't exist. Because we bound `$(pwd)` to `/app`, the container utilizes your user's exact host permissions to create that folder safely on the cluster's shared filesystem.
