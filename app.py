
from dotenv import load_dotenv
from gmail_oauth.gmail_oauth import get_gmail_service
from llm_email_labeller.llm_caller import llm_caller

load_dotenv()


def main():
    gmail_service = get_gmail_service()
    print("Successfully connected to Gmail API!")

    # Example: List the last 1 messages in the inbox
    results = gmail_service.users().messages().list(userId='me',q="is:unread in:inbox newer_than:2d").execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        llm_caller(gmail_service,messages)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")