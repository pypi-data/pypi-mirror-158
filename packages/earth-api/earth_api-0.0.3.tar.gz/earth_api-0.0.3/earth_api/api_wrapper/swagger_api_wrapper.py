# -*- coding:utf-8 -*-
import os
import sys
import json
from unittest import result

automation_api_root_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../'))

if  automation_api_root_path not in sys.path:
    sys.path.insert(0, automation_api_root_path)

from swagger_client.api.camera_api import CameraApi
from swagger_client.api.content_api import ContentApi
from swagger_client.api.flight_api import FlightApi
from swagger_client.api.graphics_api import GraphicsApi
from swagger_client.api.layer_api import LayerApi
from swagger_client.api.layers_api import LayersApi
from swagger_client.api.snapshot_api import SnapshotApi
from swagger_client.api.workspace_api import WorkspaceApi
from swagger_client.api.drawings_api import DrawingsApi
from api_wrapper.api_wrapper import BasicAPIWrapper


class SwaggerAPIWrapper(BasicAPIWrapper):

    def __init__(self, api_version="1.16"):
        super().__init__(api_version)
        self.camera_api = CameraApi()
        self.content_api = ContentApi()
        self.flight_api = FlightApi()
        self.graphics_api = GraphicsApi()
        self.layer_api = LayerApi()
        self.layers_api = LayersApi()
        self.snapshot_api = SnapshotApi()
        self.workspace_api = WorkspaceApi()
        self.drawings_api = DrawingsApi()


    def set_camera(self, camera):
        response_data, status_code, headers = self.camera_api.arcgisearth_camera_put(
            _preload_content=False,
            async_req=False,
            body=camera,
            api_version=self.version)

        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result
    
    def get_camera(self):
        age_camera, status_code, headers = self.camera_api.arcgisearth_camera_get(
            async_req=False,
            api_version=self.version)

        return status_code, age_camera.to_dict()
    
    def set_flight(self, flight):
        response_data, status_code, headers = self.flight_api.arcgisearth_flight_post(
            _preload_content=False,
            async_req=False,
            body=flight,
            api_version=self.version)

        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def add_layer(self, layer):
        response_data, status_code, headers = self.layer_api.arcgisearth_layer_post(
            _preload_content=False,
            async_req=False,
            body=layer,
            api_version=self.version)
        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def get_layer(self, layer_id):
        response_data, status_code, headers = self.layer_api.arcgisearth_layer_id_get(
            id=layer_id,
            _preload_content=False,
            async_req=False,
            api_version=self.version)

        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def remove_layer(self, layer_id):
        response_data, status_code, headers = self.layer_api.arcgisearth_layer_id_delete(
            id=layer_id,
            _preload_content=False,
            async_req=False,
            api_version=self.version)

        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result


    def clear_layers(self, target="operationallayers"):
        response_data, status_code, headers = self.layers_api.arcgisearth_layers_target_delete(
            async_req=False,
            target=target
        )

        result = {}
        if response_data is not None:
            result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def add_graphic(self, graphic):
        response_data = self.graphics_api.arcgisearth_graphics_post(
            body=graphic,
            _preload_content=False,
            async_req=False,
            api_version=self.version)

        status_code = response_data.status
        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def get_graphic(self, graphic_id):
        response_data = self.graphics_api.arcgisearth_graphics_id_get(
            id=graphic_id,
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        status_code = response_data.status
        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def update_graphic(self, graphic):
        response_data = self.graphics_api.arcgisearth_graphics_patch(
            _preload_content=False,
            async_req=False,
            body=graphic,
            api_version=self.version)
        status_code = response_data.status
        return status_code, {}

    def remove_graphic(self, graphic_id):
        response_data = self.graphics_api.arcgisearth_graphics_id_delete(
            id=graphic_id,
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        status_code = response_data.status
        return status_code, {} 

    def clear_graphics(self):
        response_data = self.graphics_api.arcgisearth_graphics_delete(
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        status_code = response_data.status
        return status_code, {} 

    def add_drawing(self, drawing):
        response_data = self.drawings_api.arcgisearth_drawings_post(
        _preload_content=False,
        async_req=False,
        body=drawing,
        api_version=self.version)
        status_code = response_data.status
        result = json.loads(response_data.data.decode('utf-8'))
        return status_code, result

    def remove_drawing(self, drawing_id):
        response_data = self.drawings_api.arcgisearth_drawings_id_delete(
        _preload_content=False,
        async_req=False,
        id=drawing_id,
        api_version=self.version)

        return response_data.status, {}


    def clear_drawings(self):
        response_data = self.drawings_api.arcgisearth_drawings_delete(
            _preload_content=False,
            async_req=False,
            api_version=self.version)

        return response_data.status, {}

    def get_workspace(self):
        response_data, status_code, headers = self.workspace_api.arcgisearth_workspace_get(
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        return status_code, json.loads(response_data.data.decode('utf-8'))

    def import_workspace(self, workspace_info):
        response_data, status_code, headers = self.workspace_api.arcgisearth_workspace_put(
            _preload_content=False,
            async_req=False,
            body=workspace_info,
            api_version=self.version)
        return status_code, json.loads(response_data.data.decode('utf-8'))

    def clear_workspace(self):
        response_data, status_code, headers = self.workspace_api.arcgisearth_workspace_delete(
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        return status_code, json.loads(response_data.data.decode('utf-8'))


    def get_snapshot(self):
        response_data, status_code, headers = self.snapshot_api.arcgisearth_snapshot_get(
            _preload_content=False,
            async_req=False,
            api_version=self.version)
        return status_code, response_data

    