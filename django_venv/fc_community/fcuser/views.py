from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from .models import Fcuser
from .forms import LoginForm
# Create your views here.


def home(request):
    return render(request, 'home.html')


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

        return redirect('/')


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():  # 검증
            # 폼에 데이터를 넣고 정상 검증을 하고 정상이면 세션코드가 들어감
            # 검증에 성공했으면 redirect로 홈으로 이동한다.
            request.session['user'] = form.user_id
            return redirect('/')
    else:  # POST 방식이 아닐때는 (GET) 일반 입력폼을 띄운다.
        form = LoginForm()
    return render(request, 'login.html', {"form": form})
    # render > html 화면을 렌더링해주고 딕셔너리 또는 다른 변수들을 넣어서
    # 템플릿에 전달한다.


def register(request):
    # views에서 로직을 만들때 메서드에 request를 무조건 받게 되있다.
    # request로 요청을 하기 때문에

    # 템플릿에서 form 요청 방식이 GET 이거나 POST일때
    # form 데이터를 전달하게된다.
    if request.method == 'GET':
        return render(request, 'register.html')
    elif request.method == 'POST':
        # POST로 요청할때 form 안에 있는 데이터를 받아 올 수 있도록
        # 각 input의 name 값을 입력해준다 .
        # 즉 name = key 값이 되는것이다.
        username = request.POST.get('username', None)
        useremail = request.POST.get('useremail', None)
        password = request.POST.get('password', None)
        re_password = request.POST.get('re-password', None)

        # key 값을 받아 왔으니 넘어갈 데이터를 받아줄 클래스 모델을 가져온다.
        # Models 에서 가져온 클래스(테이블) Fcuser의 클래스 변수에
        # 방금 POST에서 가져온 name(key) 를 변수에 할당한다.
        res_data = {}
        if not (username and password and re_password and useremail):
            res_data['error'] = "모든 값을 입력하지 않았습니다."
        elif password != re_password:
            res_data['error'] = "비밀번호가 일치하지 않습니다."
        else:
            fcuser = Fcuser(
                # models 에서 생성한 테이블 클래스를 불러와서 필드 변수에 사용자로부터 받은 값을 할당해준다.
                username=username,
                useremail=useremail,
                password=make_password(password)
            )

        # 테이블에 데이터를 저장한다.
            fcuser.save()

        # rennder 가 POST 값을 가진 templates을 요청하면
        # url로 전송된다.
        return render(request, 'register.html', res_data)

        # context , HTML 템플릿으로 넘겨줄 딕셔너리 형태의 변수

    # 브라우저에서 요청을 하면 웹서버는 클라이언트한테 세션아이디를 만들어주고 세션아이디를 등록한다.
    # 클라이언트가 다시 요청해도 클라이언트는 쿠키에 해당 세션아이디를 기록하고 있기 때문에 웹서버에서 요청과 쿠키를 같이 받아 해당 세션아이디를 찾기 때문에 세션아이디가 등록되있으면 로그인이 되는것이다.
