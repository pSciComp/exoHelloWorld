# HPC Exo 3: Minimal HPC Workflow

1. **Create 3 greeting files for 3 different courses**  
   We want to run the HelloWorld pipeline once for each of three courses (e.g. `pSciComp`, `math99`, `linalg3`), producing a separate greeting file per course.

2. **Adapt the configuration**  
   The input data already contains people enrolled in multiple courses.
   We want to adapt our configuration to not target a single course, but keep
   a list of all courses we want to create greetings files for.

   We can adapt our `config.json` to contain:
   ```json
   "all_courses": [ "pSciComp", "math99", "linalg3" ],
   ```
   instead of just:
   ```json
   "course": "pSciComp"
   ```

   Now, we can set a environment variable, call it `COURSE_ID` that will, if it is defined,
   determine which element in out list of `all_courses` should be processed.
   Ideally, if the `COURSE_ID` is not set, then the routine should just fall back to processing all courses.

   Naturally, we also need to restructure our script and code somewhat, in order to make sure the `"all_courses"` configuration is processed correctly and we select the specific element, if `COURSE_ID` is provided.

   _We encourage you to try to make these modifications yourself, however, to make sure you can try out the actual parallelization step you can also simply checkout the branch that contains all the necessary modifications of the codebase already:_
   ```bash
   git checkout parallel_config
   ```

3. **Adapt the Slurm script for multi-node execution**  

   With this new design we can use the environment variable `COURSE_ID` to create a greeting file for only one specific course.
   This is convenient since now we can decide on runtime which course to create a greeting file for.

   In the context of a HPC Slurm cluster, this is more than just convenient:
   Slurm knows the principle of [job-arrays](https://slurm.schedmd.com/job_array.html), a feature that allows you to submit an array of jobs with a single `.sh` script.

   In fact, we can create a job array and use the individual job ids to select a particular course from our `all_courses` list, all we need to do is set our `COURSE_ID` to slurms job id and we are done.

   Create a `parallel_hello.sh` script with the template below and fill in the gaps marked `___`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=hello-parallel
   #SBATCH --array=0-___
   #SBATCH --cpus-per-task=1
   #SBATCH --mem=4G
   #SBATCH --time=00:10:00
   #SBATCH --output=logs/%A_%a.out

   module load apptainer

   apptainer run \
     --env ___=$SLURM_ARRAY_TASK_ID \
     --bind ./data/raw:___/raw \
     --bind ./data/final:___/final \
     exohw-env_2.0.0.sif \
     python scripts/say_hello.py
   ```

   _Note: you can get the container with the updated codebase with:_

   ```bash
   apptainer pull oras://ghcr.io/pscicomp/exohw-env:2.0.0
   ```

4. Have a look at the job outputs under `logs/`.

   - **Why are there multiple outputs for a single job ID?**  
     _You can write the answer in an issue in your `exoHelloWorld` repository and ping us (@j-i-l or @matteodelucchi)._
