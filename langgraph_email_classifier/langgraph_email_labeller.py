from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Literal, TypedDict
from dotenv import load_dotenv

load_dotenv()

structured_llm=ChatOpenAI(model="gpt-4o-mini")

def mail_classifier():
    class MAILClassifier(BaseModel):
        mailtype:Literal["Demo","Test","Job","SPAM","Education","Payments"]=Field( description="Email type based on the subject and body of email.")


    class MAILSTATE(TypedDict):
        email_body:str
        email_subject:str
        mailtype: str
        
    structured_output=  structured_llm.with_structured_output(MAILClassifier)

    def classify_email_node(state:MAILSTATE)->MAILSTATE:

        prompt=PromptTemplate(template=
                ("""You are a helpful mail classifier. 
                    Your job is to classify the mail based on email body and subject.
                
                    Also, update the mailtype as based on what the subject and email_body are:
                    ["Demo","Test","Job","Spam","Education","Payments"]

                    If you feel mail has ambiguity mark mailtype "Spam" specifically.
                    Use your intuition to make it more robust. 
                
                    mailtype: "Demo" will be if someone is requesting for demo sessions, video calls.
                    mailtype: "Test" will be if I have sent some test messages to test
                    mailtype: "Job" Will be job related enquiry.
                    mailtype: "Education" Will be education if someone is pursuing for upskills programs
                    mailtype: "Payments" will be credit card bill payments, transaction related to bank
                    mailtype: "SPAM" will be Spam based if its none of above category.

                    Do all these task for the mail subject:{email_subject}\n\n
                    Email Body is as follow: \n\n {email_body}
                    """), 
                    input_variables=["email_subject","email_body"])
        
        chain  = prompt | structured_output

        response=chain.invoke({"email_subject":state['email_subject'],"email_body":state['email_body']})
        return { "mailtype":response.mailtype}

    graph=StateGraph(MAILSTATE)
    graph.add_node("classify_email_node",classify_email_node)
    graph.add_edge(START,"classify_email_node")
    graph.add_edge("classify_email_node",END)
    workflow=graph.compile()

    return workflow