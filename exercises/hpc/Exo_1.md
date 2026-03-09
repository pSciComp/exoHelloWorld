# HPC E1: Container Deployment

Standard virtual environments present issues on HPC systems due to metadata hammering on shared network filesystems and strict path dependencies.
To resolve these portability and performance limitations, we deploy the Apptainer container defined in prior exercises directly on the cluster.

### Your Tasks

1. Repository Setup:
   Access the remote system via SSH and clone the project repository onto the cluster's filesystem.

   _Hint:_ Try to use [ssh agent forwarding](https://pscicomp.courses.t4d.ch/content/efficientClusterComputation/source/content/recapHPC/sshSecurity.html) so you do not need to deploy ssh-keys on the cluster.

2. Resource Allocation:
   Heavy computational workloads and container builds should be avoided on login nodes.
   Instead, allocate an interactive session on a compute node using Slurm:
   ```bash
   srun --cpus-per-task=1 --mem=4G --time=00:20:00 --pty bash
   ```
   Or with directly loading the apptainer module
   ```bash
   srun --cpus-per-task=1 --mem=4G --time=00:20:00 --pty bash -c "module load apptainer && bash"
   ```

3. Module Loading and Build:
   Load the Apptainer module into the compute node environment (e.g., `module load apptainer`).

   You can then build the container directly on the compute node:
   ```bash
   apptainer env.sif containers/env.def
   ```

   _NOTE:_  
   If user namespaces or `fakeroot` restrictions cause the build to fail on the cluster, you can try applying the `--ignore-fakeroot-command` flag.
   
4. Verification:
   Initiate an interactive shell within the container:
   ```bash
   apptainer shell env.sif
   ```
   Verify the Python executable path and installed dependencies to ensure the isolated environment is active.
   
   *Ask yourself: How do you verify that the dependencies specified in your `pyproject.toml` are indeed the ones installed inside the container?*
