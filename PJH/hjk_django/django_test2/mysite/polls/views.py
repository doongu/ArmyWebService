from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

#토큰 메서드
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
import jwt
from django.conf import settings
SECRET_KEY = getattr(settings, 'SECRET_KEY', None)
ALGORITHM = getattr(settings, 'ALGORITHM', None)
#from settings.py import SECRET_KEY, ALGORITHM
# from .tokens import account_activation_token



#메인 페이지를 처음 들어올 때
def Main_page(request):
    if request.method == 'GET':
        return render(request, 'polls/Main_page.html')


#회원가입 logic
def Signup(request):
    def mak_token(data):
        return data['id'] +"asdasd" + data['pw']
    if request.method=="POST":
        data = request.POST
        signUpId = data["signUpId"] #이메일
        signUpPw = data["signUpPw"]
        signUpPw_check = data["signUpPw_check"]
        signUpBirthYear = data["signUpBirthYear"]

        #이메일 인증 할 사용자 생성
       

        data = {
            'id': signUpId,
            'pw': signUpPw
        }
        token = jwt.encode(data, SECRET_KEY, ALGORITHM)
        #이메일 인증
        context = {
            #'title' : "제목",
            'email' : signUpId,
            #'message' : "안녕하세요"
            'token' : token
        }
        emailContent = render_to_string('polls/email.html', context)
        email = EmailMessage("온실 속 돌멩이 인증메일입니다.", emailContent, to = [signUpId])
        email.content_subtype = "html"
        result = email.send()      

        #이메일이 성공적으로 발송되면 
        #의문, 이메일이 뭐든 간에 항상 1값이 전해진다.
        if result == 1:
            #messages.info(request, "성공적으로 보냈습니다.")
            return render(request, 'polls/Main_page.html', {"result" : result, "signUpId" : signUpId })
        
        #안가면
        # 여러 갈래 나눠서  
        else:
            return render(request, 'polls/Main_page.html', {"result" : result, "signUpId" : signUpId})
    else:
        return render(request, 'polls/Main_page.html')

def email_activate(request, token):
    token_str = token.decode('utf-8')
    payload = jwt.decode(token_str, SECRET_KEY, ALGORITHM)

    if payload['id'] == "must1080@naver.com":
        return render(request, 'polls/error.html',{"error" : payload['id']} )
#계정 활성화 함수(토큰을 이용해 인증)
# def email_activate(request, uid64, token):
#         try:
#             uid = force_text(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
#             user = None
#         if user is not None and account_activation_token.check_token(user, token):
#             data = decode_token(token)
#             User.objects.create(id=data['id'])
#             user.is_active = True
#             user.save()
#             auth.login(request, user)
#             return render(request, 'polls/Main_page.html') #redirect
#         else: 
#             return render(request, 'polls/error.html', {'error' : '계정 활성화 오류'})

#로그인 -> 채팅화면 전환 views
def Chat_page(request):
    if request.method=="POST":
        login_data = request.POST
        login_id = login_data["login_id"]
        login_pw = login_data["login_pw"]

        return render(request, 'polls/Chat_page.html')
        
        #db 조회

        #if login_id 와 pw 가 맞으면 
            #return render(request, 'polls/Chat_page.html')

        #if db에 로그인 정보가 없으면
            #No_Id = "아이디가 존재하지 않거나 비밀번호가 잘못 되었습니다."
            #return render(request, 'polls/Main_page.html', {"No_Id": No_Id})
