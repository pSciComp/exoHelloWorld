# HPC E1: Container Deployment

Following the construction of the container image, the artifact must be transferred to the production environment. Three distinct methods for deployment are outlined below for evaluation.

### 1. Retrieval via Container Registry

If a Continuous Integration/Continuous Deployment (CI/CD) pipeline is established, build artifacts may be sourced directly from the repository registry. Alternatively, the container from the [exoHelloWorld](https://github.com/pSciComp/exoHelloWorld/) project may be utilized.

**Tasks:**

* Identify the Uniform Resource Identifier (URI) for the target container.
* Access the production environment (e.g., HPC cluster) and retrieve the image using the `apptainer pull` command.
* Note that the `oras://` protocol may be required. If the registry is private, authentication credentials must be supplied. Refer to the [Apptainer documentation](https://apptainer.org/docs/user/main/registry.html#the-authfile-flag) regarding the `--authfile` flag.

### 2. Distribution via Object Storage

Object storage provides a cost-effective solution for distributing immutable data, such as `.sif` files. While some HPC environments lack native S3-compatible clients, Apptainer can execute tools to facilitate transfer. The [s3cmdc](https://github.com/pSciComp/s3cmdContainer) project—a containerized wrapper for `s3cmd`—serves as a reference implementation.

**Tasks:**

* Upload the locally built `.sif` binary to an S3-compatible object store.
* Configure access credentials within the production environment.
* Download the container binary from the object store to the cluster filesystem.

### 3. In-Situ Build on Production Infrastructure

While this method does not involve moving a pre-built binary, the image is generated directly on the target system. This approach requires adherence to two principles:

* **Reproducibility**: The container definition must ensure that the resulting image is independent of the host environment's specific configuration.
* **Resource Management**: Container orchestration and image building are computationally intensive. These operations must be treated as batch workloads.

**Tasks:**

* **Repository Setup**: Use SSH to access the remote system and clone the repository. Utilize [SSH agent forwarding](https://pscicomp.courses.t4d.ch/content/efficientClusterComputation/source/content/recapHPC/sshSecurity.html) to avoid storing private keys on the cluster.
* **Resource Allocation**: Container builds must not be executed on login nodes. An interactive session on a compute node must be requested via the Slurm workload manager:
```bash
srun --cpus-per-task=1 --mem=4G --time=00:20:00 --pty bash

```


Alternatively, the environment can be initialized with the Apptainer module:
```bash
srun --cpus-per-task=1 --mem=4G --time=00:20:00 --pty bash -c "module load apptainer && bash"

```


* **Image Generation**: Once allocated to a compute node, load the required module and execute the build:
```bash
module load apptainer
apptainer build env.sif containers/env.def

```


*Note: If restricted user namespaces or `fakeroot` limitations prevent a successful build, the `--ignore-fakeroot-command` flag may be applied.*
* **Verification**: Validate the environment by spawning a shell within the container:
```bash
apptainer shell env.sif

```


Verify the path of the Python executable and the presence of required dependencies.
*Analytical Exercise: Determine the methodology required to confirm that the specific dependency versions defined in `pyproject.toml` match the binaries installed within the immutable container image.*

