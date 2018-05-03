from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    自定义权限，规定只能拥有者自己修改、删除对象
    """

    def has_object_permission(self, request, view, obj):
        """
        :param request:请求对象
        :param view: 视图
        :param obj: 要操作的对象
        :return: 返回是否有权限，有则返回True，否则返回False
        """
        if request.method in permissions.SAFE_METHODS:
            '''
            表示我们永远允许GET等安全的请求方法
            '''
            return True
        # 返回是否有权限，这里我们直接通过对比拥有者是否是请求者作为返回
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.id
        elif hasattr(obj, 'id'):
            return obj.id == request.user.id
        else:
            return False


class UserMessagePermission(permissions.BasePermission):
    """
    用户消息权限，规定只能拥有者才有权限
    """

    def has_object_permission(self, request, view, obj):
        """
        :param request:请求对象
        :param view: 视图
        :param obj: 要操作的对象
        :return: 返回是否有权限，有则返回True，否则返回False
        """
        return request.user.id in (obj.from_user.id, obj.to_user.id)


class IsReadOnlyOrAdmin(permissions.BasePermission):
    """
    自定义权限，规定只能管理员可以修改、删除对象
    """

    def has_object_permission(self, request, view, obj):
        """
        :param request:请求对象
        :param view: 视图
        :param obj: 要操作的对象
        :return: 返回是否有权限，有则返回True，否则返回False
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
