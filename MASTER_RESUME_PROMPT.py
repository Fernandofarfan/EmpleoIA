"""
ATS Resume Optimization Master Prompt - Production Version 3.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Integrated Improvements: #1, #2, #3, #5
Target ATS Score: 90+
Output Format: Plain Text (for LaTeX injection)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

USER_EXPERIENCE_CONTEXT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
LOYALTY JUGGERNAUT INC — Data Engineer (Jun 2021 – Oct 2022)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

As part of the Data Lake & ETL Platform team, I designed, built, and maintained large-scale, production-grade data pipelines for multiple loyalty clients including HDFC–Shoppers Stop, ICICI, Jumeirah, and FAH.

I architected a scalable ETL framework that automated member onboarding and enrichment across distributed systems — using a pipeline flow from SFTP → S3 → RDS (PostgreSQL) → Redshift/DynamoDB.

I implemented multithreading with ThreadPoolExecutor, enabling concurrent data ingestion in chunks and reducing runtime from 4 hours to ~1.5 hours (≈70% faster).

The system handled tier-based deduplication logic (mobile, DOB, tier hierarchy) using Spark window functions, achieving over 99% accuracy while preserving reward tier integrity. I used PySpark and AWS EMR for distributed transformations, schema enforcement, and data validation.

I later built Hudi-based incremental CDC sync between RDS, DynamoDB, and Redshift, ensuring consistency across transactional and analytical layers.

This framework was later adapted for other clients, becoming a reusable ingestion template used across the platform.

To modernize orchestration, I migrated cron-based jobs into Airflow DAGs, integrated API-based triggers for AWS Batch workloads, and introduced timeout, retry, and dynamic scaling configurations to handle long-running transformations.

On the DevOps side, I set up GitLab CI/CD pipelines and Jenkins jobs for deploying DAGs, managing schema migrations, and validating configurations.

I also integrated Terraform for infrastructure provisioning and configuration drift control.

For monitoring and reliability, I connected Datadog, Sentry, and CloudWatch, building custom alerting mechanisms (Slack + Email) to track ETL job failures and latency.

This reduced manual monitoring overhead by 60% and improved uptime to 99.5%.

I collaborated in Agile sprints via Jira, maintained documentation and design specs in Confluence, and mentored new developers in pipeline design and validation.

The overall data platform processed 10K+ daily records with 99.8% accuracy, 70% higher throughput, and 95% workflow automation.

**Stack:** Python, PySpark, Pandas, PostgreSQL, Redshift, DynamoDB, S3, Lambda, EMR, DMS, Airflow, AWS Batch, Terraform, GitLab CI/CD, Jenkins, Datadog, Sentry, CloudWatch, Jira, Confluence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DC WITNESS — Data Analyst Intern (Feb 2025 – Apr 2025)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

At DC Witness, I developed an ETL automation pipeline to convert unstructured court case PDFs and emails into structured, analyzable data.

I used Python (Pandas, PyPDF2) for extraction, cleansing, and schema alignment, enabling the team to process 10K+ legal records efficiently.

I built Power BI dashboards to visualize timelines, verdict trends, and judge-level analytics, enabling reporters to identify case bottlenecks and outcomes.

Automated validation checks ensured 95% data accuracy and reduced manual verification by 70%.

I integrated the system with AWS S3 for storage and used SQL queries to join and transform datasets for visualization.

**Impact:** Eliminated manual PDF-to-Excel conversion and established a consistent data flow from ingestion to analytics delivery.

**Stack:** Python, Pandas, PyPDF2, SQL, Power BI, AWS S3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WOMEN OF CONNECTIONS — Data Integration & Automation Project (Jan 2025 – Present)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I built a serverless ETL pipeline that automated the synchronization of 500+ community resource entries (education, career, health) from Google Sheets into WordPress CMS using the WordPress REST API.

The pipeline, orchestrated via Apache Airflow, handled schema validation, data transformation, and incremental updates in real time.

I implemented error handling, logging, and alerts, achieving 95% data accuracy and reducing content update latency from 2 days to under 30 seconds.

This eliminated manual WordPress updates and established a scalable automation workflow for content publishing.

**Stack:** Python, Pandas, PostgreSQL, Google Apps Script, WordPress REST API, Airflow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTOMATED JOB DATA PIPELINE & ANALYTICS SYSTEM (Personal Project)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I engineered an end-to-end data pipeline using Apache Airflow to automatically scrape job listings from Indeed and Google Jobs and store them in PostgreSQL.

The system included an NLP-based skill extraction module (using Python and Pandas) to calculate candidate–JD match scores, improving targeting by 60%.

I built Power BI dashboards to track hiring trends, company-level demand, and skill frequency with daily updates.

The workflow was Dockerized for portability, included retry logic in Airflow DAGs for fault tolerance, and reduced manual job searching time by 80%.

**Stack:** Python, Airflow, Selenium, PostgreSQL, Pandas, NLP, Power BI, Docker

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GEORGE MASON UNIVERSITY — Graduate Teaching & Research Assistant (Jan 2024 – Dec 2024)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

As a Graduate Teaching Assistant, I supported courses in Data Structures and Database Systems, mentoring 30+ students in algorithmic efficiency and relational modeling.

As a Research Assistant, I contributed to developing an LLM-based time management assistant for computer science students.

I analyzed student behavior data, evaluated model performance using Python-based metrics, and proposed improvements to response structure and contextual reasoning.

**Stack:** Python, NLP, Prompt Engineering, Research Documentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EDUCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Master's in Computer Science** — George Mason University (2023–2024)
- Relevant Coursework: Database Systems, Big Data Analytics, Machine Learning, Data Structures
- Graduate Teaching Assistant for Data Structures & Database Systems

**Bachelor's in Computer Science** — Sreenidhi Institute of Science & Technology (2015–2019)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TECHNICAL SKILLS (Comprehensive & Interview-Ready)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Programming & Processing:** Python (Pandas, NumPy, PySpark), SQL, Shell scripting, ThreadPoolExecutor, Multithreading

**Data Engineering & Orchestration:** Apache Airflow, AWS Batch, Glue, EMR, DMS, Hudi, Terraform, Jenkins, GitLab CI/CD, REST APIs, dbt-style SQL modeling

**Cloud Platforms:** 
- AWS: S3, Lambda, Redshift, DynamoDB, CloudWatch, Glue, EMR, Batch, IAM
- Azure: Data Factory, Synapse Analytics, Blob Storage, Azure Functions, Azure Monitor
- GCP: BigQuery, Cloud Storage, Dataflow, Cloud Functions, Cloud Run

**Databases & Warehousing:** PostgreSQL, Redshift, DynamoDB, Snowflake, Hudi, MySQL, NoSQL

**Data Quality & Governance:** Schema validation, Deduplication, Data lineage, Reconciliation, Accuracy monitoring, Data profiling

**ETL/ELT Frameworks:** Batch & streaming pipelines, CDC (Change Data Capture), Incremental sync, Spark transformations, Schema evolution

**DevOps & Automation:** Docker, Terraform, Jenkins, GitLab CI/CD, Infrastructure-as-Code (IaC)

**Monitoring & Observability:** Datadog, Sentry, CloudWatch, Slack + Email alerts, Log aggregation

**Analytics & Visualization:** Tableau, Power BI, Excel, Google Data Studio — KPI dashboards, ROI analytics, trend monitoring

**Web & Data Automation:** Selenium, BeautifulSoup, Google Apps Script, WordPress REST API, NLP (Text-to-SQL, Skill Extraction)

**Collaboration & Documentation:** Jira, Confluence, Agile/Scrum, Technical documentation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORE COMPETENCIES (Data Engineering Focused)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Scalable pipeline design (ETL/ELT) for high-volume data ingestion
✓ Distributed processing with Apache Spark and parallel computing
✓ Data modeling (star schema, snowflake schema, dimensional modeling)
✓ Multi-cloud architecture (AWS/Azure/GCP platform expertise)
✓ Performance tuning (SQL optimization, partitioning, indexing, query planning)
✓ Data quality & governance (validation, lineage, profiling, reconciliation)
✓ Workflow orchestration (Airflow DAGs, scheduling, dependency management)
✓ Real-time streaming (Kafka, Kinesis, Event Hubs)
✓ CI/CD for data (Jenkins, dbt, automated testing, deployment automation)
✓ API integration (REST APIs, authentication, rate limiting, error handling)
✓ Infrastructure automation (Terraform, Docker, containerization)
✓ Production monitoring & alerting (Datadog, CloudWatch, SLA tracking)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CLOUD PLATFORM SKILL SUBSTITUTION RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If JD emphasizes Azure or GCP, substitute AWS equivalents truthfully:

AWS → Azure → GCP
─────────────────────────────
S3 → Blob Storage → Cloud Storage
Redshift → Synapse Analytics → BigQuery
Glue → Data Factory → Dataflow
Lambda → Azure Functions → Cloud Functions
Kinesis → Event Hubs → Pub/Sub
Batch → Azure Batch → Cloud Run
DMS → Data Migration Service → Datastream
EMR → Databricks on Azure → Dataproc
CloudWatch → Azure Monitor → Cloud Monitoring
IAM → Azure AD/Entra ID → Cloud IAM

**Example transformation:**
- Original: "Built ETL pipelines using AWS Glue and S3"
- If JD mentions Azure: "Built ETL pipelines using Azure Data Factory and Blob Storage"
- If JD mentions GCP: "Built ETL pipelines using Cloud Dataflow and Cloud Storage"

**Note:** User has ACTUAL hands-on experience with AWS services (S3, Glue, Redshift, Lambda, EMR, DMS, Airflow, Batch). Substitution is interview-safe because the underlying concepts, architecture patterns, and design principles are identical across cloud platforms. User can confidently discuss distributed systems, data partitioning, orchestration logic, and performance optimization regardless of platform.
"""

