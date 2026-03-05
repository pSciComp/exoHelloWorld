# Hello World Exercise

This is a "Hello World" project written in Python with the aim to help implementing some project structure and coding practices.

The actual task that is performed in this project is minimal:

We want to produce a text file (i.e. some result) that contains a simple greetings
for all people from a list of people (i.e. input data) if they are enrolled into
some course (i.e. configuration data).

Quick and dirty, all we want to do is this:

```python
people = [
  {"name": "Jon Doe", "courses": ["math1", "pSciComp", "physics1"]},
  {"name": "Leonardo Da Vinci", "courses": ["math99", "cosmology7"]},
  {"name": "Mona Lisa", "courses": ["linalg3", "pSciComp"]},
]
course = 'pSciComp'
greetings = []
for person in people:
    if course in person['courses']:
        greetings.append(f"Hello {person['name']}\n")
with open('data/final/greeting.txt', 'w') as f:
    f.writelines(greetings)
```

It might not be a surprise to you that such a script, while it works, is far from following any coding practices or adhering to some organisational patterns that would classify it as "documented", "reusable" or ...

Implementing principles like the [Separation of Concerns (SoC)](#TODO) for such a minimal task introduce overhead that is more substantial than the actual codebase itsel.
However, this overhead is largely static, i.e. it won't scale with the codebase of a project.
Implementing a rigorous SoC in a toy project like this one allows to easily identify how a strict separation between environment, configuration, code and data looks like.

## Usage

This project contains various exercises defined under [./exercises](./exercises).
To get started head over to [Exercise 0](./exercises/Exo_0.md) that will guide you through the initial setup.

Further exercises are categorised into:

**Structure**  
Exercises specific to project structure and coding practices.

**HPC**  
Exercises that focus on the usage of a HPC cluster (e.g. Slurm).

## Exercises

### Structure
- [**Exercise 1**](./exercises/structure/Exo_1.md): Rubber ducking.

### HPC
- [**Exercise 1**](./exercises/hpc/Exo_1.md): Build a runtime environment with apptainer.
- [**Exercise 2**](./exercises/hpc/Exo_2.md): 

