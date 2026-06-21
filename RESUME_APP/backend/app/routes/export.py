from flask import Blueprint, request, jsonify, send_file
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io
from datetime import datetime

bp = Blueprint('export', __name__, url_prefix='/api')

@bp.route('/export-report', methods=['POST'])
def export_report():
    """Export analysis report as PDF."""
    data = request.get_json()
    report_type = data.get('type', 'pdf')  # 'pdf' or 'text'
    content = data.get('content', {})
    
    try:
        if report_type == 'pdf':
            # Generate PDF
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            
            # Title
            c.setFont("Helvetica-Bold", 16)
            c.drawString(1*inch, height - 1*inch, "Resume Analysis Report")
            
            # Date
            c.setFont("Helvetica", 10)
            c.drawString(1*inch, height - 1.2*inch, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Content
            y = height - 1.5*inch
            c.setFont("Helvetica", 12)
            
            if 'match_result' in content:
                match = content['match_result']
                c.drawString(1*inch, y, f"Match Percentage: {match.get('match_percentage', 0)}%")
                y -= 0.3*inch
                c.drawString(1*inch, y, f"Matching Skills: {len(match.get('matching_skills', []))}")
                y -= 0.3*inch
                c.drawString(1*inch, y, f"Missing Skills: {len(match.get('missing_skills', []))}")
                y -= 0.5*inch
            
            if 'suggestions' in content:
                c.setFont("Helvetica-Bold", 12)
                c.drawString(1*inch, y, "Suggestions:")
                y -= 0.3*inch
                c.setFont("Helvetica", 10)
                for suggestion in content['suggestions'][:5]:
                    c.drawString(1.2*inch, y, f"- {suggestion.get('title', '')}")
                    y -= 0.25*inch
                    if y < 1*inch:
                        c.showPage()
                        y = height - 1*inch
            
            c.save()
            buffer.seek(0)
            
            return send_file(
                buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name='resume_analysis_report.pdf'
            )
        
        else:
            # Generate text report
            report_text = "RESUME ANALYSIS REPORT\n"
            report_text += "=" * 50 + "\n\n"
            report_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            
            if 'match_result' in content:
                match = content['match_result']
                report_text += f"Match Percentage: {match.get('match_percentage', 0)}%\n"
                report_text += f"Matching Skills: {len(match.get('matching_skills', []))}\n"
                report_text += f"Missing Skills: {len(match.get('missing_skills', []))}\n\n"
            
            if 'suggestions' in content:
                report_text += "SUGGESTIONS:\n"
                for suggestion in content['suggestions']:
                    report_text += f"- {suggestion.get('title', '')}: {suggestion.get('description', '')}\n"
            
            return jsonify({
                'success': True,
                'report': report_text,
                'type': 'text'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

