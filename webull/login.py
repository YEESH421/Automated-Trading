from webull import webull


email = ''
pswrd = ''
mfaCode = ''
qId = ''
qAns = '' 

wb = webull()


print(wb.login(email, pswrd, 'laptop', mfaCode, qId, qAns))
