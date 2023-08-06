# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['strawberry_django_jwt',
 'strawberry_django_jwt.refresh_token',
 'strawberry_django_jwt.refresh_token.admin',
 'strawberry_django_jwt.refresh_token.management',
 'strawberry_django_jwt.refresh_token.management.commands',
 'strawberry_django_jwt.refresh_token.migrations']

package_data = \
{'': ['*'],
 'strawberry_django_jwt': ['locale/ar/LC_MESSAGES/*',
                           'locale/es/LC_MESSAGES/*',
                           'locale/fr/LC_MESSAGES/*',
                           'locale/nl/LC_MESSAGES/*',
                           'locale/pt_BR/LC_MESSAGES/*'],
 'strawberry_django_jwt.refresh_token': ['locale/ar/LC_MESSAGES/*',
                                         'locale/es/LC_MESSAGES/*',
                                         'locale/fr/LC_MESSAGES/*',
                                         'locale/nl/LC_MESSAGES/*',
                                         'locale/pt_BR/LC_MESSAGES/*']}

install_requires = \
['PyJWT>=1.7.1,<3.0',
 'django-admin-display>=1.3.0,<2.0.0',
 'packaging>=20.0,<30.0',
 'strawberry-django-plus>=1.17.0,<2.0.0',
 'strawberry-graphql-django>=0.2.5,<4.0',
 'strawberry-graphql>=0.69.0,<1.0.0']

extras_require = \
{':python_version <= "3.7"': ['importlib-metadata>=1.7,<5.0']}

