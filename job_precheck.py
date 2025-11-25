import re
import logging

logger = logging.getLogger(__name__)

def quick_precheck_job(preview_text, job_title, company_name=""):

    
    company_check = check_company_blacklist(company_name, preview_text)
    if not company_check[0]:
        return company_check
    experience_check = check_experience_requirement(preview_text)
    if not experience_check[0]:
        return experience_check
    
    clearance_check = check_clearance_requirements(preview_text)
    if not clearance_check[0]:
        return clearance_check
    
    logger.info(f"✅ Pre-checks passed for: '{job_title}' (skill check will determine final decision)")
    return (True, "Passed all pre-checks")


def check_title_keywords(job_title):
    
    title_lower = job_title.lower()
    
    required_keywords = [
        'data engineer',
        'data scientist', 
        'data analyst',
        'ml engineer',
        'machine learning engineer',
        'ai engineer'
    ]
    
    for keyword in required_keywords:
        if keyword in title_lower:
            logger.info(f"✅ Title check passed: '{job_title}' contains '{keyword}'")
            return (True, f"Title contains '{keyword}'")
    
    logger.info(f"❌ Title filter: '{job_title}' doesn't contain required keywords")
    return (False, f"Title doesn't contain target keywords (data engineer, data scientist, data analyst, ml engineer, ai engineer)")


def check_job_title_relevance(job_title):
   
    title_lower = job_title.lower()
    
    invalid_keywords = [
        'data center', 'datacenter', 'data centre',
        
        'power engineer', 'mechanical engineer', 'electrical engineer',
        'hvac engineer', 'cooling engineer', 'facilities engineer',
        
        'help desk', 'it support', 'system administrator',
        
        'project manager', 'product manager',
        'account manager', 'sales engineer',
        
        'lab technician', 'clinical researcher',
    ]
    
    for keyword in invalid_keywords:
        if keyword in title_lower:
            logger.info(f"❌ Title filter: '{job_title}' contains '{keyword}'")
            return (False, f"Invalid job type: Contains '{keyword}'")
    
    valid_keywords = [
        'data engineer', 'etl engineer', 'big data engineer',
        'data pipeline', 'platform engineer',
        'data scientist', 'machine learning', 'ml engineer',
        'applied scientist',
        
        'data analyst', 'analytics engineer', 'bi analyst',
        'business intelligence', 'reporting analyst',
        'ai engineer', 'ai/ml', 'artificial intelligence',
        'deep learning', 'nlp engineer', 'computer vision',
        'software engineer', 'software developer', 'backend engineer',
        'full stack', 'fullstack', 'application engineer',
    ]
    
    has_valid_keyword = any(keyword in title_lower for keyword in valid_keywords)
    
    if has_valid_keyword:
        logger.info(f"✅ Title check passed: '{job_title}'")
        return (True, "Title is relevant")
    
    logger.info(f"❌ Title filter: '{job_title}' doesn't match valid roles")
    return (False, f"Job title not in target roles")


def check_company_blacklist(company_name, preview_text=""):
    blacklisted_companies = [
        'amazon', 
        'apple',
        
    ]
    
    company_lower = company_name.lower().strip() if company_name else ""
    
    for blacklisted in blacklisted_companies:
        if blacklisted in company_lower:
            logger.info(f"❌ Company filter: '{company_name}' is blacklisted")
            return (False, f"Company '{company_name}' is in blacklist")
    
    if preview_text and not company_name:
        text_lower = preview_text.lower()
        for blacklisted in blacklisted_companies:
            if blacklisted in text_lower:
                logger.info(f"❌ Company filter: Found '{blacklisted}' in preview text")
                return (False, f"Company '{blacklisted}' is in blacklist")
    
    logger.info(f"✅ Company check passed: '{company_name or 'Unknown'}'")
    return (True, "Company not blacklisted")


