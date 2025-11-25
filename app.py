from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_from_directory, send_file
import os
import threading
import logging
import glob
from datetime import datetime
import time
import pandas as pd
import random
import sys
import json
import mysql.connector
from db_config import db_manager

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.indeed_scraper import indeedScraper
from scrapers.linkedin_scraper import linkedinClass
from scrapers.linkedin_connection import linkedinConnections

from resume_parser import resumeParser, jobMatcher
from job_precheck import extract_skills_from_text
from simple_resume_optimizer import simpleResumeOptimizer
from cover_letter_generator import CoverLetterGenerator

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.jinja_env.auto_reload = True

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

for folder in ['uploads', 'results', 'logs', 'profiles']:
    os.makedirs(folder, exist_ok=True)

resume_parser = resumeParser()
job_matcher = jobMatcher()

job_status = {
    'indeed_scraping': {'status': 'idle', 'progress': 0, 'message': ''},
    'linkedin_scraping': {'status': 'idle', 'progress': 0, 'message': ''},
    'connection_requests': {'status': 'idle', 'progress': 0, 'message': ''}
}

def get_recent_job_files():
    csv_files = glob.glob(os.path.join('results', '*.csv'))
    files_with_time = [(f, os.path.getmtime(f)) for f in csv_files]
    files_with_time.sort(key=lambda x: x[1], reverse=True)
    return [os.path.basename(f[0]) for f in files_with_time[:10]]

