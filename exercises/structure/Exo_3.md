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

3. Build and authenticate:
   * Define a pipeline step to execute the `apptainer build` command, targeting your `containers/say_hello.def` file.

   _NOTE_: Since we use version control authoritatively, i.e. we use the git version as package version for our `exohw` package, we can (and should!) also use the git version to create an unambiguous tag for the container we build. In doing so, we will always know exactly what version of our project we are using.
   Extracting the git tag and converting it into a form useable for Apptainer or Docker tags requires a few extra steps that are not really of importance for us.
   You can have a look at an exemplary implementation of this at the [pythonProject Template](https://github.com/j-i-l/pythonProject/blob/724c5b3078d60f0bf753ea8a620c691ba3cb2656/.github/workflows/buildApptainerContainer.yml#L25-L47)

   * To push the container, you will need to authenticate with the GitHub Container Registry (GHCR).
     This can usually be established using the standard `GITHUB_TOKEN` provided by the runner context.

4. Push to the registry:
   * Add a step to push the built `.sif` image to `ghcr.io/<repository-owner>/<repository-name>:<tag>`.
   * Once you commit and push your workflow file, you can verify its successful execution via your repository's Actions tab.
     You should then see the resulting package in your repository's registry.

