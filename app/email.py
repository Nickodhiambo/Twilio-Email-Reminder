import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_reminder_email(user_email, task_title, task_due_date):
    message = Mail(
        from_email = 'nodhiambo@gmail.com',
        to_emails = user_email,
        subject = 'Reminder: Task due soon',
        html_content = f'<strong> Your task {task_title} is due on {task_due_date}'
    )
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(f'Error sending mail: {str(e)}')