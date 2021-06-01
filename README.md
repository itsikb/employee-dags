
# airflow-template
This is a template project for creating [Apache Airflow Packaged DAGs](https://airflow.apache.org/docs/stable/concepts.html#packaged-dags). 
Developing with this project is somewhat different from developing a standard python project as your code will eventually need to be packaged as a zip file and uploaded to artifactory.
As such, if you stray from the template then the setup and deploy scripts will not be able to locate and/or properly package your project.

**Please carefully read the instructions below or don't and hope for a miracle ;-)**

## Template Usage
In order to use this template for building your own team project please follow the instructions bellow.

As long as this [JIRA-STORY](https://kenshoo.atlassian.net/browse/DEVOPS-6568) is not done yet **please use** the first guide: **ticket for microservices team**. Otherwise use the second guide: **create your own repo**. After that, continue to **README & CI\CD verification** part.
### First guide - Ticket for microservices team
Please open a new Jira ticket to `DevOps` with the following information:
* Project - DevOps
* Issue type - Support
* Summary - "Generate airflow repository" + repo name
* Components - Microcosm 
* Please add the new repository name in this format: `<project_name>-dags`
* Mention the Airflow Deployer Release that you would like its job to be automatically triggered (For general use cases use `airflow-deployer-release`)
* When your repo is ready, open a branch and run `./generate/generate.sh` from the project directory (this script will substitute and adapt some names to the name of the repo) and upload a new PR to the new repo

### Second guide - Create your own repo
In order to generate a new repository by this template automatically please follow the instructions 
#### Pre-installations
* If you don't have it already, you should install the microcosm-cli: [Install instructions here](https://github.com/kenshoo/microcosm-cli)
*  python 3.7 - verify that you have python 3.7 installed with the command `python3.7 --version`
    * if not install 3.7 with the following commands:
        * `sudo apt update`
        * `sudo add-apt-repository ppa:deadsnakes/ppa`
        * `sudo apt install python3.7`
        
#### Create your project LOCALLY

* Generate it by microcosm CLI's `micro generate-project` command and complete the following parameters
   * name: `<project_name>-dags`
   * stack: select the `airflow` option.
* cd into the project root folder and run `./generate/generate.sh` 
* Check your local environment works properly
   * create virtual environment
   * run `inv clean test`
   * If something is not working well follow this [airflow env setup guide](https://github.com/kenshoo/dev-best-practices/blob/master/docs/Airflow/airflow-guide.md#airflow-guide)


#### Publish your project

* Publish your project using `micro publish-project` (put the email of the related team).
  This will do the following:
    * a Github repo for the project will be created
    * a PR in [skipper](https://github.com/kenshoo/skipper) will be created for defining pull-request & release Jenkins jobs 
* Validate that the repository was created properly on Github 
* Go to [skipper-pulls](https://github.com/kenshoo/skipper/pulls) and look for your PR
   * Add `"downstream-job":"airflow-deployer-release"` for this pr changes and commit exactly as done [on this PR](https://github.com/kenshoo/skipper/pull/806). 
   * If the PR was already merged before your changes, you can add it in a separate PR as well.
   * Make sure it is merged and PULL+RELEASE jobs are added to jenkins 

### README & CI\CD verification - relevant for all
Once your repo is ready on GitHub:
* Add the repo name to [requirements-dags.txt file](https://github.com/kenshoo/airflow-deployer/blob/master/requirements-dags.txt) on airflow-deployer (or the other deployer repo that you'd like to deploy to)
* Copy readme from [flakesloader-dags](https://github.com/kenshoo/flakesloader-dags) and adapt it on your own repo.
* It will require pull request reviews before merging
* It might take some time to generate the first PR build (check job is triggered)
* Verify related job release + related deployer (e.g: airflow-deployer) are triggered and green

# Additional Information
## Kenshoo's Airflow Guide & Best Practices
For Setting up Airflow Development Environment, Working with Airflow Environment, Best Practices and much more - please read [Kenshoo's Airflow Guide](https://github.com/kenshoo/dev-best-practices/blob/master/docs/Airflow/airflow-guide.md#airflow-guide)
