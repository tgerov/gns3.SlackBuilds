# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from aiohttp.web import HTTPConflict
from gns3server.web.route import Route
from gns3server.schemas.node import NODE_CAPTURE_SCHEMA
from gns3server.schemas.nio import NIO_SCHEMA
from gns3server.compute.vmware import VMware
from gns3server.compute.project_manager import ProjectManager

from gns3server.schemas.vmware import (
    VMWARE_CREATE_SCHEMA,
    VMWARE_OBJECT_SCHEMA
)


class VMwareHandler:

    """
    API entry points for VMware.
    """

    @Route.post(
        r"/projects/{project_id}/vmware/nodes",
        parameters={
            "project_id": "Project UUID"
        },
        status_codes={
            201: "Instance created",
            400: "Invalid request",
            409: "Conflict"
        },
        description="Create a new VMware VM instance",
        input=VMWARE_CREATE_SCHEMA,
        output=VMWARE_OBJECT_SCHEMA)
    async def create(request, response):

        vmware_manager = VMware.instance()
        vm = await vmware_manager.create_node(request.json.pop("name"),
                                                   request.match_info["project_id"],
                                                   request.json.get("node_id"),
                                                   request.json.pop("vmx_path"),
                                                   linked_clone=request.json.pop("linked_clone"),
                                                   console=request.json.get("console", None),
                                                   console_type=request.json.get("console_type", "telnet"))

        for name, value in request.json.items():
            if name != "node_id":
                if hasattr(vm, name) and getattr(vm, name) != value:
                    setattr(vm, name, value)

        response.set_status(201)
        response.json(vm)

    @Route.get(
        r"/projects/{project_id}/vmware/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            200: "Success",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Get a VMware VM instance",
        output=VMWARE_OBJECT_SCHEMA)
    def show(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        response.json(vm)

    @Route.put(
        r"/projects/{project_id}/vmware/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            200: "Instance updated",
            400: "Invalid request",
            404: "Instance doesn't exist",
            409: "Conflict"
        },
        description="Update a VMware VM instance",
        input=VMWARE_OBJECT_SCHEMA,
        output=VMWARE_OBJECT_SCHEMA)
    def update(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        # update the console first to avoid issue if updating console type
        vm.console = request.json.pop("console", vm.console)
        for name, value in request.json.items():
            if hasattr(vm, name) and getattr(vm, name) != value:
                setattr(vm, name, value)

        vm.updated()
        response.json(vm)

    @Route.delete(
        r"/projects/{project_id}/vmware/nodes/{node_id}",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance deleted",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Delete a VMware VM instance")
    async def delete(request, response):

        # check the project_id exists
        ProjectManager.instance().get_project(request.match_info["project_id"])
        await VMware.instance().delete_node(request.match_info["node_id"])
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/start",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance started",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Start a VMware VM instance")
    async def start(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        if vm.check_hw_virtualization():
            pm = ProjectManager.instance()
            if pm.check_hardware_virtualization(vm) is False:
                raise HTTPConflict(text="Cannot start VM because hardware virtualization (VT-x/AMD-V) is already used by another software like VirtualBox or KVM (on Linux)")
        await vm.start()
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/stop",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance stopped",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Stop a VMware VM instance")
    async def stop(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        await vm.stop()
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/suspend",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance suspended",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Suspend a VMware VM instance")
    async def suspend(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        await vm.suspend()
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/resume",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance resumed",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Resume a suspended VMware VM instance")
    async def resume(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        await vm.resume()
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/reload",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID"
        },
        status_codes={
            204: "Instance reloaded",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Reload a VMware VM instance")
    async def reload(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        await vm.reload()
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/nio",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter where the nio should be added",
            "port_number": "Port on the adapter (always 0)"
        },
        status_codes={
            201: "NIO created",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Add a NIO to a VMware VM instance",
        input=NIO_SCHEMA,
        output=NIO_SCHEMA)
    async def create_nio(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        nio_type = request.json["type"]
        if nio_type not in ("nio_udp", "nio_vmnet", "nio_nat", "nio_tap"):
            raise HTTPConflict(text="NIO of type {} is not supported".format(nio_type))
        nio = vmware_manager.create_nio(request.json)
        await vm.adapter_add_nio_binding(int(request.match_info["adapter_number"]), nio)
        response.set_status(201)
        response.json(nio)

    @Route.put(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/nio",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Network adapter where the nio is located",
            "port_number": "Port from where the nio should be updated"
        },
        status_codes={
            201: "NIO updated",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        input=NIO_SCHEMA,
        output=NIO_SCHEMA,
        description="Update a NIO on a VMware VM instance")
    async def update_nio(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        adapter_number = int(request.match_info["adapter_number"])
        nio = vm.get_nio(adapter_number)
        if "filters" in request.json:
            nio.filters = request.json["filters"]
        await vm.adapter_update_nio_binding(adapter_number, nio)
        response.set_status(201)
        response.json(request.json)

    @Route.delete(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/nio",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter from where the nio should be removed",
            "port_number": "Port on the adapter (always 0)"
        },
        status_codes={
            204: "NIO deleted",
            400: "Invalid request",
            404: "Instance doesn't exist"
        },
        description="Remove a NIO from a VMware VM instance")
    async def delete_nio(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        adapter_number = int(request.match_info["adapter_number"])
        await vm.adapter_remove_nio_binding(adapter_number)
        response.set_status(204)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/start_capture",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter to start a packet capture",
            "port_number": "Port on the adapter (always 0)"
        },
        status_codes={
            200: "Capture started",
            400: "Invalid request",
            404: "Instance doesn't exist",
        },
        description="Start a packet capture on a VMware VM instance",
        input=NODE_CAPTURE_SCHEMA)
    async def start_capture(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        adapter_number = int(request.match_info["adapter_number"])
        pcap_file_path = os.path.join(vm.project.capture_working_directory(), request.json["capture_file_name"])
        await vm.start_capture(adapter_number, pcap_file_path)
        response.json({"pcap_file_path": pcap_file_path})

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/stop_capture",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter to stop a packet capture",
            "port_number": "Port on the adapter (always 0)"
        },
        status_codes={
            204: "Capture stopped",
            400: "Invalid request",
            404: "Instance doesn't exist",
        },
        description="Stop a packet capture on a VMware VM instance")
    async def stop_capture(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        adapter_number = int(request.match_info["adapter_number"])
        await vm.stop_capture(adapter_number)
        response.set_status(204)

    @Route.get(
        r"/projects/{project_id}/vmware/nodes/{node_id}/adapters/{adapter_number:\d+}/ports/{port_number:\d+}/pcap",
        description="Stream the pcap capture file",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
            "adapter_number": "Adapter to steam a packet capture",
            "port_number": "Port on the adapter (always 0)"
        },
        status_codes={
            200: "File returned",
            403: "Permission denied",
            404: "The file doesn't exist"
        })
    async def stream_pcap_file(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        adapter_number = int(request.match_info["adapter_number"])
        nio = vm.get_nio(adapter_number)
        await vmware_manager.stream_pcap_file(nio, vm.project.id, request, response)

    @Route.post(
        r"/projects/{project_id}/vmware/nodes/{node_id}/interfaces/vmnet",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
        },
        status_codes={
            201: "VMnet interface allocated",
        },
        description="Allocate a VMware VMnet interface on the server")
    def allocate_vmnet(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        vmware_manager.refresh_vmnet_list(ubridge=False)
        vmnet = vmware_manager.allocate_vmnet()
        vm.vmnets.append(vmnet)
        response.set_status(201)
        response.json({"vmnet": vmnet})

    @Route.get(
        r"/vmware/vms",
        status_codes={
            200: "Success",
        },
        description="Get all VMware VMs available")
    async def get_vms(request, response):
        vmware_manager = VMware.instance()
        vms = await vmware_manager.list_vms()
        response.json(vms)

    @Route.get(
        r"/projects/{project_id}/vmware/nodes/{node_id}/console/ws",
        description="WebSocket for console",
        parameters={
            "project_id": "Project UUID",
            "node_id": "Node UUID",
        })
    async def console_ws(request, response):

        vmware_manager = VMware.instance()
        vm = vmware_manager.get_node(request.match_info["node_id"], project_id=request.match_info["project_id"])
        return await vm.start_websocket_console(request)
