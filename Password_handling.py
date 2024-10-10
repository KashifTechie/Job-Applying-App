class Password_:
    def __init__(self,Password):
        self.Password = Password
    def password_handling(self):
        if len(self.Password)>=8:
                #def password_verification(str,n):
                if self.Password[0].isdigit():
                    return '<h1>First character should not be an Integer</h1>'
                cap = 0
                num = 0
                special_char=0
                for i in self.Password:
                    if 'A'<= i <= 'Z':
                        cap+=1
                    if '0' <= i <= '9':
                        num+=1   
                    if  not('A'<= i <= 'Z') and not('0' <= i <= '9') and not('a'<=i<='z'):
                        special_char+=1  
                        
                print(f'cap: {cap}\nnum: {num}\nspecial_char: {special_char}')        
                if cap >0 and num>0 and special_char>0:
                    return 1
                elif cap ==0 and num==0 and special_char==0:
                    return '<h1>Pasword should atleast contain 1 Special character, 1 Uppercase character and 1 integer character</h1>'
                elif cap >0 and num==0 and special_char==0:
                    return '<h1>Pasword should atleast contain 1 Special characterand 1 integer character</h1>'
                elif cap ==0 and num>0 and special_char==0:    
                    return '<h1>Pasword should atleast contain 1 Special character and 1 Upper Case</h1>'
                elif cap ==0 and num==0 and special_char>0:    
                    return '<h1>Pasword should atleast contain  1 Uppercase character and 1 integer character</h1>'
                elif cap>0 and num>0 and special_char==0:
                    return '<h1>Pasword should atleast contain 1 Special character</h1>'
                elif cap >0 and num==0 and special_char>0:
                    return '<h1>Pasword should atleast contain 1 Integer character</h1>'
                elif cap ==0 and num>0 and special_char>0:
                    return '<h1>Pasword should atleast contain 1 Uppercase character</h1>'
        else:
            return '<h1>Pasword should atleast contain 8 characters</h1>'