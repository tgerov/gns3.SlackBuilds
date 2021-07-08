#!/usr/bin/env python
#
# Copyright (C) 2016 GNS3 Technologies Inc.
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

import sys

from .cloud import Cloud
from ...error import NodeError

import gns3server.utils.interfaces
from gns3server.config import Config

import logging
log = logging.getLogger(__name__)


class Nat(Cloud):
    """
    A portable and pre-configured node allowing topologies to get a
    NAT access.
    """

    def __init__(self, name, node_id, project, manager, ports=None):

        if sys.platform.startswith("linux"):
            nat_interface = Config.instance().get_section_config("Server").get("default_nat_interface", "virbr0")
            if nat_interface not in [interface["name"] for interface in gns3server.utils.interfaces.interfaces()]:
                raise NodeError("NAT interface {} is missing, please install libvirt".format(nat_interface))
            interface = nat_interface
        else:
            nat_interface = Config.instance().get_section_config("Server").get("default_nat_interface", "vmnet8")
            interfaces = list(filter(lambda x: nat_interface in x.lower(),
                           [interface["name"] for interface in gns3server.utils.interfaces.interfaces()]))
            if not len(interfaces):
                raise NodeError("NAT interface {} is missing. You need to install VMware or use the NAT node on GNS3 VM".format(nat_interface))
            interface = interfaces[0]  # take the first available interface containing the vmnet8 name

        log.info("NAT node '{}' configured to use NAT interface '{}'".format(name, interface))
        ports = [
            {
                "name": "nat0",
                "type": "ethernet",
                "interface": interface,
                "port_number": 0
            }
        ]
        super().__init__(name, node_id, project, manager, ports=ports)

    @property
    def ports_mapping(self):
        return self._ports_mapping

    @ports_mapping.setter
    def ports_mapping(self, ports):
        # It's not allowed to change it
        pass

    @classmethod
    def is_supported(self):
        return True

    def __json__(self):
        return {
            "name": self.name,
            "node_id": self.id,
            "project_id": self.project.id,
            "status": "started",
            "ports_mapping": self.ports_mapping
        }
