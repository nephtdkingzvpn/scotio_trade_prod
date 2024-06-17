# email_utils.py
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_html_email(subject, template_name, context):
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)  # Fallback for email clients that don't support HTML

    email = EmailMessage(
        subject,
        text_content,
        'your_email@gmail.com',  # Replace with your "from" email address
        ['nephgthk@gmail.com'],
    )
    email.content_subtype = "html"  # Main content is text/html
    email.send()
