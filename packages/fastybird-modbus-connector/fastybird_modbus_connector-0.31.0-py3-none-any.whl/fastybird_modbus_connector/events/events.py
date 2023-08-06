#!/usr/bin/python3

#     Copyright 2022. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Modbus connector events module events
"""

# Python base dependencies
from typing import Optional

# Library dependencies
from whistle import Event

# Library libs
from fastybird_modbus_connector.registry.records import PropertyRecord, RegisterRecord


class RegisterActualValueEvent(Event):
    """
    Register record actual value was updated in registry

    @package        FastyBird:ModbusConnector!
    @module         events/events

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __original_record: Optional[RegisterRecord]
    __updated_record: RegisterRecord

    EVENT_NAME: str = "registry.RegisterRecordActualValueUpdated"

    # -----------------------------------------------------------------------------

    def __init__(self, original_record: Optional[RegisterRecord], updated_record: RegisterRecord) -> None:
        self.__original_record = original_record
        self.__updated_record = updated_record

    # -----------------------------------------------------------------------------

    @property
    def original_record(self) -> Optional[RegisterRecord]:
        """Original register record"""
        return self.__original_record

    # -----------------------------------------------------------------------------

    @property
    def updated_record(self) -> RegisterRecord:
        """Updated register record"""
        return self.__updated_record


class PropertyActualValueEvent(Event):
    """
    Property record actual value was updated in registry

    @package        FastyBird:ModbusConnector!
    @module         events/events

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __original_record: Optional[PropertyRecord]
    __updated_record: PropertyRecord

    EVENT_NAME: str = "registry.propertyRecordActualValueUpdated"

    # -----------------------------------------------------------------------------

    def __init__(self, original_record: Optional[PropertyRecord], updated_record: PropertyRecord) -> None:
        self.__original_record = original_record
        self.__updated_record = updated_record

    # -----------------------------------------------------------------------------

    @property
    def original_record(self) -> Optional[PropertyRecord]:
        """Original property record"""
        return self.__original_record

    # -----------------------------------------------------------------------------

    @property
    def updated_record(self) -> PropertyRecord:
        """Updated property record"""
        return self.__updated_record
