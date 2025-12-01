from langgraph_email_classifier.langgraph_email_labeller import mail_classifier

def add_labels_gmail(gmail_service,result,mailid):
    new_label=result.get("mailtype","No Label")
    labels_list = gmail_service.users().labels().list(userId='me').execute()
    labels = labels_list.get('labels', [])
    final_label_list=[{"id":label["id"],"name":label["name"]} for label in labels]
    final_label_info = [{"id": label['id'], "name": label['name']} for label in final_label_list if label.get('name') == new_label]

    try:
    # Define the request body to remove the 'UNREAD' label
        modify_request = {
        'removeLabelIds': ['INBOX'],
        'addLabelIds': [final_label_info[0]['id']]
    }

    # Execute the modify API call
        gmail_service.users().messages().modify(userId='me', id=mailid, body=modify_request).execute()

        return (f"Successfully labelled the mail with label:")
        
    except Exception as e:
        return (f"ERROR labelling the message {mailid}: {e}")

def llm_caller(gmail_service,messages):

    def extract_subject():
        msg_header=msg.get("payload",{}).get("headers",[])
        subject = next((header for header in msg_header if header.get("name")=="Subject"),None)
        return subject.get("value","No Subject")

    for message in messages:
        msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        full_message_list=[{"id":m["id"],"email_body":m["snippet"],"Subject":extract_subject(),"labelIds":m["labelIds"]} for m in [msg] if 'UNREAD' in m.get("labelIds",[])]
        workflow=mail_classifier()
        mailid=[ item['id'] for item in full_message_list]
        mailid=mailid[0]
        email_body=[ item['email_body'] for item in full_message_list]
        email_body=email_body[0]
        email_subject=[ item['Subject'] for item in full_message_list]
        email_subject=email_subject[0]
        result=workflow.invoke({"email_body":email_body,"email_subject":email_subject})
        label_result=add_labels_gmail(gmail_service,result,mailid)

        print(f'For the email: "{result['email_subject']}", {label_result}{result['mailtype']}')