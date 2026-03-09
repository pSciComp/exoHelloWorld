# Struct E1: Separate concerns

In [/scripts/drafts/say_hello.py](../../scripts/drafts/say_hello.py) you find
a minimal working implementation of what it is we want to do.
However, this scripts has some issues we want to address here.

### Your Tasks

1. "Rubber-duck" through the script:
  - Add a docstring at the top explaining what this script does.
  - For each statement write in a comment above it:
    - What does this do?
    - Which ones of the 4 pillars (Environment, Configuration, Code, Data) are 
      concerned in this statement.
2. Separate data (SoC Pillar 4):  
   Move all that is input data into an appropriate location inside the project.  
   Remember that we aim for a genuine project structure, in particular we want
   to use these standard items:
  
   ```bash
   .env                  # environment variables
   config/               # hyperparams, model config
   src/                  # code: reusable functions/modules
   scripts/drafts/       # scripts in the making
   data/README.md        # document data stages
   ```
  
   _Note:_ "Tiny" input data, like in this case, we can simply commit it directly into the repository.  
  
   **Optional**: Track the input data with `git lfs`.


3. Separate configuration (Soc Pillar 2):  
   We do have some configuration data in this example. In particular, let's 
   consider the actual course name we want to use to filter people with as
   configuration data.
   
   In addition, note that actual key names of JSON data can also be
   considered configuration:
   If the `name` key of the input data should change to `fullname` at some
   point you should not need to change your code at all.

   **Hint**: Use python's `SimpleNamespace` to parametrise JSON keys, e.g.:
   ```
   >>> from types import SimpleNamespace
   >>> config_data = {'name': 'name', "age": "age"}
   >>> cfg = SimpleNamespace(**config_data)
   >>> cfg.name
   'name'
   ```
  
4. Separate environment variables (SoC Pillar 1):  
   In this simple example we import and export some data.
   The location of data is generally environment specific, so we might want to
   allow these locations to be set via environment variables.
 
   For our purpose we can define a `.env` file in the root of the project and 
   declare our variables in there.
   Environment variables can by definition be environment specific - you will
   know this much by know. This also means that tracking them directly in the
   repository is not a smart choice as this might lead to unexpected behaviour
   depending on the system you are running your project on.
   However, since we would like a user (i.e future us) to know what to put in
   the `.env` file we might provide an exemplary file along with the repository.
 
   In fact, it is common practice to add the `.env` file into your `.gitignore`
   and track a `.env.example` file in your repository.
 
   A `.env` file might look like this:
 
   ```bash
   # Set the output directory path (I'm a comment by the way)
   OUTPUT_DIR=./data/final
   ```
  
   > **NOTE**:  
   > Since we might track the input data directly in the project and, also,
     expect "tiny" output data files, we could get away with considering the input
     and output data paths as "internal" to the project and thus that they do not
     concern the environment in which the project runs.  
     However, this case is particular and in general we should always expect data
     to reside outside, or be exported from, the project context.
     So **data location definitions should always concern the Environment pillar!**

5. Now that we have moved away the environment variables, we still need to
   get the back into our script.
   This can happen in various ways. Traditionally, in python you could use the
   `dotenv` package and do `dotenv run -- python scritps/say_hello.py`.

   With `uv` you can specify an environment file to include:

   ```
   uv run --env-file .env scripts/ssay_hello.py
   ```
   Or set the environment variable (!) `UV_ENV_FILE` and uv will load the file
   on every run:

   ```bash
   export UV_ENV_FILE=".env"
   ur run scripts/say_hello.py
   ```

   Inside python environment variables can be accessed with the `os` module:

   ```python
   import os
   os.environ["OUTPU_DIR"]
   ```

6. Finally, move any reusable code out of the script (SoC Pillar 3).

   Arguably, in this script there is not much to move out, but by moving the
   input data into a JSON file and declaring the configuration in a JSON file
   we already have 2 occasion in which we convert JSON data into python object.
   For the sake of this example we define a `load_json_file` in our package,
   i.e. under `src/exohw/...` and import it in our script.

   _Note:_ You will have to "install" this project in your python Environment
   to be able to properly import the `load_json_file` function in your script.
   You can do this either with `uv`, simply by typing:
   ```bash
   uv sync
   ```
   in the root of your project, or using `pip`:
   ```
   pip install -e .
   ```
