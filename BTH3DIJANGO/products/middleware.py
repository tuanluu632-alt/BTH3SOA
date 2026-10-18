import requests
from django.http import JsonResponse


class AuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Chỉ kiểm tra các API products
        if request.path.startswith('/products'):

            authorization = request.headers.get('Authorization')

            if not authorization:
                return JsonResponse({
                    'message': 'Thiếu Authorization'
                }, status=401)

            if not authorization.startswith('Bearer '):
                return JsonResponse({
                    'message': 'Authorization phải có dạng Bearer <token>'
                }, status=401)

            try:

                # Gọi sang Bài 2 để xác thực token
                response = requests.post(
                    'http://127.0.0.1:8000/auth/',
                    headers={
                        'Authorization': authorization
                    },
                    timeout=5
                )

                if response.status_code != 200:
                    return JsonResponse({
                        'message': 'Token không hợp lệ'
                    }, status=401)

                data = response.json()

                if not data.get('valid'):
                    return JsonResponse({
                        'message': 'Token không hợp lệ'
                    }, status=401)

                # Lưu thông tin user để API có thể sử dụng
                request.user_id = data.get('user_id')
                request.username = data.get('username')

            except requests.exceptions.RequestException:
                return JsonResponse({
                    'message': 'Không thể kết nối Auth Service'
                }, status=503)

        return self.get_response(request)