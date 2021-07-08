# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 GNS3 Technologies Inc.
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

IOU_LICENSE_SETTINGS_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "description": "IOU license",
    "type": "object",
    "properties": {
        "iourc_content": {
            "type": "string",
            "description": "Content of iourc file"
        },
        "license_check": {
            "type": "boolean",
            "description": "Whether the license must be checked or not",
        },
    },
    "additionalProperties": False
}