def get_user_profile():
    profile_path = os.path.join('profiles', 'user_profile.json')
    if os.path.exists(profile_path):
        try:
            with open(profile_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading profile: {e}")
    return None

def save_user_profile(profile, filename):
    profile_path = os.path.join('profiles', 'user_profile.json')
    profile_data = profile.copy()
    profile_data['resume_filename'] = filename
    profile_data['upload_date'] = datetime.now().isoformat()
    
    try:
        with open(profile_path, 'w') as f:
            json.dump(profile_data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving profile: {e}")
        return False

def save_user_profile_for_role(profile, filename, role_type):
    profiles_dir = 'profiles'
    os.makedirs(profiles_dir, exist_ok=True)
    
    profiles_file = os.path.join(profiles_dir, 'user_profiles.json')
    
    if os.path.exists(profiles_file):
        with open(profiles_file, 'r') as f:
            all_profiles = json.load(f)
    else:
        all_profiles = {}
    
    profile_data = profile.copy()
    profile_data['resume_filename'] = filename
    profile_data['role_type'] = role_type
    profile_data['upload_date'] = datetime.now().isoformat()
    
    all_profiles[role_type] = profile_data
    
    try:
        with open(profiles_file, 'w') as f:
            json.dump(all_profiles, f, indent=2)
        logger.info(f"Saved profile for role: {role_type}")
        return True
    except Exception as e:
        logger.error(f"Error saving profile: {e}")
        return False

def get_all_user_profiles():
    profiles_file = os.path.join('profiles', 'user_profiles.json')
    if os.path.exists(profiles_file):
        try:
            with open(profiles_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading profiles: {e}")
    return {}

def get_user_profile_by_role(role_type):
    all_profiles = get_all_user_profiles()
    return all_profiles.get(role_type)

def delete_user_profile_by_role(role_type):
    profiles_file = os.path.join('profiles', 'user_profiles.json')
    
    if not os.path.exists(profiles_file):
        return False
    
    try:
        with open(profiles_file, 'r') as f:
            all_profiles = json.load(f)
        
        if role_type not in all_profiles:
            return False
        
        resume_filename = all_profiles[role_type].get('resume_filename')
        if resume_filename:
            resume_path = os.path.join('uploads', resume_filename)
            if os.path.exists(resume_path):
                try:
                    os.remove(resume_path)
                except OSError as e:
                    logger.warning(f"Could not delete resume file {resume_path}: {e}")
        
        del all_profiles[role_type]
        
        with open(profiles_file, 'w') as f:
            json.dump(all_profiles, f, indent=2)
        
        logger.info(f"Deleted profile for role: {role_type}")
        return True
        
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        return False

def delete_user_profile():
    profile_path = os.path.join('profiles', 'user_profile.json')
    try:
        if os.path.exists(profile_path):
            os.remove(profile_path)
        
        upload_files = glob.glob(os.path.join('uploads', '*'))
        for file in upload_files:
            os.remove(file)
        
        return True
    except Exception as e:
        logger.error(f"Error deleting profile: {e}")
        return False


def get_user_profile():
    """Load user profile from profiles/user_profiles.json"""
    try:
        profile_path = os.path.join('profiles', 'user_profiles.json')
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    except Exception as e:
        logger.error(f"Error loading user profile: {e}")
        return None

def get_resume_text_from_profile():
    user_profile = get_user_profile()
    if not user_profile:
        return None
    
    resume_filename = user_profile.get('resume_filename')
    if not resume_filename:
        return None
    
    resume_path = os.path.join('uploads', resume_filename)
    if not os.path.exists(resume_path):
        return None
    
    try:
        return resume_parser.extract_text_from_file(resume_path)
    except Exception as e:
        logger.error(f"Error reading resume: {e}")
        return None

def run_indeed_scraper_with_matching(credentials, searches, filters=None):
    try:
        job_status['indeed_scraping']['status'] = 'running'
        job_status['indeed_scraping']['progress'] = 5
        job_status['indeed_scraping']['message'] = 'Starting Indeed scraper...'
        
        indeed_email = credentials.get('indeed_email')
        indeed_password = credentials.get('indeed_password')
        
        user_profile = get_user_profile()
        
        user_skills = None
        if user_profile and 'resume_path' in user_profile:
            try:
                resume_path = user_profile['resume_path']
                if os.path.exists(resume_path):
                    with open(resume_path, 'r', encoding='utf-8', errors='ignore') as f:
                        resume_text = f.read()
                    user_skills = extract_skills_from_text(resume_text)
                    logger.info(f"Extracted {len(user_skills)} skills from resume")
            except Exception as e:
                logger.error(f"Error extracting skills: {e}")
        
        all_jobs = []
        scraper = None
        
        job_status['indeed_scraping']['progress'] = 10
        job_status['indeed_scraping']['message'] = 'Setting up scraper...'
        
        for i, search in enumerate(searches):
            position = search.get('position')
            location = search.get('location')
            
            search_progress_base = 20 + (i / len(searches)) * 60
            job_status['indeed_scraping']['progress'] = int(search_progress_base)
            job_status['indeed_scraping']['message'] = f"Searching for {position} in {location}... ({i+1}/{len(searches)})"
            
            if scraper:
                try:
                    scraper.close()
                except:
                    pass
            
            scraper = indeedScraper(indeed_email, indeed_password, user_skills=user_skills)
            
            try:
                if not scraper.login_with_google():
                    job_status['indeed_scraping']['message'] = f"Login failed. Skipping {position}."
                    continue
                
                jobs_per_search = 50
                
                if filters is None:
                    filters = {}
                clear_previous = (i == 0)
                jobs = scraper.search_jobs_with_filters(position, location, filters, clear_previous=clear_previous)
                
                if jobs:
                    new_jobs_count = len(jobs) - (len(all_jobs) - jobs_per_search) if i > 0 else len(jobs)
                    all_jobs = jobs
                    job_status['indeed_scraping']['message'] = f"Found {new_jobs_count} new jobs for {position}, Total: {len(all_jobs)}"
                else:
                    job_status['indeed_scraping']['message'] = f"No jobs found for {position}, Total: {len(all_jobs)}"
                
                time.sleep(random.uniform(2, 4))
                job_status['indeed_scraping']['progress'] = int(search_progress_base + 30)
                
            except Exception as e:
                logger.error(f"Error during search: {e}")
                job_status['indeed_scraping']['message'] = f"Error: {str(e)}"
                continue
        
            if all_jobs:
                job_status['indeed_scraping']['message'] = 'Processing results...'
                job_status['indeed_scraping']['progress'] = 85
                
                df = pd.DataFrame(all_jobs)
                
                if user_profile:
                    job_status['indeed_scraping']['message'] = 'Calculating matches...'
                    job_status['indeed_scraping']['progress'] = 90
                    
                    description_columns = ['Description', 'Job_Description', 'description', 'job_description']
                    description_col = None
                    
                    for col in description_columns:
                        if col in df.columns:
                            description_col = col
                            break
                    
                    if description_col:
                        df = job_matcher.process_job_dataframe(df, user_profile, description_col)
                        job_status['indeed_scraping']['message'] = 'Matching done'
                    else:
                        df['overall_match'] = 0.0
                        df['skill_match'] = 0.0
                        df['experience_match'] = 0.0
                        df['text_similarity'] = 0.0
                        df['matched_skills'] = [[] for _ in range(len(df))]
                
                job_status['indeed_scraping']['message'] = 'Saving...'
                job_status['indeed_scraping']['progress'] = 95
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename_suffix = "_with_matches" if user_profile else ""
                indeed_filename = f"indeed_jobs_all{filename_suffix}_{timestamp}.csv"
                
                file_path = os.path.join('results', indeed_filename)
                df.to_csv(file_path, index=False)
                
                job_status['indeed_scraping']['message'] = f"Saved {len(all_jobs)} jobs"
            else:
                job_status['indeed_scraping']['message'] = 'No jobs found'
        
        if scraper:
            try:
                scraper.close()
            except:
                pass
        
        job_status['indeed_scraping']['status'] = 'completed'
        job_status['indeed_scraping']['progress'] = 100
        
    except Exception as e:
        logger.error(f"Error in Indeed scraper: {str(e)}")
        job_status['indeed_scraping']['status'] = 'failed'
        job_status['indeed_scraping']['message'] = f"Error: {str(e)}"
        job_status['indeed_scraping']['progress'] = 0
        
        if scraper:
            try:
                scraper.close()
            except:
                pass

def run_linkedin_scraper_with_matching(credentials, searches, filters=None):
    if filters is None:
        filters = {}
    
    scraper = None
    
    try:
        job_status['linkedin_scraping']['status'] = 'running'
        job_status['linkedin_scraping']['progress'] = 5
        job_status['linkedin_scraping']['message'] = 'Starting LinkedIn scraper...'
        
        linkedin_token = credentials.get('linkedin_token')
        
        user_profile = get_user_profile()
        
        job_status['linkedin_scraping']['message'] = 'Initializing scraper...'
        try:
            scraper = linkedinClass(linkedin_token)
        except Exception as init_error:
            logger.error(f"Failed to initialize scraper: {init_error}")
            job_status['linkedin_scraping']['status'] = 'failed'
            job_status['linkedin_scraping']['message'] = f'Failed to initialize scraper: {str(init_error)}'
            job_status['linkedin_scraping']['progress'] = 0
            return
        
        job_status['linkedin_scraping']['message'] = 'Logging in to LinkedIn...'
        job_status['linkedin_scraping']['progress'] = 10
        
        login_success = False
        max_login_attempts = 3
        
        for attempt in range(max_login_attempts):
            try:
                login_success = scraper.login_with_cookie()
                if login_success:
                    logger.info("Login successful")
                    break
                else:
                    logger.warning(f"Login attempt {attempt + 1} failed")
                    time.sleep(5)
                    
                    if attempt < max_login_attempts - 1:
                        try:
                            if scraper and scraper.driver:
                                scraper.driver.quit()
                        except:
                            pass
                        time.sleep(2)
                        scraper = linkedinClass(linkedin_token)
                        
            except Exception as login_error:
                logger.error(f"Login error: {login_error}")
                if attempt == max_login_attempts - 1:
                    job_status['linkedin_scraping']['status'] = 'failed'
                    job_status['linkedin_scraping']['message'] = f'Login failed: {str(login_error)}'
                    job_status['linkedin_scraping']['progress'] = 0
                    return
        
        if not login_success:
            job_status['linkedin_scraping']['status'] = 'failed'
            job_status['linkedin_scraping']['message'] = 'Failed to login to LinkedIn'
            job_status['linkedin_scraping']['progress'] = 0
            return
            
        job_status['linkedin_scraping']['progress'] = 20
        job_status['linkedin_scraping']['message'] = 'Login successful, starting job searches...'
        
        all_jobs = []
        max_jobs_per_search = 50
        
        for i, search in enumerate(searches):
            position = search.get('position')
            location = search.get('location')
            
            search_progress_base = 20 + (i / len(searches)) * 60
            job_status['linkedin_scraping']['progress'] = int(search_progress_base)
            job_status['linkedin_scraping']['message'] = f"Searching for {position} in {location}... ({i+1}/{len(searches)})"
            
            try:
                jobs = scraper.search_jobs(
                    keyword=position, 
                    location=location, 
                    filters=filters,
                    max_jobs_per_search=max_jobs_per_search
                )
                
                if jobs:
                    all_jobs.extend(jobs)
                    job_status['linkedin_scraping']['message'] = f"Found {len(jobs)} jobs for {position}, Total: {len(all_jobs)}"
                    logger.info(f"Found {len(jobs)} jobs")
                else:
                    job_status['linkedin_scraping']['message'] = f"No jobs found for {position}, Total: {len(all_jobs)}"
                
                job_status['linkedin_scraping']['progress'] = int(search_progress_base + 30)
                
                if i < len(searches) - 1:
                    delay = random.uniform(3, 5)
                    time.sleep(delay)
                    
            except Exception as search_error:
                logger.error(f"Error searching: {search_error}")
                job_status['linkedin_scraping']['message'] = f"Error: {str(search_error)}"
                continue
        
        if all_jobs:
            job_status['linkedin_scraping']['message'] = 'Processing results...'
            job_status['linkedin_scraping']['progress'] = 85
            
            df = pd.DataFrame(all_jobs)
            
            if user_profile:
                job_status['linkedin_scraping']['message'] = 'Calculating matches...'
                job_status['linkedin_scraping']['progress'] = 90
                
                description_columns = ['Job_Description', 'Description', 'job_description', 'description']
                description_col = None
                
                for col in description_columns:
                    if col in df.columns:
                        description_col = col
                        break
                
                if description_col:
                    try:
                        df = job_matcher.process_job_dataframe(df, user_profile, description_col)
                        job_status['linkedin_scraping']['message'] = 'Matching done'
                    except Exception as match_error:
                        logger.error(f"Error in matching: {match_error}")
                else:
                    df['overall_match'] = 0.0
                    df['skill_match'] = 0.0
                    df['experience_match'] = 0.0
                    df['text_similarity'] = 0.0
                    df['matched_skills'] = [[] for _ in range(len(df))]
            
            job_status['linkedin_scraping']['message'] = 'Saving...'
            job_status['linkedin_scraping']['progress'] = 95
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_suffix = "_with_matches" if user_profile else ""
            linkedin_filename = f"linkedin_jobs_all{filename_suffix}_{timestamp}.csv"
            
            os.makedirs('results', exist_ok=True)
            
            file_path = os.path.join('results', linkedin_filename)
            
            try:
                df.to_csv(file_path, index=False)
                job_status['linkedin_scraping']['message'] = f"Saved {len(all_jobs)} jobs"
                logger.info(f"Saved {len(all_jobs)} jobs")
            except Exception as save_error:
                logger.error(f"Error saving: {save_error}")
                job_status['linkedin_scraping']['message'] = f"Error: {str(save_error)}"
                job_status['linkedin_scraping']['status'] = 'failed'
                return
                
        else:
            job_status['linkedin_scraping']['message'] = 'No jobs found'
        
        job_status['linkedin_scraping']['status'] = 'completed'
        job_status['linkedin_scraping']['progress'] = 100
        
    except Exception as e:
        logger.error(f"Error in LinkedIn scraper: {str(e)}")
        job_status['linkedin_scraping']['status'] = 'failed'
        job_status['linkedin_scraping']['message'] = f"Error: {str(e)}"
        job_status['linkedin_scraping']['progress'] = 0
        
    finally:
        if scraper:
            try:
                if hasattr(scraper, 'driver') and scraper.driver:
                    scraper.driver.quit()
            except Exception as cleanup_error:
                logger.error(f"Cleanup error: {cleanup_error}")

def run_connection_requests(credentials, company_list, message_template):
    try:
        job_status['connection_requests']['status'] = 'running'
        job_status['connection_requests']['progress'] = 5
        job_status['connection_requests']['message'] = 'Starting LinkedIn connection bot...'
        
        linkedin_token = credentials.get('linkedin_token')
        total_connections_sent = 0
        
        # Process each company with a fresh browser instance
        for index, company in enumerate(company_list):
            bot = None
            
            search_progress_base = 20 + (index / len(company_list)) * 70
            job_status['connection_requests']['progress'] = int(search_progress_base)
            
            job_status['connection_requests']['message'] = f"Processing connection requests for {company}..."
            
            try:
                bot = linkedinConnections(linkedin_token)
                
                if not bot.login_with_cookie():
                    job_status['connection_requests']['message'] = f"Login failed for {company}"
                    continue
                    
                # Process company
                # Pass raw template; per-person formatting (with {name} and {company}) happens in the bot
                success = bot.process_company(
                    company=company, 
                    message=message_template,
                    max_connections=25,
                    max_pages=5
                )
                
                if success:
                    job_status['connection_requests']['message'] = f"Successfully processed {company}"
                    total_connections_sent += bot.total_connections_sent
                else:
                    job_status['connection_requests']['message'] = f"Failed to process {company}"
                    
            except Exception as e:
                logger.error(f"Unexpected error processing {company}: {str(e)}")
                job_status['connection_requests']['message'] = f"Error with {company}: {str(e)}"
            finally:
                # Always clean up the browser before moving to next company
                if bot:
                    bot.cleanup()
                    bot = None
                    
                # Add delay between companies
                if index < len(company_list) - 1:  # Don't delay after the last company
                    delay = random.uniform(5, 10)
                    time.sleep(delay)
            
            # Update progress
            job_status['connection_requests']['progress'] = int(search_progress_base + 70/len(company_list))
        
        # Mark task as complete
        job_status['connection_requests']['status'] = 'completed'
        job_status['connection_requests']['progress'] = 100
        job_status['connection_requests']['message'] = f"Sent a total of {total_connections_sent} connection requests"
        
    except Exception as e:
        logger.error(f"Error in connection requests: {str(e)}")
        job_status['connection_requests']['status'] = 'failed'
        job_status['connection_requests']['message'] = f"Error: {str(e)}"
        job_status['connection_requests']['progress'] = 0

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scraper')
def scraper():
    user_profile = get_user_profile()
    profile_available = user_profile is not None
    return render_template('scraper.html', profile_available=profile_available)

@app.route('/results')
def results():
    job_files = get_recent_job_files()
    return render_template('results.html', job_files=job_files)


@app.route('/profile')
def profile():
    return render_template('profile.html')
import mysql.connector
from db_config import db_manager

@app.route('/view/<filename>')
def view_file(filename):
    try:
        file_path = os.path.join('results', filename)
        if os.path.exists(file_path) and filename.endswith('.csv'):
            # SOLUCIÓN: latin-1 puede decodificar cualquier byte (0-255) sin errores
            df = pd.read_csv(file_path, encoding='latin-1')
            
            has_matches = 'overall_match' in df.columns
            
            if has_matches:
                df = df.sort_values('overall_match', ascending=False)
            
            # Select columns to display (excluding match scores)
            display_columns = ['Title', 'Company', 'Location', 'Salary', 'Job_Link', 'Experience_Category']
            
            display_columns = [col for col in display_columns if col in df.columns]
            
            display_df = df[display_columns].copy()
            
            # Make job links clickable
            if 'Job_Link' in display_df.columns:
                display_df['Job_Link'] = display_df['Job_Link'].apply(
                    lambda x: f'<a href="{x}" target="_blank" class="btn btn-sm btn-primary">Apply</a>' 
                    if pd.notna(x) and str(x).startswith('http') else 'N/A'
                )
            
            table_html = display_df.head(100).to_html(
                classes='table table-striped table-hover table-sm', 
                table_id='jobTable',
                escape=False,
                index=False
            )
            
            return render_template('view_file.html', 
                                 filename=filename, 
                                 table_html=table_html,
                                 has_matches=has_matches,
                                 total_jobs=len(df),
                                 display_columns=display_columns)
        else:
            flash('File not found or not a CSV file', 'danger')
            return redirect(url_for('results'))
    except Exception as e:
        flash(f'Error viewing file: {str(e)}', 'danger')
        return redirect(url_for('results'))

@app.route('/api/save_applications', methods=['POST'])
def api_save_applications():
    try:
        data = request.json
        filename = data.get('filename')
        applied_jobs = data.get('applied_jobs')
        total_jobs = data.get('total_jobs', 0)
        
        saved_ids = []
        companies = set()
        
        for job_data in applied_jobs.values():
            application_id = db_manager.save_application(job_data)
            if application_id:
                saved_ids.append(application_id)
                companies.add(job_data['company'])
        
        # Save file processing info
        db_manager.save_processed_file(filename, total_jobs, len(saved_ids))
        
        # Store in session for connection requests
        session['applied_companies'] = list(companies)
        
        return jsonify({
            'success': True,
            'saved': len(saved_ids),
            'companies': list(companies)
        })
        
    except Exception as e:
        logger.error(f"Error saving applications: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/connections')
def connections():
    job_files = get_recent_job_files()
    
    auto_start = request.args.get('auto_start') == 'true'
    
    companies = session.get('applied_companies', [])
    
    if not companies:
        db_companies = db_manager.get_companies_for_connections()
        companies = [c['company'] for c in db_companies]
    
    return render_template('connections.html', 
                         job_files=job_files, 
                         companies=companies,
                         empresas=session.get('companies', companies),
                         auto_start=auto_start)

@app.route('/tracker')
def tracker():
    db_manager.create_job_tracker_table()
    return render_template('job_tracker.html')

@app.route('/api/tracker/jobs')
def api_get_tracked_jobs():
    try:
        jobs = db_manager.get_all_tracked_jobs()
        return jsonify({
            'success': True,
            'jobs': jobs,
            'count': len(jobs)
        })
    except Exception as e:
        logger.error(f"Error getting tracked jobs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tracker/job', methods=['POST'])
def api_add_tracked_job():
    try:
        job_data = request.json
        
        if not job_data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        if not job_data.get('title') or not job_data.get('company'):
            return jsonify({'success': False, 'error': 'Title and Company are required'}), 400
        
        logger.info(f"Adding job to tracker: {job_data.get('title')} at {job_data.get('company')}")
        
        result = db_manager.add_job_to_tracker(job_data)
        
        if isinstance(result, dict) and result.get('exists'):
            logger.info(f"Job already exists with ID: {result['job_id']}")
            return jsonify({
                'success': False,
                'exists': True,
                'job_id': result['job_id'],
                'message': 'Job already exists in tracker'
            }), 409
        
        if result:
            logger.info(f"Successfully added job with ID: {result}")
            return jsonify({
                'success': True,
                'job_id': result,
                'message': 'Job added to tracker'
            })
        else:
            logger.error("Database returned None for job_id")
            return jsonify({'success': False, 'error': 'Database error: Failed to add job'}), 500
            
    except Exception as e:
        logger.error(f"Error adding job to tracker: {e}", exc_info=True)
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500

@app.route('/api/tracker/job/<int:job_id>')
def api_get_tracked_job(job_id):
    try:
        job = db_manager.get_tracked_job_by_id(job_id)
        
        if job:
            return jsonify({
                'success': True,
                'job': job
            })
        else:
            return jsonify({'success': False, 'error': 'Job not found'}), 404
            
    except Exception as e:
        logger.error(f"Error getting tracked job: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tracker/job/<int:job_id>/status', methods=['PUT'])
def api_update_job_status(job_id):
    try:
        data = request.json
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'success': False, 'error': 'Status is required'}), 400
        
        success = db_manager.update_job_status(job_id, new_status)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Job status updated to {new_status}'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to update status'}), 500
            
    except Exception as e:
        logger.error(f"Error updating job status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tracker/job/<int:job_id>', methods=['DELETE'])
def api_delete_tracked_job(job_id):
    try:
        success = db_manager.delete_tracked_job(job_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'Job deleted successfully'
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to delete job'}), 500
            
    except Exception as e:
        logger.error(f"Error deleting tracked job: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_applications')
def api_get_applications():
    try:
        filters = {
            'status': request.args.get('status'),
            'company': request.args.get('company')
        }
        
        applications = db_manager.get_applications(filters)
        
        return jsonify({
            'success': True,
            'applications': applications,
            'count': len(applications)
        })
        
    except Exception as e:
        logger.error(f"Error getting applications: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
@app.route('/view_profile')
def view_profile():
    user_profile = get_user_profile()
    if not user_profile:
        flash('No profile found. Please upload a resume first.', 'warning')
        return redirect(url_for('profile'))
    
    return render_template('view_profile.html', 
                         profile=user_profile, 
                         resume_filename=user_profile.get('resume_filename'))

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No file selected', 'danger')
        return redirect(url_for('profile'))
    
    file = request.files['resume']
    role_type = request.form.get('role_type')
    additional_skills = request.form.get('additional_skills', '')
    
    if not role_type:
        flash('Please select a role type', 'danger')
        return redirect(url_for('profile'))
    
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(url_for('profile'))
    
    if file:
        uploads_dir = 'uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"resume_{role_type}_{timestamp}_{file.filename}"
        filepath = os.path.join(uploads_dir, filename)
        file.save(filepath)
        
        try:
            profile = resume_parser.parse_resume(filepath)
            
            if profile:
                if additional_skills:
                    extra_skills = [s.strip() for s in additional_skills.split(',')]
                    profile['skills'].extend(extra_skills)
                    profile['skills'] = list(set(profile['skills']))
                
                if save_user_profile_for_role(profile, filename, role_type):
                    role_name = role_type.replace('_', ' ').title()
                    flash(f'✅ {role_name} resume uploaded successfully!', 'success')
                    return redirect(url_for('profile'))
                else:
                    flash('Error saving profile', 'danger')
            else:
                flash('Error parsing resume. Please check the file format.', 'danger')
                
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            flash(f'Error parsing resume: {str(e)}', 'danger')
    
    return redirect(url_for('profile'))

@app.route('/delete_profile')
def delete_profile():
    if delete_user_profile():
        flash('Profile deleted successfully', 'success')
    else:
        flash('Error deleting profile', 'danger')
    return redirect(url_for('profile'))

@app.route('/view_profile/<role_type>')
def view_profile_by_role(role_type):
    profile_data = get_user_profile_by_role(role_type)
    
    if not profile_data:
        flash(f'No profile found for {role_type.replace("_", " ").title()}', 'warning')
        return redirect(url_for('profile'))
    
    return render_template('view_profile.html', 
                         profile=profile_data, 
                         role_type=role_type,
                         resume_filename=profile_data.get('resume_filename'))

@app.route('/delete_profile/<role_type>')
def delete_profile_by_role(role_type):
    # Show confirmation page instead of deleting directly
    profile_data = get_user_profile_by_role(role_type)
    if profile_data:
        role_name = role_type.replace('_', ' ').title()
        return render_template('confirm_delete.html', role_type=role_type, role_name=role_name)
    else:
        flash('Profile not found', 'danger')
        return redirect(url_for('profile'))

@app.route('/delete_profile/<role_type>/confirm', methods=['POST'])
def confirm_delete_profile(role_type):
    if delete_user_profile_by_role(role_type):
        role_name = role_type.replace('_', ' ').title()
        flash(f'✅ {role_name} profile deleted successfully', 'success')
    else:
        flash('Error deleting profile', 'danger')
    return redirect(url_for('profile'))

@app.route('/api/all_profiles')
def api_all_profiles():
    profiles = get_all_user_profiles()
    return jsonify({
        'success': True,
        'profiles': profiles,
        'count': len(profiles)
    })

@app.route('/api/profile_summary')
def api_profile_summary():
    user_profile = get_user_profile()
    if not user_profile:
        return jsonify({'error': 'No profile found'}), 404
    
    return jsonify({
        'skills_count': len(user_profile.get('skills', [])),
        'experience_years': user_profile.get('experience_years', 0),
        'education_count': len(user_profile.get('education', [])),
        'upload_date': user_profile.get('upload_date')
    })

@app.route('/debug/directories')
def debug_directories():
    directories = {
        'uploads': os.path.exists('uploads'),
        'results': os.path.exists('results'),
        'logs': os.path.exists('logs'),
        'profiles': os.path.exists('profiles'),
        'temp': os.path.exists('temp'),
        'temp/resumes': os.path.exists('temp/resumes')
    }
    
    # Try to create directories if they don't exist
    for dir_path in ['uploads', 'results', 'logs', 'profiles', 'temp', 'temp/resumes']:
        try:
            os.makedirs(dir_path, exist_ok=True)
            directories[dir_path] = True
        except Exception as e:
            directories[dir_path] = f"Error: {str(e)}"
    
    return jsonify({
        'directories': directories,
        'current_working_dir': os.getcwd(),
        'message': 'Directory status checked and created if needed'
    })

@app.route('/status')
def status():
    return jsonify(job_status)

@app.route('/results/<filename>')
def download_file(filename):
    return send_from_directory('results', filename, as_attachment=True)


@app.route('/download_csv/<filename>')
def download_csv_file(filename):
    try:
        file_path = os.path.join('results', filename)
        if os.path.exists(file_path) and filename.endswith('.csv'):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            flash('File not found or not a CSV file', 'danger')
            return redirect(url_for('results'))
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('results'))

@app.route('/extract_companies/<filename>')
def extract_companies_from_file(filename):
    try:
        file_path = os.path.join('results', filename)
        if os.path.exists(file_path) and filename.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='latin-1')
            
            # Extract companies
            companies = set()
            if 'Company' in df.columns:
                for company in df['Company'].dropna().unique():
                    # Clean company name - remove Inc., Corp., etc.
                    company_name = company.split(',')[0].split('Inc.')[0].split('Corp.')[0].strip()
                    if company_name and len(company_name) > 1:  # Ensure not empty
                        companies.add(company_name)
            
            # Filter out very common companies that might be too broad
            common_companies = ['amazon', 'google', 'microsoft', 'apple', 'facebook', 'meta']
            filtered_companies = [
                company for company in companies 
                if company.lower() not in common_companies
            ]
            
            # Limit to top 20 and sort alphabetically
            top_companies = sorted(filtered_companies)[:20]
            
            # Store in session
            session['companies'] = top_companies
            
            flash(f'Extracted {len(top_companies)} companies', 'success')
            return redirect(url_for('connections'))
        else:
            flash('File not found or not a CSV file', 'danger')
            return redirect(url_for('results'))
    except Exception as e:
        flash(f'Error extracting companies: {str(e)}', 'danger')
        return redirect(url_for('results'))


@app.route('/start_indeed_scraper', methods=['POST'])
def start_indeed_scraper():
    indeed_email = request.form.get('indeed_email')
    indeed_password = request.form.get('indeed_password')
    
    searches = []
    positions = request.form.getlist('position[]')
    locations = request.form.getlist('location[]')
    
    for i in range(len(positions)):
        if positions[i] and locations[i]:
            searches.append({
                'position': positions[i],
                'location': locations[i]
            })
    
    filters = {
        'salary_range': request.form.get('salary_range', ''),
        'remote_work': request.form.get('remote_work', ''),
        'experience_level': request.form.get('experience_level', ''),
        'education_level': request.form.get('education_level', ''),
        'date_posted': request.form.get('date_posted', '')
    }
    
    if not indeed_email or not indeed_password:
        flash('Please provide Indeed email and password', 'danger')
        return redirect(url_for('scraper'))
        
    if not searches:
        flash('Please provide at least one valid search', 'danger')
        return redirect(url_for('scraper'))
    
    job_status['indeed_scraping'] = {
        'status': 'idle', 
        'progress': 0, 
        'message': 'Starting...'
    }
    
    thread = threading.Thread(
        target=run_indeed_scraper_with_matching,
        args=({
            'indeed_email': indeed_email,
            'indeed_password': indeed_password
        }, searches, filters)
    )
    thread.daemon = True
    thread.start()
    
    flash('Indeed scraper started', 'success')
    return redirect(url_for('scraper'))

@app.route('/start_linkedin_scraper', methods=['POST'])
def start_linkedin_scraper():
    linkedin_token = request.form.get('linkedin_token')
    
    searches = []
    positions = request.form.getlist('position[]')
    locations = request.form.getlist('location[]')
    
    for i in range(len(positions)):
        if positions[i] and locations[i]:
            searches.append({
                'position': positions[i],
                'location': locations[i]
            })
    
    filters = {
        'sort_by': request.form.get('sort_by', ''),
        'date_posted': request.form.get('date_posted', ''),
        'job_type': request.form.getlist('job_type[]'),
        'experience_level': request.form.get('experience_level', ''),
        'remote_work': request.form.get('remote_work', ''),
        'salary_range': request.form.get('salary_range', ''),
        'has_verifications': request.form.get('has_verifications', 'true') == 'true'
    }
    
    if not linkedin_token:
        flash('Please provide LinkedIn authentication token', 'danger')
        return redirect(url_for('scraper'))
        
    if not searches:
        flash('Please provide at least one valid search', 'danger')
        return redirect(url_for('scraper'))
    
    job_status['linkedin_scraping'] = {
        'status': 'idle', 
        'progress': 0, 
        'message': 'Starting...'
    }
    
    thread = threading.Thread(
        target=run_linkedin_scraper_with_matching,
        args=({
            'linkedin_token': linkedin_token
        }, searches, filters)
    )
    thread.daemon = True
    thread.start()
    
    flash('LinkedIn scraper started', 'success')
    return redirect(url_for('scraper'))


@app.route('/start_connection_requests', methods=['POST'])
def start_connection_requests():
    linkedin_token = request.form.get('linkedin_token')
    company_list = request.form.getlist('company_selection')
    message_template = request.form.get('message_template', '')
    
    if not linkedin_token:
        flash('Please provide LinkedIn authentication token', 'danger')
        return redirect(url_for('connections'))
        
    if not company_list:
        flash('Please select at least one company', 'danger')
        return redirect(url_for('connections'))
    
    job_status['connection_requests'] = {
        'status': 'idle', 
        'progress': 0, 
        'message': 'Starting...'
    }
    
    thread = threading.Thread(
        target=run_connection_requests,
        args=({
            'linkedin_token': linkedin_token
        }, company_list, message_template)
    )
    thread.daemon = True
    thread.start()
    
    flash('Connection requests started', 'success')
    return redirect(url_for('connections'))

@app.route('/download_resume/<filename>')
def download_resume(filename):
    try:
        # Check in cover_letters directory first
        cover_letters_dir = os.path.join('temp', 'cover_letters')
        if os.path.exists(os.path.join(cover_letters_dir, filename)):
            mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            return send_from_directory(
                cover_letters_dir, 
                filename, 
                as_attachment=True, 
                download_name=filename,
                mimetype=mimetype
            )
        
        # Fallback to resumes directory
        resume_dir = os.path.join('temp', 'resumes')
        mimetype = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        return send_from_directory(
            resume_dir, 
            filename, 
            as_attachment=True, 
            download_name=filename,
            mimetype=mimetype
        )
    except Exception as e:
        flash(f'Error downloading resume: {str(e)}', 'danger')
        return redirect(url_for('results'))

@app.route('/delete_csv/<filename>')
def delete_csv(filename):
    try:
        results_dir = 'results'
        filepath = os.path.join(results_dir, filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            flash(f'File {filename} deleted successfully!', 'success')
        else:
            flash(f'File {filename} not found!', 'warning')
        
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'danger')
        return redirect(url_for('index'))

@app.route('/batch_cover_letters')
def batch_cover_letters():
    try:
        results_dir = 'results'
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)
        
        job_files = [f for f in os.listdir(results_dir) if f.endswith('.csv')]
        job_files.sort(reverse=True)
        
        return render_template('batch_cover_letters.html', job_files=job_files)
    except Exception as e:
        logger.error(f"Error loading batch cover letters page: {e}")
        flash('Error loading page', 'danger')
        return redirect(url_for('index'))

@app.route('/api/batch_cover_letters', methods=['POST'])
def api_batch_cover_letters():
    try:
        data = request.json
        filename = data.get('filename')
        num_jobs = int(data.get('num_jobs', 5))
        
        if not filename:
            return jsonify({'success': False, 'error': 'Filename is required'}), 400
        
        resume_text = get_resume_text_from_profile()
        if not resume_text:
            return jsonify({'success': False, 'error': 'Please upload your resume first'}), 400
        
        file_path = os.path.join('results', filename)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        df = pd.read_csv(file_path, encoding='latin-1')
        
        description_col = None
        for col in ['Job_Description', 'Description', 'job_description', 'description']:
            if col in df.columns:
                description_col = col
                break
        
        if not description_col:
            return jsonify({'success': False, 'error': 'No job description column found'}), 400
        
        generator = CoverLetterGenerator()
        results = []
        
        jobs_to_process = df.head(num_jobs)
        
        for index, row in jobs_to_process.iterrows():
            try:
                job_title = row.get('Title', 'Unknown Position')
                company = row.get('Company', 'Unknown Company')
                job_description = str(row.get(description_col, ''))
                
                if not job_description or job_description == 'nan':
                    continue
                
                cover_letter = generator.generate_cover_letter(resume_text, job_description, job_title, company)
                saved_filename = generator.save_cover_letter(cover_letter, job_title, company)
                
                results.append({
                    'job_title': job_title,
                    'company': company,
                    'filename': saved_filename,
                    'status': 'success'
                })
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error generating cover letter for job {index}: {e}")
                results.append({
                    'job_title': row.get('Title', 'Unknown'),
                    'company': row.get('Company', 'Unknown'),
                    'filename': None,
                    'status': 'failed',
                    'error': str(e)
                })
        
        successful = sum(1 for r in results if r['status'] == 'success')
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': successful
        })
        
    except Exception as e:
        logger.error(f"Error in batch cover letter generation: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/optimize_resume')
def optimize_resume_page():
    return render_template('optimize_resume.html')

@app.route('/optimize_resume', methods=['POST'])
def optimize_resume():
    try:
        job_title = request.form.get('job_title', '')
        company = request.form.get('company', '')
        job_description = request.form.get('job_description', '')
        resume_text = request.form.get('resume_text', '')
        
        if not job_description:
            flash('Job description is required', 'danger')
            return redirect(url_for('optimize_resume_page'))
        
        if not resume_text:
            resume_text = get_resume_text_from_profile()
            if not resume_text:
                flash('Please provide resume text or upload your resume first', 'warning')
                return redirect(url_for('optimize_resume_page'))
        
        optimizer = simpleResumeOptimizer()
        optimized_resume = optimizer.optimize_resume(resume_text, job_description, job_title, company)
        
        filename = optimizer.save_resume(optimized_resume, job_title, company)
        
        return render_template('optimize_resume.html', 
                             optimized_resume=optimized_resume,
                             filename=filename,
                             job_title=job_title,
                             company=company)
        
    except Exception as e:
        logger.error(f"Error optimizing resume: {e}")
        flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('optimize_resume_page'))

@app.route('/api/optimize_resume', methods=['POST'])
def api_optimize_resume():
    try:
        data = request.json
        job_title = data.get('job_title', '')
        company = data.get('company', '')
        job_description = data.get('job_description', '')
        
        if not job_description:
            return jsonify({'success': False, 'error': 'Job description is required'}), 400
        
        resume_text = get_resume_text_from_profile()
        if not resume_text:
            return jsonify({'success': False, 'error': 'Please upload your resume first'}), 400
        
        optimizer = simpleResumeOptimizer()
        optimized_resume = optimizer.optimize_resume(resume_text, job_description, job_title, company)
        
        filename = optimizer.save_resume(optimized_resume, job_title, company)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'resume_text': optimized_resume
        })
        
    except Exception as e:
        logger.error(f"Error optimizing resume: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/batch_optimize')
def batch_optimize_page():
    job_files = get_recent_job_files()
    return render_template('batch_optimize.html', job_files=job_files)

@app.route('/api/batch_optimize', methods=['POST'])
def api_batch_optimize():
    try:
        data = request.json
        filename = data.get('filename')
        num_jobs = int(data.get('num_jobs', 5))
        
        if not filename:
            return jsonify({'success': False, 'error': 'Filename is required'}), 400
        
        resume_text = get_resume_text_from_profile()
        if not resume_text:
            return jsonify({'success': False, 'error': 'Please upload your resume first'}), 400
        
        file_path = os.path.join('results', filename)
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        df = pd.read_csv(file_path, encoding='latin-1')
        
        description_col = None
        for col in ['Job_Description', 'Description', 'job_description', 'description']:
            if col in df.columns:
                description_col = col
                break
        
        if not description_col:
            return jsonify({'success': False, 'error': 'No job description column found'}), 400
        
        optimizer = simpleResumeOptimizer()
        results = []
        
        jobs_to_process = df.head(num_jobs)
        
        for index, row in jobs_to_process.iterrows():
            try:
                job_title = row.get('Title', 'Unknown Position')
                company = row.get('Company', 'Unknown Company')
                job_description = str(row.get(description_col, ''))
                
                if not job_description or job_description == 'nan':
                    continue
                
                optimized_resume = optimizer.optimize_resume(resume_text, job_description, job_title, company)
                saved_filename = optimizer.save_resume(optimized_resume, job_title, company)
                
                results.append({
                    'job_title': job_title,
                    'company': company,
                    'filename': saved_filename,
                    'status': 'success'
                })
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"Error optimizing for job {index}: {e}")
                results.append({
                    'job_title': row.get('Title', 'Unknown'),
                    'company': row.get('Company', 'Unknown'),
                    'filename': None,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': len([r for r in results if r['status'] == 'success'])
        })
        
    except Exception as e:
        logger.error(f"Error in batch optimization: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