setup_kwargs = {
    'name': 'gqlauth-jwt',
    'version': '0.2.0',
    'description': 'Strawberry-graphql port of the graphene-django-jwt package',
    'long_description': '# Strawberry Django JWT\n\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/strawberry-django-jwt?style=for-the-badge)](https://pypi.org/project/strawberry-django-jwt/)\n\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/KundaPanda/strawberry-django-jwt?style=for-the-badge)](https://github.com/KundaPanda/strawberry-django-jwt/graphs/commit-activity)\n![GitHub last commit](https://img.shields.io/github/last-commit/KundaPanda/strawberry-django-jwt?style=for-the-badge)\n\n![Codecov](https://img.shields.io/codecov/c/github/KundaPanda/strawberry-django-jwt?style=for-the-badge)\n[![Codacy grade](https://img.shields.io/codacy/grade/aa892e1ed8924429af95d9eeaa495338?style=for-the-badge)](https://www.codacy.com/gh/KundaPanda/strawberry-django-jwt/dashboard?utm_source=github.com&utm_medium=referral&utm_content=KundaPanda/strawberry-django-jwt&utm_campaign=Badge_Grade)\n\n[JSON Web Token](https://jwt.io/>) authentication\nfor [Strawberry Django GraphQL](https://strawberry.rocks/docs/integrations/django)\n\n---\n\n## Disclaimer\n\nThis project is a forked version of [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt) that\nsubstitutes [Graphene](https://graphene-python.org/) GraphQL backend for [Strawberry](https://strawberry.rocks/)\n\n---\n\n## Installation\n\n1. Install last stable version from Pypi:\n\n   ```shell\n   pip install strawberry-django-jwt\n   ```\n\n2. Add `AuthenticationMiddleware` middleware to your **MIDDLEWARE** settings:\n\n   ```python\n   MIDDLEWARE = [\n       ...,\n       \'django.contrib.auth.middleware.AuthenticationMiddleware\',\n       ...,\n   ]\n   ```\n\n3. Add following django apps to **INSTALLED_APPS**:\n\n   ```python\n   INSTALLED_APPS = [\n       \'django.contrib.auth\',\n       \'django.contrib.contenttypes\',\n       \'django.contrib.sessions\',\n       ...,\n   ]\n   ```\n\n   If using refresh tokens, also add `strawberry_django_jwt.refresh_token`\n\n   ```python\n   INSTALLED_APPS = [\n       \'django.contrib.auth\',\n       \'django.contrib.contenttypes\',\n       \'django.contrib.sessions\',\n       ...,\n       \'strawberry_django_jwt.refresh_token\',\n       ...,\n   ]\n   ```\n\n4. Add `JSONWebTokenMiddleware` or `AsyncJSONWebTokenMiddleware` middleware to your **STRAWBERRY** schema definition:\n\n   ```python\n   from strawberry_django_jwt.middleware import JSONWebTokenMiddleware, AsyncJSONWebTokenMiddleware\n   from strawberry import Schema\n\n   # !! IMPORTANT !!\n   # Pick only one, async middleware is needed when using AsyncGraphQLSchema\n   schema = Schema(..., extensions=[\n      JSONWebTokenMiddleware,\n      AsyncJSONWebTokenMiddleware,\n   ])\n   ```\n\n5. Add `JSONWebTokenBackend` backend to your **AUTHENTICATION_BACKENDS**:\n\n   ```python\n   AUTHENTICATION_BACKENDS = [\n       \'strawberry_django_jwt.backends.JSONWebTokenBackend\',\n       \'django.contrib.auth.backends.ModelBackend\',\n   ]\n   ```\n\n6. Add _strawberry-django-jwt_ mutations to the root schema:\n\n   ```python\n   import strawberry\n   import strawberry_django_jwt.mutations as jwt_mutations\n\n   @strawberry.type\n   class Mutation:\n       token_auth = jwt_mutations.ObtainJSONWebToken.obtain\n       verify_token = jwt_mutations.Verify.verify\n       refresh_token = jwt_mutations.Refresh.refresh\n       delete_token_cookie = jwt_mutations.DeleteJSONWebTokenCookie.delete_cookie\n   ```\n\n   schema = strawberry.Schema(mutation=Mutation, query=...)\n\n7. \\[OPTIONAL\\] Set up the custom Strawberry views\n\n   These views set the status code of failed authentication attempts to 401 instead of the default 200.\n\n   ```python\n   from django.urls import re_path\n   from strawberry_django_jwt.decorators import jwt_cookie\n   from strawberry_django_jwt.views import StatusHandlingGraphQLView as GQLView\n   from ... import schema\n\n   urlpatterns += \\\n   [\n       re_path(r\'^graphql/?$\', jwt_cookie(GQLView.as_view(schema=schema))),\n   ]\n   ```\n\n   or, for async views:\n\n   ```python\n   from django.urls import re_path\n   from strawberry_django_jwt.decorators import jwt_cookie\n   from strawberry_django_jwt.views import AsyncStatusHandlingGraphQLView as AGQLView\n   from ... import schema\n\n   urlpatterns += \\\n   [\n       re_path(r\'^graphql/?$\', jwt_cookie(AGQLView.as_view(schema=schema))),\n   ]\n   ```\n\n---\n\n## Known Issues\n\n- `JWT_ALLOW_ANY_CLASSES`\n\n  - Only supports return-type based filtering at the moment, because strawberry does not use class-based field\n    definitions (so all superclasses are dropped)\n\n  - It might be possible to create a workaround by using either a class decorator or by creating a custom graphql\n    scheme that somehow preserves class hierarchy of types\n\n## Example Application\n\nTo start the example application, install poetry dev dependencies (`poetry install` will suffice) and run `poetry run uvicorn tests.example_app.asgi:application`\n\n## Quickstart Documentation\n\n===============_Work in Progress_===============\n\nRelay support has been temporarily removed due to lack of experience with Relay\n\nMost of the features are conceptually the same as those provided\nby [Django GraphQL JWT](https://github.com/flavors/django-graphql-jwt)\n\n### Authenticating Fields\n\nFields can be set to auth-only using the `login_required` decorator in combination with `strawberry.field` or\nvia `login_field`\n\n```python\nimport strawberry\nfrom strawberry.types import Info\nfrom strawberry_django_jwt.decorators import login_required\nfrom strawberry_django_jwt.decorators import login_field\n\n\n@strawberry.type\nclass Query:\n    @login_field\n    def hello(self, info: Info) -> str:\n        return "World"\n\n    @strawberry.field\n    @login_required\n    def foo(self, info: Info) -> str:\n        return "Bar"\n\n    @strawberry.field\n    @login_required\n    def foo2(self) -> str:\n        return "Bar2"\n```\n\nThe info argument is optional. If not provided, the login_required decorator decorates the resolver function with a\ncustom function with info.\n\nAll required function arguments that are not present in the definition (atm. only info) will be added by\nthe `login_required` decorator to the `self` dictionary as kwargs.\n\n### Model Mutations\n\nYou can add the login_required decorator to them as well\n\n```python\nimport strawberry\nfrom strawberry_django_jwt.decorators import login_required\nfrom strawberry.django import mutations\n\n\n@strawberry.type\nclass Mutation:\n    foo_create: FooType = login_required(mutations.create(FooInput))\n    foo_delete: FooType = login_required(mutations.update(FooPartialInput))\n    foo_update: FooType = login_required(mutations.delete())\n```\n\n### Async Views\n\nShould be fully supported :)\n\n```python\nimport strawberry\nfrom strawberry_django_jwt.decorators import login_field\n\n\n@strawberry.type\nclass Query:\n    @login_field\n    async def foo(self) -> str:\n        return "bar"\n```\n\n### Other\n\nThe introspection query authentication can be controlled by setting `JWT_AUTHENTICATE_INTROSPECTION`\n',
    'author': 'Vojtěch Dohnal',
    'author_email': 'vojdoh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
