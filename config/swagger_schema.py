import coreschema
from rest_framework import schemas
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.schemas.generators import INSERT_INTO_COLLISION_FMT, LinkNode
from rest_framework.views import APIView
from rest_framework_swagger import renderers
import yaml
import coreapi

"""
自定义文档处理格式
"""


def insert_into(target, keys, value):
    """
    Nested dictionary insertion.
    这个方法是在django-money的文件找到的
    """
    for key in keys[:-1]:
        if key not in target:
            target[key] = LinkNode()
        target = target[key]

    try:
        target.links.append((keys[-1], value))
    except TypeError:
        msg = INSERT_INTO_COLLISION_FMT.format(
            value_url=value.url,
            target_url=target.url,
            keys=keys
        )
        raise ValueError(msg)


class SchemaGenerator(schemas.SchemaGenerator):
    # 重写方法 网上很多教程重写get_link 但是新的swagger版本SchemaGenerator已经没有get_link方法了！
    def get_links(self, request=None):
        links = LinkNode()

        # Generate (path, method, view) given (path, method, callback).
        paths = []
        view_endpoints = []
        for path, method, callback in self.endpoints:
            view = self.create_view(callback, method, request)
            path = self.coerce_path(path, method, view)
            paths.append(path)
            view_endpoints.append((path, method, view))

        # Only generate the path prefix for paths that will be included
        if not paths:
            return None
        prefix = self.determine_path_prefix(paths)

        for path, method, view in view_endpoints:
            if not self.has_view_permissions(path, method, view):
                continue
            link = view.schema.get_link(path, method, base_url=self.url)
            fields = list(link.fields)
            yaml_doc = None
            method_desc = link.description
            # 如果存在视图注释 取视图注释 否则 取方法注释
            doc_desc = view.__doc__ if view and view.__doc__ else method_desc
            # 尝试用yaml解析注释
            try:
                yaml_doc = yaml.load(doc_desc)
            except:
                yaml_doc = None
            if yaml_doc and type(yaml_doc) != str:
                params = yaml_doc.get('parameters', [])
                method_desc = yaml_doc.get('description', '')

                _schema = coreschema.String()
                for i in params:
                    _name = i.get('name')
                    _desc = i.get('description')
                    _required = i.get('required', False)
                    _type = i.get('type', None)
                    _type = 'integer' if _type == 'int' else _type
                    _location = i.get('location', 'formData')
                    field = coreapi.Field(
                        name=_name,
                        location=_location,
                        required=_required,
                        description=_desc,
                        type=_type,
                        schema=_schema,
                        example='',
                    )
                    fields.append(field)
            else:
                pass
            # 因为Link类被设置为无法修改属性 只能新建一个
            nl = coreapi.Link(
                url=link.url,
                action=link.action,
                encoding=link.encoding,
                fields=tuple(fields),
                description=method_desc,
            )
            subpath = path[len(prefix):]
            keys = self.get_keys(subpath, method, view)
            insert_into(links, keys, nl)

        return links


class SwaggerSchemaView(APIView):
    exclude_from_schema = True
    permission_classes = [AllowAny]
    renderer_classes = [
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ]

    def get(self, request):
        generator = SchemaGenerator()
        schema = generator.get_schema(request=request)
        return Response(schema)
