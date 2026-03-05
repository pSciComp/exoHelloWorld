# Struct E1: Rubber ducking

In [/scripts/drafts/say_hello.py](../../scripts/drafts/say_hello.py) you find
a minimal working implementation of what it is we want to do.
However, this scripts has some issues we want to address here.

### Your Tasks
- "Rubber-duck" through the script:
  - Add a docstring at the top explaining what this script does.
  - For each statement write in a comment above it:
    - What does this do?
    - Which ones of the 4 pillars (Environment, Configuration, Code, Data) are 
      concerned in this statement.
- Separate data (SoC Pillar 4):
  Move all that is input data into an appropriate location inside the project.  
  _Note:_ "Tiny" input data, like in this case, we can simply commit it directly into the repository.  
  **Bonus**: Track the input data with `git lfs`.
- Separate configuration (Soc Pillar 2):
  ...
  
- Separate environment variables (SoC Pillar 1):
  ...
  
> [!NOTE]
> Since we might track the input data directly in the project and, also,
  expect "tiny" output data files, we could get away with considering the input
  and output data paths as "internal" to the project and thus that they do not
  concern the environment in which the project runs.  
  However, this case is particular and in general we should always expect data
  to reside outside, or be exported from, the project context.
  So **data location definitions should always concern the Environment pillar!**
  
