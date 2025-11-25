import os
import logging
from datetime import datetime
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoverLetterGenerator:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            # Use gemini-2.5-flash which is available and fast
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("Gemini 2.5 Flash model loaded successfully")
        except ImportError:
            logger.error("google-generativeai package not installed")
            raise
        except Exception as e:
            logger.error(f"Error initializing Gemini API: {e}")
            raise
    
    def generate_cover_letter(self, resume_text: str, job_description: str, job_title: str = "", company: str = "") -> str:
        """Generate a personalized cover letter using Gemini AI"""
        
        prompt = f"""Sos un experto en recursos humanos y redacción profesional. Tu tarea es crear una carta de presentación personalizada y profesional en español.

INFORMACIÓN DEL CANDIDATO (de su CV):
{resume_text[:3000]}

INFORMACIÓN DEL TRABAJO:
Puesto: {job_title}
Empresa: {company}
Descripción del trabajo:
{job_description[:2000]}

INSTRUCCIONES:
1. Creá una carta de presentación profesional en español de Argentina
2. La carta debe tener aproximadamente 300-400 palabras
3. Usá un tono profesional pero cercano
4. Estructura:
   - Fecha (usar formato: Buenos Aires, [fecha actual])
   - Saludo personalizado (si es posible, sino "Estimado/a equipo de {company}")
   - Párrafo 1: Por qué te interesa este puesto y la empresa
   - Párrafo 2: Tu experiencia relevante que calza con los requisitos
   - Párrafo 3: Qué valor podés aportar a la empresa
   - Cierre: Agradecimiento y disponibilidad para entrevista
   - Despedida formal

5. NO incluyas datos de contacto ficticios (dirección, teléfono, email)
6. Enfocate en las habilidades y experiencias del CV que sean relevantes para este puesto
7. Mencioná tecnologías o herramientas específicas que coincidan entre el CV y el job description
8. Sé específico sobre por qué este puesto en particular te interesa

IMPORTANTE: Devolvé SOLO el texto de la carta, sin formato markdown, sin títulos adicionales, sin explicaciones. La carta debe estar lista para copiar y pegar en un documento Word.
"""
        
        try:
            response = self.model.generate_content(prompt)
            cover_letter = response.text.strip()
            
            # Clean up any markdown formatting that might have slipped through
            cover_letter = cover_letter.replace('**', '')
            cover_letter = cover_letter.replace('*', '')
            cover_letter = cover_letter.replace('#', '')
            
            logger.info(f"Cover letter generated successfully for {job_title} at {company}")
            return cover_letter
            
        except Exception as e:
            logger.error(f"Error generating cover letter: {e}")
            raise Exception(f"Failed to generate cover letter: {str(e)}")
    
    def save_cover_letter(self, letter_text: str, job_title: str, company: str, output_dir: str = "temp/cover_letters") -> str:
        """Save cover letter as a formatted DOCX file"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_title = "".join(c for c in job_title if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
        safe_company = "".join(c for c in company if c.isalnum() or c in (' ', '-', '_')).strip()[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"cover_letter_{safe_title}_{safe_company}_{timestamp}.docx"
        filename = filename.replace(" ", "_")
        filepath = os.path.join(output_dir, filename)
        
        # Create Word document
        doc = Document()
        
        # Set margins (1 inch all around)
        sections = doc.sections
        for section in sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)
        
        # Split letter into paragraphs
        paragraphs = letter_text.split('\n\n')
        
        for para_text in paragraphs:
            para_text = para_text.strip()
            if not para_text:
                continue
            
            # Add paragraph
            p = doc.add_paragraph(para_text)
            
            # Format paragraph
            p_format = p.paragraph_format
            p_format.line_spacing = 1.15
            p_format.space_after = Pt(10)
            
            # Set font
            for run in p.runs:
                run.font.name = 'Calibri'
                run.font.size = Pt(11)
        
        # Save document
        doc.save(filepath)
        logger.info(f"Cover letter saved to {filepath}")
        
        return filename
    
    def generate_and_save(self, resume_text: str, job_description: str, job_title: str, company: str) -> str:
        """Generate and save cover letter in one step"""
        
        letter_text = self.generate_cover_letter(resume_text, job_description, job_title, company)
        filename = self.save_cover_letter(letter_text, job_title, company)
        
        return filename
