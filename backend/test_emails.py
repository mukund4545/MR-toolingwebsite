import asyncio
import resend
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
resend.api_key = os.environ.get('RESEND_API_KEY')

async def test_emails():
    emails = ['mukundprajapati2408@gmail.com', 'mrtooling@hotmail.com']

    for email in emails:
        try:
            params = {
                'from': os.environ.get('SENDER_EMAIL', 'onboarding@resend.dev'),
                'to': [email],
                'subject': f'Test Email to {email}',
                'html': f'<p>This is a test email sent to {email} from MR Tooling Industries website.</p><p>Timestamp: {datetime.now()}</p>'
            }

            result = resend.Emails.send(params)
            print(f'✅ Email sent successfully to {email}')
            print(f'   Email ID: {result.get("id", "N/A")}')
        except Exception as e:
            print(f'❌ Failed to send to {email}: {str(e)}')
        print()

if __name__ == "__main__":
    asyncio.run(test_emails())