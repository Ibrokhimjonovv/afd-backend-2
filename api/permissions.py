from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    """
    Faqat admin foydalanuvchi uchun yozish va o'chirish ruxsati beriladi.
    Boshqalar faqat o'qiy olishlari mumkin.
    """
    def has_permission(self, request, view):
        # Agar foydalanuvchi admin bo'lsa yoki faqat GET so'rov yuborayotgan bo'lsa
        print(request.user.is_staff)
        return bool(
            request.method in ['GET', 'HEAD', 'OPTIONS', "DELETE"] or
            (request.user and request.user.is_staff)
        )
