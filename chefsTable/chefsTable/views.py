from django.http import HttpResponse 

# カスタムハンドラーを表示するには、セッティングでデバッグを無効にする必要がある
# DEBUG = False
# ALLOWED_HOSTS = ['*']

def handler404(request, exception):
    return HttpResponse('4040: page not found costom page')
