# from uuid import UUID
#
# from flask import Flask
# from flask_jwt import JWT, JWTError
# from injector import Injector
#
# from src.application.api.security.auth_user import AuthUser
# from src.entities.exceptions.authentication_exception import AuthenticationException
# from src.entities.user import User
# from src.service.user_service import UserService
#
#
# def fill_jwt_auth_function(app: Flask, injector: Injector) -> JWT:
#
#     def authenticate(login: str, password: str) -> AuthUser:
#         user_service = injector.get(UserService)
#
#         try:
#             return AuthUser(user_service.authenticate(login, password))
#         except AuthenticationException as ex:
#             raise JWTError("Invalid credentials", str(ex))
#
#     def identity(payload: dict) -> User:
#         user_service = injector.get(UserService)
#
#         user_id = UUID(payload.get("identity"))
#         return user_service.find_by_id(user_id)
#
#     return JWT(app, authenticate, identity)
