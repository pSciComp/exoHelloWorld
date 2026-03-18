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
   apptainer pull oras://ghcr.io/pscicomp/exohw-env:1.0.0
   ```
   Fetch it over the Swift object storage (if configured) or build it directly in the production environment.

3. **Write the submission script**  
   Complete the template below — fill in the gaps marked `___`:

   ```bash
   #!/bin/bash
   #SBATCH --account=___
   #SBATCH --job-name=helloworld
   #SBATCH --cpus-per-task=___
   #SBATCH --mem=___
   #SBATCH --time=___
   #SBATCH --output=logs/%j.out

   module load apptainer

   apptainer ___ \
     --bind ./data/raw:___/raw \
     --bind ./data/final:___/final \
     exohw_env_1.0.0.sif \
     ___ scripts/say_hello.py

   ```

   **What can and what should be improved in this script?**

   **Where would you store this script?**

   _For both questions you can open an issue in your `exoHelloWorld` repository and ping either @j-i-l or @matteodelucchi._



4. (Optional) **Upload results to object storage**  
   After the job completes, push output data to object storage:
   ```bash
   # Using the s3cmdc (containerd s3cmd):
   ./s3cmdc put ... s3://...
   # Or using curl
   ```

> [!NOTE]
> Unfortunately, pushing data to the Object Storage is currently only supported from the Science Cluster login nodes.
> The network routing rules prevent the backwards traffic from reaching the compute nodes (i.e. you can push to the Object Storage but you never get a confirmation back, leading the `s3cmdc` command to hang).
> 
> This means that you will need to perform the following operations on the login nodes:
> - Fetch data from the Object Storage and store it on the clusters shared filesystem prior to using it.
> - Store result data to the shared filesystem on the cluster prior to storing in in Object Storage.
> 
> This also disables cloud native approaches in which you would fetch data directly inside your application, e.g. using [pandas `read_parquet`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_parquet.html) method.
