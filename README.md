# Microsoft Fabric Retail Sales CI/CD Project

A small end-to-end Microsoft Fabric data engineering project built primarily
to practice professional CI/CD workflows.

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

CSV → Fabric Data Pipeline → Lakehouse Bronze → PySpark →
Silver/Gold Delta Tables → Semantic Model / Power BI

## Environments

- Retail-CICD-Dev
- Retail-CICD-Test
- Retail-CICD-Prod
