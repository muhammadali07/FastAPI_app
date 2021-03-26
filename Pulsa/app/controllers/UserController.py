from starlette.requests import Request
from starlette.responses import JSONResponse

from app import response
from app.models.user import Users
from app.transformers import UserTransformer


class UserController:
    @staticmethod
    async def index(request: Request) -> JSONResponse:
        try:
            users = Users.objects()
            transformer = UserTransformer.transform(users)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def store(request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            if name == "":
                raise Exception("Data Tidak ada")

            user = Users(name=name)
            user.save()
            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "Berhasil Membuat user")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def show(id) -> JSONResponse:
        try:
            user = Users.objects(id=id).first()

            if user is None:
                raise Exception('User tidak di temukan')

            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def update(id: str, request: Request) -> JSONResponse:
        try:
            body = await request.json()
            name = body['name']

            if name == "":
                raise Exception("data kosong")

            user = Users.objects(id=id).first()

            if user is None:
                raise Exception("user tidak ditemukan")
            user.name = name
            user.save()

            transformer = UserTransformer.singleTransform(user)
            return response.ok(transformer, "Berhasil di update")
        except Exception as e:
            return response.badRequest('', f'{e}')

    @staticmethod
    async def delete(id: str) -> JSONResponse:
        try:
            user = User.objects(id=id).first()
            if user is None:
                raise Exception('user tidak ditemukan')

            user.delete()
            return response.ok('', "Berhasil menghapus user")
        except Exception as e:
            return response.badRequest('', f'{e}')
