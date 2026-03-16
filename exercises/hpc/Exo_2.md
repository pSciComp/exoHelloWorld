# HPC Exo 2: Minimal HPC Workflow


Now we have everything set up to transition from some interactive test-runs to asynchronous batch job submissions, enabling scalable execution on an HPC cluster.
With the setup at hand a strict separation between environment, configuration, code, and data is maintained when integrating the container environment, configuration data, and mapped storage paths.

The execution script, `scripts/say_hello.py`, imports functions from our `exohw` package and requires a configuration file path and an output directory.
It is designed to read these from the environment variables `CONFIG_PATH` and `OUTPUT_DIR` that default to your standard locations, `./config/` and `./data/final/` which we can bind to any location on the cluster upon runtime of the container.

1. **Track input data with git lfs**  
   
   In a project with a modest amount of data (this one is very modest) we can "attach" the data directly using `git lfs`.
   This approach comes with the advantage to decouple the data from the project allowing to "inject" it only at runtime.
   To do so we first want to track our data with `git lfs`.

   Add `data/raw/*.json` (or your input data) to git LFS tracking:
   ```bash
   git lfs install
   git lfs track "data/raw/*.json"
   git add .gitattributes data/raw/
   ```

2. **Update your container and redeploy it.**
   Either pull the pre-built container from the GitHub Container Registry:
   ```bash
   apptainer pull oras://ghcr.io/pscicomp/env-sif:latest
   ```
   Fetch it over the Swift object storage (if configured) or build it directly in the production environment.

3. **Write the submission script**  
   Complete the template below — fill in the gaps marked `___`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=helloworld
   #SBATCH --cpus-per-task=___
   #SBATCH --mem=___
   #SBATCH --time=___
   #SBATCH --output=logs/%j.out

   module load apptainer

   apptainer exec \
     --env-file .env \
     --bind ___:data/raw \
     --bind ___:data/final \
     env-sif_latest.sif \
     ___ scripts/say_hello.py
   ```

   
   **What can and what should be improved in this script?**

   **Where would you store this script?**

   _For both questions you can open an issue in your `exoHelloWorld` repository and ping either @j-i-l or @matteodelucchi.



4. (Optional) **Upload results to object storage**  
   After the job completes, push output data to object storage:
   ```bash
   # Using the s3cmdc (containerd s3cmd):
   ./s3cmdc put ... s3://...
   # Or using curl
   ```
