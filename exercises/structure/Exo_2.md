# Struct E2: Build a container

Now that we have a well structured mini project it is time to create an appropriate environment for it.

> [!NOTE]
> In case you want to make sure to start this exercise with a good state of the project you can checkout the `stuct_exo_1` branch and start from there.

Container are a form of isolated environment we can design and use to run a codebase.
Their definition can - and in many cases should - be part of the project itself.

In therm of Separation of Concerns (SoC), a container definition is the definition of an environment and thus should neither reside in `scripts/`, nor in `src/` or `config/`.

_Ask yourself why not in `config/`?_

What complicates things slightly is that a container defines an environment that, in turn will also have to be run inside some other environment.
In fact, a container gives us full control over the python runtime environment and we can define it completely to our liking.
This has some drastic consequences, typically on input and output data paths:

> [!NOTE]
> Inside a container we can always rely on our genuine project structure and set, for example, the `OUTPUT_DIR` for some final results data to `data/final/` by default.
> Whenever we then run that container we bind a specific location form the container runtime environment to this path, e.g., `--bind /scratch/<username>/<myproject>/results:data/final`.
> So whenever our python routine inside the container then writes to the default location, i.e. `./data/final`, we get the output data written to `/scratch/<username>/<myproject>/results`.

To keep a clear separation of runtime environment variables and environment declarations we move all container definitions into the `containers/` folder and we track them in our project.
 
_Ask yourself why is it OK to track container definitions but not `.env`?_

To get started with declaring apptainer containers we recommend you have a look at the [official documentation](https://apptainer.org/docs/user/latest/), alternatively you can also checkout the existing container definition in [T4D's pythonProject Template](https://github.com/j-i-l/pythonProject).

## Your Tasks

1. Create the `containers/` folder and start with an new `.def` file in it: `containers/say_hello.def`.
2. Start with the container specification:
   * The container definition must specify a base image (e.g., `python:3.13-slim`).
   * The `%files` section is utilized to copy `pyproject.toml` and other required project files into the container.  
     _NOTE 1:_ We recommend you always follow the principle that any container build, or script execution **always** happens from the root folder of your project.
     Therefore, the path to the files you cant to make available inside the container should also be relative to this location.

     _NOTE 2:_ Inside the container it is standard practice to use the location `/app` to place any file or directories. You do not need to call it `/app`, you could call it `/project` or anything else (though avoid names the you would see when you run `ls -ahl /` on a linux system as some of these locations will be [bound by apptainer to system folder](https://apptainer.org/docs/user/main/bind_paths_and_mounts.html#system-defined-bind-paths)).
     Placing `pyproject.toml` there would look as follows:
     ```docker
     %files 
         pyproject.toml /app/
     ```
   * The `%post` section can be used to install system dependencies and perform configurations.
     Installing `uv`, and synchronizing the Python environment using the project specifications is typically done here.
   * The `%environment` section allows to export environment variables on runtime of the container.
     It should be used to set the path to where you've installed the virtual environment in the `%post` section, for example (e.g., `export PATH="/opt/venv/bin:$PATH"`).
3. Build and run your container locally:  
   * You can build locally using the Apptainer CLI: `apptainer build say_hello.sif containers/say_hello.def`.
     
     _NOTE:_ The `.sif` binary should be excluded from version control via `.gitignore`. It is a result from your `.def` container declaration and tracking the `.def` file inside your git repository is all that is needed.
     However, being able to easily obtain a built container (i.e. the `.sif` file) can make your life much easier - an issue we will tackle in the next exercise.
   * Run the `src/say_hello.py` script locally through the built container.
     You can use the `--env-file .env` parameter so to inject environment variables securely.
     
     _Ask yourself what locations (i.e. folders) from your machine you need to bind to the container for this script to run smoothly?_

4. Refactor your codebase to use the genuine locations for input and output data, i.e. `data/...`.

   _How does this affect what environment variable you need to pass to the container?_


> [!NOTE]
> Note down in an issue in your repository the things that are unclear or confusing to you.
> We are going to discuss this exercise in plenum in the next session.

**Bonus**:
Since our container definition is now part of the repository and verion-controlled like the rest, we can go ahead and build version specific container for our project.

But manually building a new container for each version and copying it around wherever we need it, is a strategy that is bound to fail.

Luckily CI/CD pipelines, a feature that is widely available on Git remote Services, can help us drastically here:

In fact, we can setup a CI/CD pipeline to build our Apptainer containers for us store them in a www-reachable container registry for us to fetch whenever and wherever we need them.

If you are completely new to CI/CD pipelines, we recommend having a look at [T4D's Course on CI/CD Workflows](ttps://t4d-gmbh.github.io/using-git-in-academia/content/ci-cd-workflows/source/content/index.html).
Alternatively, you can ask your favorite LLM for help, and it will get you going in no time!

You can also get inspiration from the CI/CD workflow script that builds and stores an Apptainer container in GitHubs registry [in the pythonProject Template](https://github.com/j-i-l/pythonProject/blob/main/.github/workflows/buildApptainerEnv.yml).
