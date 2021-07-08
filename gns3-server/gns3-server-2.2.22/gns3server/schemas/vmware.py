# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
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

from .custom_adapters import CUSTOM_ADAPTERS_ARRAY_SCHEMA


VMWARE_CREATE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "Request validation to create a new VMware VM instance",
    "type": "object",
    "properties": {
        "node_id": {
            "description": "Node UUID",
            "type": "string",
            "minLength": 36,
            "maxLength": 36,
            "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        },
        "linked_clone": {
            "description": "Whether the VM is a linked clone or not",
            "type": "boolean"
        },
        "name": {
            "description": "VMware VM instance name",
            "type": "string",
            "minLength": 1,
        },
        "usage": {
            "description": "How to use the VMware VM",
            "type": "string",
        },
        "vmx_path": {
            "description": "Path to the vmx file",
            "type": "string",
            "minLength": 1,
        },
        "console": {
            "description": "Console TCP port",
            "minimum": 1,
            "maximum": 65535,
            "type": ["integer", "null"]
        },
        "console_type": {
            "description": "Console type",
            "enum": ["telnet", "none"]
        },
        "headless": {
            "description": "Headless mode",
            "type": "boolean"
        },
        "on_close": {
            "description": "Action to execute on the VM is closed",
            "enum": ["power_off", "shutdown_signal", "save_vm_state"],
        },
        "adapters": {
            "description": "Number of adapters",
            "type": "integer",
            "minimum": 0,
            "maximum": 10,  # maximum adapters support by VMware VMs
        },
        "adapter_type": {
            "description": "VMware adapter type",
            "type": "string",
            "minLength": 1,
        },
        "use_any_adapter": {
            "description": "Allow GNS3 to use any VMware adapter",
            "type": "boolean",
        },
        "custom_adapters": CUSTOM_ADAPTERS_ARRAY_SCHEMA
    },
    "additionalProperties": False,
    "required": ["name", "vmx_path", "linked_clone"],
}


VMWARE_OBJECT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "VMware VM instance",
    "type": "object",
    "properties": {
        "name": {
            "description": "VMware VM instance name",
            "type": "string",
            "minLength": 1,
        },
        "usage": {
            "description": "How to use the VMware VM",
            "type": "string",
        },
        "node_id": {
            "description": "Node UUID",
            "type": "string",
            "minLength": 36,
            "maxLength": 36,
            "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        },
        "status": {
            "description": "VM status",
            "enum": ["started", "stopped", "suspended"]
        },
        "node_directory": {
            "description": "Path to the node working directory",
            "type": ["string", "null"]
        },
        "project_id": {
            "description": "Project UUID",
            "type": "string",
            "minLength": 36,
            "maxLength": 36,
            "pattern": "^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$"
        },
        "vmx_path": {
            "description": "Path to the vmx file",
            "type": "string",
            "minLength": 1,
        },
        "headless": {
            "description": "Headless mode",
            "type": "boolean"
        },
        "on_close": {
            "description": "Action to execute on the VM is closed",
            "enum": ["power_off", "shutdown_signal", "save_vm_state"],
        },
        "adapters": {
            "description": "Number of adapters",
            "type": "integer",
            "minimum": 0,
            "maximum": 10,  # maximum adapters support by VMware VMs
        },
        "adapter_type": {
            "description": "VMware adapter type",
            "type": "string",
            "minLength": 1,
        },
        "use_any_adapter": {
            "description": "Allow GNS3 to use any VMware adapter",
            "type": "boolean",
        },
        "console": {
            "description": "Console TCP port",
            "minimum": 1,
            "maximum": 65535,
            "type": ["integer", "null"]
        },
        "console_type": {
            "description": "Console type",
            "enum": ["telnet", "none"]
        },
        "linked_clone": {
            "description": "Whether the VM is a linked clone or not",
            "type": "boolean"
        },
        "custom_adapters": CUSTOM_ADAPTERS_ARRAY_SCHEMA
    },
    "additionalProperties": False
}
