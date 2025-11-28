"""
Stub module for job_precheck functions.
These functions are imported by scrapers but not actively used.
"""

def quick_precheck_job(card_preview_text, job_title, company):
    """
    Stub function for quick job pre-check.
    Returns: (should_process, reason)
    """
    return (True, "Pre-check passed")

def classify_job_role(job_title):
    """
    Stub function for job role classification.
    Returns: role category string
    """
    return "general"

def should_save_job(job_title, jd_text, user_skills, skill_threshold=0.5):
    """
    Stub function for job saving decision.
    Returns: (should_save, reason, match_percentage)
    """
    return (True, "Job matches criteria", 0.75)
