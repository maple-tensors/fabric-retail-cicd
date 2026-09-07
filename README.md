# Microsoft Fabric Retail Sales CI/CD Project

## Overview

This project demonstrates an end-to-end CI/CD workflow for a small Microsoft Fabric data engineering solution.

The main goal is not complex data architecture. The goal is to show how a Fabric data pipeline can be developed using feature branches, validated through pull requests and GitHub Actions, deployed through Dev/Test/Prod environments, and promoted to Production only after automated Test validation succeeds.

## Objective

Build a retail sales pipeline using Microsoft Fabric while practicing:

- Git source control
- Feature branches
- Pull requests
- Automated CI validation
- Dev / Test / Prod environments
- Fabric Deployment Pipelines
- Automated deployment and post-deployment validation

## Architecture

```text
CSV files
   ↓
Microsoft Fabric Data Pipeline
   ↓
Lakehouse Bronze
   ↓
PySpark transformation notebook
   ↓
Silver Delta table
   ↓
Gold KPI table

Fabric artifacts:

- lh_retail
- nb_transform_sales
- nb_validate_release
- pl_daily_sales

The transformation produces:

- silver_sales
- gold_daily_sales

The Silver layer includes calculated metrics such as:

- gross amount
- discount amount
- net revenue
- estimated cost
- profit amount
- profit margin

## Environments

- Retail-CICD-Dev
- Retail-CICD-Test
- Retail-CICD-Prod

GitHub main
    ↓
Retail-CICD-Dev
    ↓
Fabric Deployment Pipeline
    ↓
Retail-CICD-Test
    ↓
Fabric Deployment Pipeline
    ↓
Retail-CICD-Prod

Test and Production are intentionally not connected directly to Git.
This keeps GitHub as the source of truth while Fabric Deployment Pipelines control environment promotion.

## Branch Strategy

Development uses short-lived feature branches.

main
  ↓
feature/add-profit-margin
  ↓
Pull Request
  ↓
CI validation
  ↓
Merge to main

Fabric notebook development follows the same model:

Fabric Dev connected to feature branch
        ↓
develop and test notebook
        ↓
commit changes
        ↓
open Pull Request
        ↓
CI passes
        ↓
switch Fabric Dev back to main
        ↓
merge Pull Request


## CI Workflow

GitHub Actions runs CI for Pull Requests targeting main.

CI currently validates:
- Repository structure
- Python business logic
- Profit calculations
- Edge cases
- Data-quality contracts
- Schema expectations
- Release validation logic

Example unit-tested business logic includes:
- gross_amount
- discount_amount
- net_revenue
- estimated_cost
- profit_amount
- profit_margin

The CI workflow runs:
python -m pytest -q

## CD Workflow

CD runs automatically after a change is merged into main.

Merge to main
     ↓
GitHub Actions CD
     ↓
Authenticate to Microsoft Fabric
     ↓
Sync Fabric Dev from GitHub main
     ↓
Deploy Dev → Test
     ↓
Run Test pipeline
     ↓
Run release validation notebook
     ↓
Validation PASS?
     │
   No ─────→ Stop deployment
     │
    Yes
     ↓
Deploy Test → Production

GitHub Actions acts as the CD orchestrator.

Fabric Deployment Pipelines remain responsible for promoting Fabric artifacts between environments.

## Authentication

GitHub Actions authenticates to Microsoft Fabric using a Microsoft Entra service principal.

Sensitive credentials are stored as GitHub Actions secrets:

- AZURE_TENANT_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET

Non-sensitive Fabric object IDs are stored as GitHub repository variables.

Examples:
- FABRIC_DEV_WORKSPACE_ID
- FABRIC_TEST_WORKSPACE_ID
- FABRIC_TEST_PIPELINE_ID
- FABRIC_DEPLOYMENT_PIPELINE_ID
- FABRIC_DEV_STAGE_ID
- FABRIC_TEST_STAGE_ID
- FABRIC_PROD_STAGE_ID
- FABRIC_GITHUB_CONNECTION_ID

## Automated Test Release Gate

After deployment to Test, GitHub Actions automatically runs pl_daily_sales.

The pipeline executes:

nb_transform_sales
        ↓
nb_validate_release

The validation notebook checks conditions such as:

- silver_sales exists
- gold_daily_sales exists
- expected Silver columns exist
- invalid row count = 0
- expected Test revenue = 465.00

If validation fails, the Fabric pipeline fails and GitHub Actions stops the release.

Production deployment only occurs after the Test gate succeeds.

## Repository Structure

fabric-retail-cicd/
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── fabric/
│   ├── lh_retail.Lakehouse/
│   ├── nb_transform_sales.Notebook/
│   ├── nb_validate_release.Notebook/
│   └── pl_daily_sales.DataPipeline/
│
├── scripts/
│   └── validate_test_release.py
│
├── src/
│   ├── __init__.py
│   └── retail_logic.py
│
├── tests/
│   ├── fixtures/
│   ├── test_basic.py
│   ├── test_notebook_definition.py
│   ├── test_retail_logic.py
│   └── test_release_validation.py
│
├── README.md
└── .gitignore

## Failure Scenarios and Lessons Learned

This project intentionally kept several real implementation problems instead of hiding them.

1. Delta schema evolution

Adding:
estimated_cost
profit_amount
profit_margin

caused a Delta schema mismatch because the existing Silver table used the old schema.

The solution for this full-refresh pipeline was: .option("overwriteSchema", "true")

Schema changes are part of the data contract and must be handled explicitly.

2. Python import failure in CI

GitHub Actions initially failed with: ModuleNotFoundError: No module named 'src'

The workflow was updated to run pytest with the repository root on PYTHONPATH.

Local Python execution and CI environments may resolve imports differently.

3. HTTP 411 when calling Fabric

The Fabric Data Pipeline REST call initially returned: 411 Length Required

because the POST request had no body.

The request was corrected by sending: -d '{}'

REST automation requires attention to HTTP request semantics, not only API endpoints.

4. Service principal Git credentials

The service principal could authenticate to Fabric but initially returned: {"source": "None"}

The GitHub connection had to be configured for the service principal using a Fabric configured connection.

Fabric API authentication and Fabric Git authentication are separate concerns.

## Git update override protection

Fabric Git synchronization returned: OverrideItemsNotAllowed

The CD workflow was updated with:

"options": {
  "allowOverrideItems": true
}

Automated deployment should explicitly define which system is authoritative.

In this project, merged GitHub main is the source of truth for the Dev workspace.

## Merge conflicts

The CD workflow eventually produced a Git merge conflict in: .github/workflows/cd.yml

The conflict was manually resolved while preserving the required Fabric Git synchronization options.

CI/CD configuration is production code and requires the same Git discipline as application or data-pipeline code

## CI/CD Responsibilities

GitHub
→ source control
→ feature branches
→ Pull Requests
→ version history

GitHub Actions CI
→ pre-merge automated testing

GitHub Actions CD
→ release orchestration

Fabric Git Integration
→ synchronize main into Dev

Fabric Deployment Pipelines
→ Dev → Test → Production promotion

Fabric Test
→ runtime validation and release gate

Fabric Production
→ released workload

## Release History

### v1.0.0 - Initial Retail Sales pipeline

CSV
→ Bronze
→ Silver
→ Gold

Includes initial Fabric Dev/Test/Prod deployment workflow.

### v2.0.0 - Automated Fabric CI/CD

feature branch
→ Pull Request
→ CI
→ merge main
→ Git sync
→ Dev → Test
→ automated Test validation
→ Production

## Project Evidence

### Pull Request CI

![Pull Request CI](docs/images/01-pr-ci-passed.png)

### Fabric Deployment Pipeline

![Fabric Deployment Pipeline](docs/images/02-fabric-deployment-pipeline.png)

### Automated CD

![GitHub Actions CD](docs/images/03-github-actions-full-cd.png)

### Automated Test Gate

![Test Validation](docs/images/04-test-validation-passed.png)

### Production Deployment

![Production Deployment](docs/images/05-prod-deployment-passed.png)

## Skills Demonstrated

Microsoft Fabric, PySpark, Delta Lake, OneLake, Fabric Data Pipelines, Fabric Deployment Pipelines, GitHub, GitHub Actions, Git branching, Pull Requests, CI/CD, Microsoft Entra service principals, REST APIs, automated testing, release validation, Dev/Test/Prod environment promotion.
