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


### 🚀 Real GitHub Actions YAML for the Auto Loader Pipeline
This pipeline:
- Runs on pushes to main
- Authenticates to Databricks using a service principal
- Deploys notebooks to the workspace
- Deploys the Databricks Job definition
- Runs a smoke test job in TEST
- Promotes to PROD if tests pass

 **Full YAML:**
 ```
 name: Deploy Customer Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout repository
      - name: Checkout code
        uses: actions/checkout@v3

      # 2. Install Databricks CLI
      - name: Install Databricks CLI
        run: pip install databricks-cli

      # 3. Authenticate using Service Principal
      - name: Configure Databricks CLI
        run: |
          databricks configure --aad-token --host ${{ secrets.DATABRICKS_HOST }} <<EOF
          ${{ secrets.DATABRICKS_AAD_TOKEN }}
          EOF

      # 4. Deploy notebooks to TEST workspace
      - name: Deploy notebooks to TEST
        run: |
          databricks workspace import_dir \
            ./notebooks \
            /Repos/test/customer_pipeline \
            --overwrite

      # 5. Deploy job definition to TEST
      - name: Deploy job to TEST
        run: |
          databricks jobs reset \
            --job-id ${{ secrets.TEST_JOB_ID }} \
            --json-file jobs/customer_pipeline.json

      # 6. Run smoke test in TEST
      - name: Run smoke test
        run: |
          databricks jobs run-now \
            --job-id ${{ secrets.TEST_JOB_ID }}

      # 7. Deploy to PROD only if TEST succeeded
      - name: Deploy notebooks to PROD
        if: success()
        run: |
          databricks workspace import_dir \
            ./notebooks \
            /Repos/prod/customer_pipeline \
            --overwrite

      - name: Deploy job to PROD
        if: success()
        run: |
          databricks jobs reset \
            --job-id ${{ secrets.PROD_JOB_ID }} \
            --json-file jobs/customer_pipeline.json

 ```


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


<br><br>
# 🧱 Putting it all together (simple map)
Here’s the full journey in one clean flow:

```
Databricks DEV (you build)
        ↓
GitHub (you push code)
        ↓
GitHub Actions CI (tests)
        ↓
Pull Request (review)
        ↓
Merge to main
        ↓
GitHub Actions CD (service principal deploys)
        ↓
Databricks TEST (validation)
        ↓
Databricks PROD (production)

```

<br><br>
# 🎯 The key idea

You **develop in Databricks,**  
you **version and review in GitHub,**  
and you **deploy through CI/CD** using a service principal.  

Each environment has a clear purpose:


|Stage	|Where you work|	Purpose
|---|---|---|
|Development|	Databricks DEV|	Build & experiment
|Version control|	GitHub|	Track changes
|CI	|GitHub Actions|	Test code
|Review|	GitHub PR	|Team approval
|CD|	GitHub Actions → Databricks	|Deploy code
|Validation|	Databricks TEST|	Ensure correctness
|Production|	Databricks PROD	|Run business workloads



<br><br>
# 🌍 Real Scenario: Customer Data Pipeline
Your company receives daily JSON files with customer updates.
They land in cloud storage:

```
/raw/customers/YYYY/MM/DD/*.json

```
**You need to:**
- Ingest them with Auto Loader
- Store raw data in Bronze
- Clean and dedupe in Silver
- Build analytics tables in Gold
- Deploy everything through CI/CD
- Run it daily with Databricks Jobs

Let’s walk through the entire journey.

## 🧱 STEP 1 — You develop in Databricks DEV workspace
You create three notebooks:

### 1. Bronze notebook — Auto Loader ingestion
```
df = (
    spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")
        .load("/mnt/raw/customers/")
)

df.writeStream.format("delta") \
    .option("checkpointLocation", "/mnt/checkpoints/bronze/customers") \
    .trigger(availableNow=True) \
    .start("/mnt/bronze/customers")
```

### 2. Silver notebook — Clean + dedupe
```
from pyspark.sql import functions as F, Window

df = spark.read.table("bronze.customers")

w = Window.partitionBy("customer_id").orderBy(F.col("updated_at").desc())

cleaned = (
    df.withColumn("rn", F.row_number().over(w))
      .filter("rn = 1")
      .drop("rn")
)

cleaned.write.format("delta").mode("overwrite").saveAsTable("silver.customers")
```

### 3. Gold notebook — Business logic
```
df = spark.read.table("silver.customers")

gold = df.select("customer_id", "name", "country")

gold.write.format("delta").mode("overwrite").saveAsTable("gold.customer_dim")

```

⚠️ **You test everything in DEV until it works.**

<br><br>
## 🧱 STEP 2 — You push your code to GitHub
**You create a branch:**
```
feature/customer-pipeline

```
You commit:
```
/notebooks/bronze_customers.py
/notebooks/silver_customers.py
/notebooks/gold_customer_dim.py
/jobs/customer_pipeline.json
```
**Push the branch.**

<br><br>
## 🧪 STEP 3 — GitHub Actions CI runs
**CI checks:**
- notebook syntax
- Python linting
- unit tests (if any)
- JSON validation for job definitions

⚠️ **If something fails, you fix it.**

<br><br>
## 🔀 STEP 4 — You open a Pull Request
**Your team reviews:**
- logic
- naming
- performance
- schema handling
- deduplication logic

Once approved → **merge to main.**

<br><br>
## 🚀 STEP 5 — GitHub Actions CD deploys to Databricks TEST
**The pipeline:**
- Authenticates using a service principal
- Deploys notebooks to TEST workspace
- Updates the Databricks Job
- Runs a smoke test job

**Example job definition (customer_pipeline.json)**
```
{
  "name": "customer_pipeline",
  "tasks": [
    { "task_key": "bronze", "notebook_task": { "notebook_path": "/Repos/prod/bronze_customers" } },
    { "task_key": "silver", "notebook_task": { "notebook_path": "/Repos/prod/silver_customers" }, "depends_on": [{"task_key": "bronze"}] },
    { "task_key": "gold", "notebook_task": { "notebook_path": "/Repos/prod/gold_customer_dim" }, "depends_on": [{"task_key": "silver"}] }
  ]
}
```
**The CD pipeline updates the job:**
```
databricks jobs reset --job-id $JOB_ID --json-file jobs/customer_pipeline.json
```


<br><br>
## 🧪 STEP 6 — Tests run in TEST workspace
**The job runs:**

- Bronze Auto Loader ingestion
- Silver cleaning
- Gold dimension table creation

**If everything works → promote to PROD.**


<br><br>
## 🏁 STEP 7 — CD deploys to PROD
Same notebooks  
Same job definition  
Same workflow  
Same service principal  

**Now your pipeline is live.**


<br><br>
## 🕒 STEP 8 — Databricks Job runs daily
The job runs every night at 2 AM:
- Auto Loader ingests new files
- Silver dedupes and cleans
- Gold updates analytics tables

Dashboards and reports use the Gold tables.


<br><br>
## 🎯 Full Flow Summary
```
DEV Workspace → GitHub Branch → CI → PR → Merge → CD → TEST Workspace → Tests → PROD Workspace → Daily Job
```

### And the key players:

|Component	|Role|
|---|---|
|Auto Loader|	Ingest raw files into Bronze|
|Bronze notebook|	Raw ingestion|
|Silver notebook|	Clean + dedupe|
|Gold notebook|	Business tables|
|GitHub	Version |control|
|GitHub Actions|	CI/CD automation|
|Service Principal|	Secure non-human authentication|
|Databricks Jobs|	Scheduled pipeline execution|
|TEST workspace|	Validation|
|PROD workspace|	Production workloads|
