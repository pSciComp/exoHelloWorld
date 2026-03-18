# HPC E1: Container Deployment

Following the construction of the container image, the artifact must be transferred to the production environment. Three distinct methods for deployment are outlined below for evaluation.

### 1. Retrieval via Container Registry

If a Continuous Integration/Continuous Deployment (CI/CD) pipeline is established, build artifacts may be sourced directly from the repository registry. Alternatively, the container from the [exoHelloWorld](https://github.com/pSciComp/exoHelloWorld/) project may be utilized.

**Tasks:**

* Identify the Uniform Resource Identifier (URI) for the target container.
* Access the production environment (e.g., HPC cluster) and retrieve the image using the `apptainer pull` command.
* Note that the `oras://` protocol may be required. If the registry is private, authentication credentials must be supplied. Refer to the [Apptainer documentation](https://apptainer.org/docs/user/main/registry.html#the-authfile-flag) regarding the `--authfile` flag.

### 2. Distribution via Object Storage

Object storage provides a cost-effective solution for distributing immutable data, such as `.sif` files.
Furthermore, it can act as alternative storage option to the shared filesystem of a HPC cluster.

While some HPC environments lack native S3-compatible clients, Apptainer can be used to provide containerized versions of such clients, enabling the usage of Object Storage.

The [s3cmdc](https://github.com/pSciComp/s3cmdContainer) project — a containerized wrapper for `s3cmd` — can server as such a tool.

Setting `s3cmdc` up on the Science Cluster basically boils down to:

- Fetching the container image:
  ```bash
  apptainer pull s3cmdc oras://ghcr.io/pscicomp/s3cmdc:1.0.1
  ```
- Making it executable (optional)
  ```bash
  chmod +x s3cmdc
  mv s3cmdc ~/.local/bin/
  ```
  _If you skip this step, you need to run `apptainer run s3cmdc ...` to use the `s3cmdc` container._

In order to use `s3cmd` (or the containerized version provided in this course) a valid configuration file is needed.  
Usually, `s3cmdc` would take care of generating this file, if it does not exist. The only thing you would need to do is to provide the necessary access credentials to the Science Cloud API.  
Unfortunately, on the Science Cluster we need to add this configuration file manually:

> [!WARNING]
> From the Science Cluster access to the Science Cloud API is blocked (or not configured properly) by internal network rules, making it impossible to use the `openstack` cli directly on the cluster.
> Luckily, access to the Science Cloud Object Storage is still possible.
> 
> This means that we cannot simply let the `s3cmdc` container take care of fetching the access information necessary to communicate with the Object Storage:
> We need to manually provide a valid `.s3cfg-apptainer` file for the `s3cmdc` command to work from the Science Cluster.  
> To do so have 2 options. In both cases you need a machine that can reach the Science Cloud (i.e. must be in the internal network or connected via VPN):
>
> **Option 1: Manually create the config file**:  
> The `.s3cfg-apptainer` file must look like this:
> ```ini
> [default]
> host_base = <the S3_HOST url>
> host_bucket = %(host_base)s
> access_key = <the ACCCESS_KEY>
> secret_key = <the SECRET_KEY>
> use_https = True
> ```
> To get the necessary information (i.e. the URL and the KEY):
> - Install the `openstack` cli tool.
> - Source the OpenStack RC file retrieved from the Science Cloud:
>   ```bash
>   source <projectRC.sh>
>   ```
> - Fetch the `S3_HOST` url with:
>   ```bash
>   S3_HOST=$(openstack catalog show swift -f json -c endpoints | \
>             jq --raw-output '.endpoints[] | select(.interface | contains("public")) | .url' | \
>             head -n 1 | sed 's|https://||' | cut -d'/' -f1)
>   ```
> - Fetch the `ACCESS_KEY` with:
>   ```bash
>   ACCESS_KEY=$(openstack ec2 credentials create -f value -c access)
>   ```
> - Fetch the `SECRET_KEY` with:
>   ```bash
>   SECRET_KEY=$(openstack ec2 credentials show "${ACCESS_KEY}" -f value -c secret)
>   ```
> - Complete the `.s3cfg-apptainer` file with the retrieved values and copy it to your home folder on the Science Cluster.
>
> **Option 2: Automatically generate the file:**  
> We can use the `s3cmdc` command to generate the `.s3cfg-apptainer` file for us:
> - Make sure apptainer is installed.
> - Fetch the `s3cmdc` container:
>   ```bash
>   apptainer pull s3cmdc oras://ghcr.io/pscicomp/s3cmdc:1.0.1
>   ```
> - Source the OpenStack RC file retrieved from the Science Cloud:
>   ```bash
>   source <projectRC.sh>
>   ```
> - Run a simple `ls` to trigger the config file genertion:
>   ```bash
>   apptainer run s3cmdc ls
>   ```
> - Copy the newly generated `~/.s3cfg-apptainer` file to your home folder on the Science Cluster.


**Tasks:**

* Upload the locally built `.sif` binary to an S3-compatible object store.
* Configure access credentials within the production environment, aka make sure you have a valid `.s3cfg-apptainer` file in your home folder on the cluster.
* Download the container binary from the object store to the cluster shared filesystem.

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
