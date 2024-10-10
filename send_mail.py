class SEND_MAIL:
    def __init__(self, subject, message, reciever):
        self.__subject = subject
        self.__message = message
        self.__reciever = reciever
    def send(self):
        import smtplib 
        
        text = f"Subject: {self.__subject}\n\n{self.__message}"
              
        server = smtplib.SMTP('smtp.gmail.com',587) 
        server.starttls() 
        server.login('kkmd865@gmail.com','pkwp swlv mjwk lzbj') 
        server.sendmail('kkmd865@gmail.com', self.__reciever,text) 
        print('message sent')
    