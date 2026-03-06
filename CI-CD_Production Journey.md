# 🧭 The Full Databricks Development → CI/CD → Production Journey
Below is the exact sequence of where you work at each stage, and what happens in each environment.

<br><br>
## 1️⃣ You start in Databricks DEV workspace
**This is your playground.**

### What you do here:
- Write notebooks
- Test transformations
- Explore data
- Build models
- Try new logic
- Break things freely

### Where this happens:
👉 **Inside the Databricks DEV workspace**  
Using your personal user identity.

You are NOT touching GitHub yet.
You are just experimenting and building.

<br><br>
## 2️⃣ When your code works, you move it to GitHub
**Now you switch from “exploration mode” to “engineering mode”.**

### What you do:

- Create a new branch  
  Example:
 ```feature/add-customer-cleaning```
- Export or sync your notebook to GitHub
- Commit your code
- Push the branch

### Where this happens:
**👉 GitHub (your repo)**  
This is where version control begins.

<br><br>
## 3️⃣ GitHub Actions runs CI on your branch
**This is where automation starts.**

### What happens:
- Tests run
- Linting runs
- Notebook validation
- Packaging (if needed)

### Where this happens:
👉 **GitHub Actions Runner (a temporary VM)**  
Not Databricks yet.

This VM checks your code quality before merging.


## 4️⃣ You open a Pull Request (PR)
**This is the team review stage.**

### What happens:
- Teammates review your code
- Comments, suggestions, fixes
- Approvals

### Where this happens:
👉 **GitHub Pull Request interface** 

This is the “quality gate” before code enters main.

<br><br>
## 5️⃣ PR is merged → CD pipeline starts
**Now your code is ready to be deployed.**

### What happens:
**GitHub Actions pipeline starts** 

- It authenticates to Databricks using a service principal
- It deploys notebooks to TEST workspace
- It updates jobs/workflows
- It runs smoke tests

### Where this happens:

- Authentication: GitHub Runner → Databricks
- Deployment: Databricks TEST workspace
- Tests: Databricks cluster

This is the first time your code touches Databricks again.

<br><br>
## 6️⃣ Promotion to PROD
**If tests pass, the pipeline promotes your code to production.** 

### What happens:
- Same notebooks deployed to PROD
- PROD workflows updated
- PROD clusters run validation
- Notifications sent

### Where this happens:
👉 **Databricks PROD workspace** 

This is the final destination.