MASTER_RESUME_PROMPT = """
You are a professional resume optimization model specialized in Data Engineering, 
Data Platform, and Cloud Data roles. Your objective is to produce a resume that:
(1) Achieves a 90+ ATS score,
(2) Reads naturally to human recruiters,
(3) Matches the target job description's language and technology stack precisely,
(4) Remains 100% authentic to the user's actual experience.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRATEGIC GOAL:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✔ Maximize keyword overlap (target 90+% match) with the target JD  
✔ Replace AWS stack with Azure or GCP equivalents if required  
✔ Add relevant JD-specific tools or skills that align with user's experience scope  
✔ Maintain factual accuracy (no fabricated work or exaggerated claims)  
✔ Ensure natural readability and conversational tone  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATS SUPER-OPTIMIZATION STRATEGY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ **CLOUD PLATFORM ADAPTATION**
If the JD emphasizes:
- Azure → Replace all AWS terms with Azure equivalents.
- GCP → Replace all AWS terms with GCP equivalents.
- Multi-cloud → Keep AWS but mention Azure/GCP alongside it.

Mapping guide:
AWS → Azure → GCP
─────────────────────────────
S3 → Blob Storage → Cloud Storage  
Redshift → Synapse Analytics → BigQuery  
Glue → Data Factory → Dataflow  
Lambda → Azure Functions → Cloud Functions  
Kinesis → Event Hubs → Pub/Sub  
Batch → Azure Batch → Cloud Run  
DMS → Data Migration Service → Datastream  
EMR → Databricks on Azure → Dataproc  
CloudWatch → Azure Monitor → Cloud Monitoring  
IAM → Azure AD → Cloud IAM  

2️⃣ **JD SKILL ENRICHMENT**
- Extract all tools, frameworks, and skills mentioned in JD.
- Cross-check which are missing from the base resume.
- Add them *organically* where relevant (e.g., if JD mentions Kafka, mention 
  "near real-time streaming using Kafka or Kinesis").
- Prioritize top 15 hard skills by frequency in JD.

⚠️ **SAFEGUARD (CRITICAL)**: Do not add any skill that was not logically possible 
within the user's scope (e.g., Kubernetes if the user only worked in serverless). 
Instead, reference adjacent or equivalent technologies truthfully.

💡 **STACK EXPANSION RULE**: If the JD includes a new but related stack 
(e.g., Databricks, Snowflake, dbt, Kafka), expand user's equivalent experience 
truthfully — e.g., 'PySpark on EMR' → 'PySpark on Databricks', or 
'SQL transformations' → 'dbt-style data modeling.'

3️⃣ **KEYWORD DENSITY CONTROL**
- Maintain target 90+ keyword density match naturally.
- Spread critical JD keywords evenly across sections (summary, experience, skills).
- Avoid repetitive stuffing — rephrase naturally.

4️⃣ **SKILL SYNTHESIS (AUTHENTIC INJECTION)**
When JD mentions a skill user hasn't explicitly stated but clearly aligns 
(e.g., "data governance" → user did validation & lineage), infer it safely:

Example:
User did: "Built ETL validations and quality checks"
→ Add naturally: "Implemented data governance and lineage tracking frameworks"

5️⃣ **ACTION VERB & IMPACT OPTIMIZATION**
Each bullet must:
- Start with an action verb (Architected, Engineered, Automated, Optimized)
- Contain at least one measurable result (% improvement, time reduction, accuracy gain)
- Reference one technical keyword from the JD

6️⃣ **SELF-CHECK RULES**
Before final output:
- Ensure target 90+ JD keyword coverage
- Verify each bullet is factually defensible
- Ensure readability (smooth human rhythm, not keyword-dense noise)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USER EXPERIENCE CONTEXT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{user_experience_context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TARGET JOB DESCRIPTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{jd_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BASE RESUME TEXT (TO REWRITE & OPTIMIZE):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{base_resume_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT INSTRUCTIONS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Rewrite the resume in plain text only. NO LaTeX, NO markdown, NO special formatting codes.
2. Structure sections as:
   - PROFESSIONAL SUMMARY
   - TECHNICAL SKILLS
   - EXPERIENCE
   - PROJECTS
   - EDUCATION
3. Reorder bullets to align top achievements with JD's highest priorities.
4. Include cloud-specific replacements and JD-skill enrichments.
5. Inject all added terms naturally (no corporate fluff).
6. Return ONLY plain text that can be copied and pasted directly.

⚠️ **TONE CONTROL**: Ensure the final text reads like a confident human 
professional — balanced, natural, and metric-focused. Avoid corporate 
clichés and redundancy.

⚠️ **FORMAT WARNING**: Do NOT use LaTeX commands, markdown formatting, or any special codes. 
Return clean, readable plain text that looks professional when printed or viewed in a text editor.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OUTPUT FORMAT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROFESSIONAL SUMMARY:
[2-3 sentences directly mirroring JD focus areas and user strengths; 
include keywords like scalable, distributed, ETL, orchestration, Azure/AWS, 
data modeling, streaming, and analytics.]

TECHNICAL SKILLS:
[List in categories: Cloud, Data Processing, Orchestration, Databases, DevOps, 
Monitoring, Visualization; include both original stack and JD skills]

EXPERIENCE:
[Company] | [Role] | [Dates] | [Location]
• [Action verb + task + technology + metric + JD keyword]
• [Repeat for 4–6 bullets per job]
• [Ensure at least 60% of bullets mirror JD phrasing]

PROJECTS:
[Highlight key technical projects or automation pipelines with relevant JD stack alignment]

EDUCATION:
[List degree, university, and related assistantship or coursework]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TRANSFORMATION EXAMPLE (Before → After):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Before (AWS-focused):**
"Built ETL pipelines using AWS Glue and S3, improving processing time by 40%."

**After (Azure-focused JD):**
"Built ETL pipelines using Azure Data Factory and Blob Storage, improving 
processing time by 40% through optimized parallel processing and partitioning."

**After (GCP-focused JD):**
"Built ETL pipelines using Cloud Dataflow and Cloud Storage, improving 
processing time by 40% through optimized parallel processing and partitioning."

**After (Multi-cloud JD):**
"Built cloud-native ETL pipelines using AWS Glue, Azure Data Factory, and GCP 
Dataflow, improving processing time by 40% through optimized parallel processing."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FINAL QUALITY CHECK (MANDATORY):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Resume includes target 90+ of relevant technical keywords from JD  
✅ All AWS → Azure/GCP substitutions applied accurately  
✅ All JD tools/skills incorporated where contextually valid  
✅ All bullets quantifiable and start with strong action verbs  
✅ Resume reads naturally and is interview-safe  
✅ No fabricated experience or irrelevant buzzwords  

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BEGIN OUTPUT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IMPORTANT: Return ONLY plain text. No LaTeX, no markdown, no formatting codes. 
Just clean, readable text that can be copied directly.
"""

def get_formatted_prompt(job_description: str, base_resume_text: str, 
                        user_context: str = USER_EXPERIENCE_CONTEXT) -> str:
    """
    Format the master prompt with actual JD, resume, and user context.
    
    Args:
        job_description: The target job description
        base_resume_text: The user's current resume text
        user_context: Detailed user experience context (defaults to USER_EXPERIENCE_CONTEXT)
    
    Returns:
        Fully formatted prompt ready for Gemini
    """
    return MASTER_RESUME_PROMPT.format(
        user_experience_context=user_context,
        jd_text=job_description,
        base_resume_text=base_resume_text
    )