def check_experience_requirement(text):
    
    text_lower = text.lower()
    
    
    
    numeric_patterns = [
        r'(\d+)\s*\+?\s*(?:-\s*\d+)?\s*years?\s+(?:of\s+)?(?:experience|exp)',
        r'(?:minimum|minimum of|at least)\s+(\d+)\s*\+?\s*years?',
        r'(\d+)\s*\+?\s*years?\s+(?:experience|exp)',
        r'with\s+(\d+)\s*\+?\s*years?',
        r'\((\d+)\)\s*years?', 
    ]
    
    found_years = []
    
    for pattern in numeric_patterns:
        matches = re.findall(pattern, text_lower)
        if matches:
            for match in matches:
                try:
                    years = int(match)
                    found_years.append(years)
                except:
                    continue
    
    
    written_years_map = {
        'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
        'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12
    }
    
    for word, num in written_years_map.items():
        if num > 3:
            
            if f"{word} years" in text_lower or f"{word} ({num})" in text_lower:
                found_years.append(num)
    
    if found_years:
        max_years = max(found_years)
        if max_years > 3:
            logger.info(f"❌ Experience filter: Requires {max_years} years (>3 limit)")
            return (False, f"Requires {max_years} years experience (>3 years limit)")
    
    senior_indicators = [
        'senior', 'sr.', 'lead', 'principal', 'staff', 'architect'
    ]
    
    senior_count = sum(1 for indicator in senior_indicators if indicator in text_lower)
    
    if senior_count >= 2 and found_years and max(found_years) >= 3:
        logger.info(f"⚠️ Experience filter: Multiple senior indicators + {max(found_years)} years")
        return (False, f"Likely requires senior experience (>3 years)")
    
    logger.info(f"✅ Experience check passed (Years found: {found_years or 'None'})")
    return (True, "Experience requirement acceptable")


def check_clearance_requirements(text):

    text_lower = text.lower()
    
    clearance_keywords = [
        'clearance required', 'security clearance', 'ts/sci', 'top secret',
        'secret clearance', 'polygraph', 'dod clearance',
        'active clearance', 'must have clearance', 'requires clearance'
    ]
    
    for keyword in clearance_keywords:
        if keyword in text_lower:
            logger.info(f"❌ Clearance filter: Contains '{keyword}'")
            return (False, f"Requires security clearance: '{keyword}'")
    
    citizenship_keywords = [
        'us citizen only', 'u.s. citizen only', 'citizenship required',
        'must be a us citizen', 'must be a u.s. citizen',
        'us citizenship required', 'american citizen only',
        'no sponsorship', 'cannot sponsor', 'will not sponsor',
        'must be authorized to work', 'no visa sponsorship'
    ]
    
    for keyword in citizenship_keywords:
        if keyword in text_lower:
            logger.info(f"❌ Citizenship filter: Contains '{keyword}'")
            return (False, f"Requires US citizenship/no sponsorship: '{keyword}'")
    
    logger.info(f"✅ Clearance/citizenship check passed")
    return (True, "No clearance/citizenship restrictions")


def classify_job_role(job_title):
    
    title_lower = job_title.lower()
    
    ai_keywords = [
        'ai engineer', 'ml engineer', 'machine learning engineer',
        'mlops', 'ai/ml', 'artificial intelligence engineer',
        'deep learning engineer', 'nlp engineer', 'computer vision engineer'
    ]
    if any(kw in title_lower for kw in ai_keywords):
        return 'ai_engineer'
    
    ds_keywords = [
        'data scientist', 'applied scientist', 'research scientist',
        'quantitative analyst', 'ml scientist', 'applied ml'
    ]
    if any(kw in title_lower for kw in ds_keywords):
        return 'data_scientist'
    
    de_keywords = [
        'data engineer', 'etl engineer', 'etl developer', 'big data engineer',
        'data pipeline', 'platform engineer', 'analytics engineer'
    ]
    if any(kw in title_lower for kw in de_keywords):
        return 'data_engineer'
    
    da_keywords = [
        'data analyst', 'business intelligence', 'bi analyst',
        'reporting analyst', 'analytics'
    ]
    if any(kw in title_lower for kw in da_keywords):
        return 'data_analyst'
    
    logger.info(f"⚠️ Could not classify role: '{job_title}'")
    return None


