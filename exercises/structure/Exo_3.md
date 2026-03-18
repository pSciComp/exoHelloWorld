# Struct E3: CI/CD Pipeline for Container Registry

Manual container builds present scalability and reproducibility challenges.
Since our container definition is now part of the repository and version-controlled, we can automate its creation. 

Continuous Integration/Continuous Deployment (CI/CD) pipelines can help us drastically here by automating the building of Apptainer containers and pushing the resulting binaries to a container registry for us to fetch whenever and wherever we need them.

## Your Tasks

1. Initialize the workflow:
   * Create a YAML workflow file in your project at `.github/workflows/buildApptainerContainer.yml`.

2. Configure the pipeline:
   * **Triggers:** You can configure the workflow to execute on specific events.
     For example, you might want to trigger it on pushes to the main branch or allow for manual dispatch.
   * **Checkout:** The repository code needs to be checked out into the runner environment.
     We recommend using standard GitHub checkout actions for this.
   * **Environment Setup:** You also need to install and configure the Apptainer binary on the runner system.
     You can utilize existing open-source actions to handle this setup for you.

3. Adapt your container build declaration (`containers/env.def`) to accept a `VERSION` variable that we can use the explicitly set the version of our `exohw` package.
   Recall that we are using the git version as SSOT for versioning and we fetch it during the installation (e.g. with `uv`) form the repository (i.e. the `.git` folder in the project).
   W

3. Build and authenticate:
   * Define a pipeline step to execute the `apptainer build` command, targeting your `containers/env.def` file.

   _NOTE_: Since we use version control authoritatively, i.e. we use the git version as package version for our `exohw` package, we can (and should!) also use the git version to create an unambiguous tag for the container we build. In doing so, we will always know exactly what version of our project we are using.
   Extracting the git tag and converting it into a form useable for Apptainer or Docker tags requires a few extra steps that are not really of importance for us.
   You can have a look at an exemplary implementation of this at the [pythonProject Template](https://github.com/j-i-l/pythonProject/blob/724c5b3078d60f0bf753ea8a620c691ba3cb2656/.github/workflows/buildApptainerContainer.yml#L25-L47)

4. Push to the registry:
   * Add a step to push the built `.sif` image to `ghcr.io/<repository-owner>/<repository-name>:<tag>`.

   * To push the container, you will need to authenticate with the GitHub Container Registry (GHCR).
     This can usually be established using the standard `GITHUB_TOKEN` provided by the runner context.

   * Once you commit and push your workflow file, you can verify its successful execution via your repository's Actions tab.
     You should then see the resulting package in your repository's registry.

5. Run apptainer directly with the remote container:  

   Once the container is pushed to the GitHub registry it can be retrieved directly when initiating the runtime.
   For this to work you must either authenticate to GitHub, or you can set the "package" holding the container to be publicly reachable.
   For this example repository, the settings can be found under:

   <https://github.com/orgs/pSciComp/packages/container/exohw-env/settings>

   Where `exohw-env` is the name of the container.

   Alternatively you can export the authentication credentials required to pull the image (`export APPTAINER_DOCKER_USERNAME=<github username>` and `export=APPTAINER_DOCKER_PASSWORD=<Personal access token (PAT)>`.

   Using the remote container is then as simple as:

   ```bash
   apptainer run oras://ghcr.io/pscicomp/exohw-env:1.0.0
   ```
