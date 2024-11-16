import mailbox 
import pandas as pd

#From https://stackoverflow.com/questions/26567843/reading-the-mail-content-of-an-mbox-file-using-python-mailbox.
def getbody(message): #getting plain text 'email body'
    body = None
    if message.is_multipart():
        for part in message.walk():
            if part.is_multipart():
                for subpart in part.walk():
                    if subpart.get_content_type() == 'text/plain':
                        body = subpart.get_payload(decode=True)
            elif part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
    elif message.get_content_type() == 'text/plain':
        body = message.get_payload(decode=True)
    return body

def getbookinfo(body):
    title = str(body).split("<li>")
    editor_mail_line = title[2]
    press_name = title[1]
    submission_info = title[3].split("</li>")[0]
    table = title[3]
    if "|" in table:
        table_unfucked = table.split("<br>")[2].split("|")[1]
    else:
        table_unfucked = table.split(">")[23].split("<")[0]
    return {"editor_email" : [editor_mail_line], 
            "press_name" : [press_name],
            "submission_info" : [submission_info],
            "title" : [table_unfucked]}
    
out_df = pd.DataFrame()
all_mails = mailbox.mbox("spbox.mbox")
for message in all_mails:
    if "SmallPitch Team" in message['from']:
        body = getbody(message)
        bookinfo = getbookinfo(body)
        bt_df = pd.DataFrame(data = bookinfo)
        out_df = pd.concat([out_df, bt_df])
with open("emails.csv", "w+") as emails:
    out_df.to_csv(emails, index=False, lineterminator="\n")