def extract_skills_from_text(text):
   
    if not text:
        return set()
    
    text_lower = text.lower()
    
    all_skills = [
        'python', 'sql', 'r', 'scala', 'java', 'javascript', 'typescript', 'go', 'c++', 'c#',
        
        'spark', 'airflow', 'kafka', 'etl', 'elt', 'data pipeline', 'data warehouse', 'data lake',
        'glue', 'emr', 'databricks', 'dbt', 'fivetran', 'talend', 'nifi',
        'kinesis', 'batch processing', 'stream processing', 'hadoop', 'hive', 'presto', 'athena',
        
        'postgres', 'postgresql', 'mysql', 'mongodb', 'dynamodb', 'cassandra', 'redis',
        'redshift', 'snowflake', 'bigquery', 'oracle', 'sql server',
        
        'aws', 'azure', 'gcp', 'google cloud', 's3', 'lambda', 'ec2', 'rds',
        'cloud', 'serverless',
        
        'docker', 'kubernetes', 'terraform', 'jenkins', 'git', 'gitlab', 'github',
        'ci/cd', 'ansible', 'circleci',
        
        'machine learning', 'deep learning', 'nlp', 'computer vision', 'statistics',
        'pandas', 'numpy', 'scikit-learn', 'sklearn', 'tensorflow', 'pytorch', 'keras',
        'jupyter', 'matplotlib', 'seaborn', 'a/b testing', 'hypothesis testing',
        'regression', 'classification', 'clustering', 'neural networks',
        'transformers', 'bert', 'gpt', 'llm', 'mlops',
        
        'tableau', 'power bi', 'looker', 'data visualization', 'dashboards',
        
        'rest', 'api', 'graphql', 'microservices', 'backend', 'frontend', 'full stack',
        'react', 'node', 'express', 'fastapi', 'flask', 'django'
    ]
    
    found_skills = set()
    for skill in all_skills:
        if skill in text_lower:
            found_skills.add(skill)
    
    return found_skills


def check_skill_match_with_resume(jd_text, user_skills, threshold=0.5):
   
    if not jd_text or not user_skills:
        return (False, 0.0, set(), set())
    
    jd_skills = extract_skills_from_text(jd_text)
    
    if not jd_skills:
        logger.info("❌ No skills found in JD")
        return (False, 0.0, set(), set())
    
    matched_skills = jd_skills.intersection(user_skills)
    missing_skills = jd_skills.difference(user_skills)
    
    match_percentage = len(matched_skills) / len(jd_skills) if jd_skills else 0.0
    
    logger.info(f"📊 Skill match: {match_percentage*100:.1f}% ({len(matched_skills)}/{len(jd_skills)} skills)")
    if matched_skills:
        logger.info(f"   Matched: {', '.join(sorted(list(matched_skills)[:10]))}")
    
    return (match_percentage >= threshold, match_percentage, matched_skills, missing_skills)


def should_save_job(job_title, jd_text, user_skills, skill_threshold=0.5):
    
    is_skill_match, match_pct, matched, missing = check_skill_match_with_resume(
        jd_text, user_skills, skill_threshold
    )
    
   
    if is_skill_match:
        logger.info(f"✅ SAVE: {match_pct*100:.1f}% skill match (threshold: {skill_threshold*100}%)")
        return (True, f"Skill match: {match_pct*100:.1f}%", match_pct)
    
    
    logger.info(f"⚠️ Skill match below threshold ({match_pct*100:.1f}% < {skill_threshold*100}%)")
    logger.info(f"   Checking title as fallback...")
    
    title_check = check_title_keywords(job_title)
    
    if title_check[0]:
       
        logger.info(f"✅ SAVE: Title saved it - '{job_title}' contains target keywords")
        return (True, f"Title fallback: {title_check[1]} (skill match: {match_pct*100:.1f}%)", match_pct)
    else:
       
        logger.info(f"❌ SKIP: Skill match too low ({match_pct*100:.1f}%) AND title doesn't match")
        return (False, f"Low skill match ({match_pct*100:.1f}%) and title doesn't contain keywords", match_pct)

