# HPC Exo 3: Minimal HPC Workflow

---

_⏳ This exercise will be ready by March 20, 2026 ⏳_

---

1. **Create 3 greeting files for 3 different courses**  
   We want to run the HelloWorld pipeline once for each of three courses (e.g. `pSciComp`, `math1`, `linalg3`), producing a separate greeting file per course.

2. **Adapt the configuration**  
   The input data already contains people enrolled in multiple courses. We need a config that selects which course to greet for.

   _Checkout the branch that contains this already:_
   ```bash
   git checkout parallel_config
   ```

3. **Introduce an environment variable to select the course**  
   Instead of hardcoding the course name, the script should read it from an environment variable (e.g. `COURSE_NAME`).

   _Checkout the branch that contains this already:_
   ```bash
   git checkout parallel_env
   ```

4. **Adapt the Slurm script for multi-node execution**  
   Write (or adapt) the `.sh` submission script so that it uses **multiple nodes** (or array jobs), setting the `COURSE_NAME` environment variable appropriately for each.

   A Slurm job array is a clean way to do this:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=hello-parallel
   #SBATCH --array=0-2
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=4G
   #SBATCH --time=00:10:00
   #SBATCH --output=logs/%A_%a.out

   module load apptainer

   apptainer run \
     --env COURSE_ID=$SLURM_ARRAY_TASK_ID \
     --bind ./data/raw:/app/data/raw \
     --bind ./data/final:/app/data/final \
     exohw-env_1.1.0.sif \
     python scripts/say_hello.py
   ```

5. **Invite us to your repository**  
   Add [@matteodelucchi](https://github.com/matteodelucchi) and [@j-i-l](https://github.com/j-i-l) as collaborators so we can see that you at least tried :-)
:::
   
   :::{admonition}
   :class: warning
   Invite [@mattedoleducchi](https://github.com/matteodelucchi) and/or [@j-i-l](https://github.com/j-i-l) to your exercise projects!

   You can ping us in an issue, if you have any questions!
   :::

