from io import BytesIO

from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required
from injector import Injector

from src.application.api.controller.generic_entity_controller import GenericEntityController
from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.file_document_mapper import FileDocumentMapper
from src.entities.exceptions.invalid_entity_exception import InvalidEntityException
from src.entities.file_document import FileType
from src.service.file_document_service import FileDocumentService


class FileDocumentController:

    def __init__(self, app_injector: Injector):
        self.app_injector = app_injector
        self.controller = Blueprint("file_document_controller", __name__, url_prefix="/api/file-documents")
        self.start_controller()

    def get_app_injector(self) -> Injector:
        return self.app_injector

    def get_controller(self) -> Blueprint:
        return self.controller

    def start_controller(self):
        @self.get_controller().route("", methods=["POST"])
        @jwt_required()
        def create_file_document():
            file_name = request.form.get("name")
            workspace_id = request.form.get("workspace_id")
            file_type = request.form.get("file_type")

            if "file" not in request.files:
                raise InvalidEntityException("FileDocument", ["file"])

            file = request.files["file"]

            dto = {
                "name": file_name or file.filename,
                "workspace": {"id": workspace_id},
                "file_type": file_type or FileType.PHOTO.name
            }

            file_document = FileDocumentMapper.to_entity(dto)
            file_document.file = file.read()

            service = self.app_injector.get(FileDocumentService)

            service.create(file_document)

            return jsonify(FileDocumentMapper.to_dto(file_document)), 201

        @self.controller.route("/<string:file_id>", methods=["GET"])
        @jwt_required()
        def get_file_document(file_id: str):
            uuid_file_id = uuid_mapper.to_uuid(file_id)

            service = self.app_injector.get(FileDocumentService)
            file_document = service.find_by_id(uuid_file_id, fill_file=True)


            return send_file(
                BytesIO(file_document.file),
                mimetype="JPG",
                as_attachment=True,
                download_name=file_document.name,
            )
