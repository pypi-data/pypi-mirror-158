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
Modbus connector events module listeners
"""

# Python base dependencies
import logging
from datetime import datetime
from typing import Dict, Union

# Library dependencies
from fastybird_devices_module.entities.channel import (
    ChannelDynamicPropertyEntity,
    ChannelStaticPropertyEntity,
)
from fastybird_devices_module.entities.device import (
    DeviceDynamicPropertyEntity,
    DeviceStaticPropertyEntity,
)
from fastybird_devices_module.managers.channel import ChannelPropertiesManager
from fastybird_devices_module.managers.device import DevicePropertiesManager
from fastybird_devices_module.managers.state import (
    ChannelPropertiesStatesManager,
    DevicePropertiesStatesManager,
)
from fastybird_devices_module.repositories.channel import ChannelPropertiesRepository
from fastybird_devices_module.repositories.device import DevicePropertiesRepository
from fastybird_devices_module.repositories.state import (
    ChannelPropertiesStatesRepository,
    DevicePropertiesStatesRepository,
)
from fastybird_metadata.types import ButtonPayload, SwitchPayload
from kink import inject
from whistle import Event, EventDispatcher

# Library libs
from fastybird_modbus_connector.events.events import (
    PropertyActualValueEvent,
    RegisterActualValueEvent,
)
from fastybird_modbus_connector.logger import Logger


@inject
class EventsListener:  # pylint: disable=too-many-instance-attributes
    """
    Events listener

    @package        FastyBird:ModbusConnector!
    @module         events/listeners

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __devices_properties_repository: DevicePropertiesRepository
    __devices_properties_manager: DevicePropertiesManager
    __devices_properties_states_repository: DevicePropertiesStatesRepository
    __devices_properties_states_manager: DevicePropertiesStatesManager

    __channels_properties_repository: ChannelPropertiesRepository
    __channels_properties_manager: ChannelPropertiesManager
    __channels_properties_states_repository: ChannelPropertiesStatesRepository
    __channels_properties_states_manager: ChannelPropertiesStatesManager

    __event_dispatcher: EventDispatcher

    __logger: Union[Logger, logging.Logger]

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        devices_properties_repository: DevicePropertiesRepository,
        devices_properties_manager: DevicePropertiesManager,
        devices_properties_states_repository: DevicePropertiesStatesRepository,
        devices_properties_states_manager: DevicePropertiesStatesManager,
        channels_properties_repository: ChannelPropertiesRepository,
        channels_properties_manager: ChannelPropertiesManager,
        event_dispatcher: EventDispatcher,
        channels_properties_states_repository: ChannelPropertiesStatesRepository,
        channels_properties_states_manager: ChannelPropertiesStatesManager,
        logger: Union[Logger, logging.Logger] = logging.getLogger("dummy"),
    ) -> None:
        self.__devices_properties_repository = devices_properties_repository
        self.__devices_properties_manager = devices_properties_manager
        self.__devices_properties_states_repository = devices_properties_states_repository
        self.__devices_properties_states_manager = devices_properties_states_manager

        self.__channels_properties_repository = channels_properties_repository
        self.__channels_properties_manager = channels_properties_manager
        self.__channels_properties_states_repository = channels_properties_states_repository
        self.__channels_properties_states_manager = channels_properties_states_manager

        self.__event_dispatcher = event_dispatcher

        self.__logger = logger

    # -----------------------------------------------------------------------------

    def open(self) -> None:
        """Open all listeners callbacks"""
        self.__event_dispatcher.add_listener(
            event_id=PropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_attribute_actual_value_updated_event,
        )

        self.__event_dispatcher.add_listener(
            event_id=RegisterActualValueEvent.EVENT_NAME,
            listener=self.__handle_register_actual_value_updated_event,
        )

    # -----------------------------------------------------------------------------

    def close(self) -> None:
        """Close all listeners registrations"""
        self.__event_dispatcher.remove_listener(
            event_id=PropertyActualValueEvent.EVENT_NAME,
            listener=self.__handle_attribute_actual_value_updated_event,
        )

        self.__event_dispatcher.remove_listener(
            event_id=RegisterActualValueEvent.EVENT_NAME,
            listener=self.__handle_register_actual_value_updated_event,
        )

    # -----------------------------------------------------------------------------

    def __handle_attribute_actual_value_updated_event(self, event: Event) -> None:
        if not isinstance(event, PropertyActualValueEvent):
            return

        device_property = self.__devices_properties_repository.get_by_id(property_id=event.updated_record.id)

        if device_property is None:
            self.__logger.warning(
                "Device property couldn't be found in database",
                extra={
                    "device": {"id": str(event.updated_record.device_id)},
                    "property": {"id": str(event.updated_record.id)},
                },
            )
            return

        if isinstance(device_property, DeviceDynamicPropertyEntity):
            try:
                property_state = self.__devices_properties_states_repository.get_by_id(
                    property_id=device_property.id,
                )

            except NotImplementedError:
                self.__logger.warning("States repository is not configured. State could not be fetched")

                return

            state_data: Dict[str, Union[str, int, float, bool, datetime, ButtonPayload, SwitchPayload, None]] = {
                "actual_value": event.updated_record.actual_value,
                "expected_value": None,
                "pending": False,
                "valid": True,
            }

            if property_state is None:
                try:
                    property_state = self.__devices_properties_states_manager.create(
                        device_property=device_property,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Creating new device property state",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

            else:
                try:
                    property_state = self.__devices_properties_states_manager.update(
                        device_property=device_property,
                        state=property_state,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Updating existing device property state",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

        elif isinstance(device_property, DeviceStaticPropertyEntity):
            actual_value_normalized = str(device_property.value) if device_property.value is not None else None
            updated_value_normalized = (
                str(event.updated_record.actual_value) if event.updated_record.actual_value is not None else None
            )

            if actual_value_normalized != updated_value_normalized:
                self.__devices_properties_manager.update(
                    data={
                        "value": event.updated_record.actual_value,
                    },
                    device_property=device_property,
                )

                self.__logger.debug(
                    "Updating existing device property",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_register_actual_value_updated_event(self, event: Event) -> None:
        if not isinstance(event, RegisterActualValueEvent):
            return

        if (
            event.updated_record.channel_id is not None
            and event.updated_record.channel_id == event.updated_record.device_id
        ):
            self.__handle_device_property_actual_value_updated_event(event=event)

        else:
            self.__handle_channel_property_actual_value_updated_event(event=event)

    # -----------------------------------------------------------------------------

    def __handle_device_property_actual_value_updated_event(self, event: RegisterActualValueEvent) -> None:
        device_property = self.__devices_properties_repository.get_by_id(property_id=event.updated_record.id)

        if device_property is None:
            self.__logger.warning(
                "Device property couldn't be found in database",
                extra={
                    "device": {"id": str(event.updated_record.device_id)},
                    "property": {"id": str(event.updated_record.id)},
                },
            )
            return

        if isinstance(device_property, DeviceDynamicPropertyEntity):
            try:
                property_state = self.__devices_properties_states_repository.get_by_id(property_id=device_property.id)

            except NotImplementedError:
                self.__logger.warning("States repository is not configured. State could not be fetched")

                return

            actual_value = (
                event.updated_record.actual_value
                if isinstance(event.updated_record.actual_value, (str, int, float, bool))
                or event.updated_record.actual_value is None
                else str(event.updated_record.actual_value)
            )
            expected_value = (
                event.updated_record.expected_value
                if isinstance(event.updated_record.expected_value, (str, int, float, bool))
                or event.updated_record.expected_value is None
                else str(event.updated_record.expected_value)
            )

            state_data: Dict[str, Union[str, int, float, bool, datetime, ButtonPayload, SwitchPayload, None]] = {
                "actual_value": event.updated_record.actual_value,
                "expected_value": event.updated_record.expected_value,
                "pending": actual_value != expected_value and expected_value is not None,
                "valid": event.updated_record.actual_value_valid,
            }

            if property_state is None:
                try:
                    property_state = self.__devices_properties_states_manager.create(
                        device_property=device_property,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Creating new device property state",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

            else:
                try:
                    property_state = self.__devices_properties_states_manager.update(
                        device_property=device_property,
                        state=property_state,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Updating existing device property state",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

        elif isinstance(device_property, DeviceStaticPropertyEntity):
            actual_value_normalized = str(device_property.value) if device_property.value is not None else None
            updated_value_normalized = (
                str(event.updated_record.actual_value) if event.updated_record.actual_value is not None else None
            )

            if actual_value_normalized != updated_value_normalized:
                self.__devices_properties_manager.update(
                    data={
                        "value": event.updated_record.actual_value,
                    },
                    device_property=device_property,
                )

                self.__logger.debug(
                    "Updating existing device property",
                    extra={
                        "device": {
                            "id": str(device_property.device.id),
                        },
                        "property": {
                            "id": str(device_property.id),
                        },
                    },
                )

    # -----------------------------------------------------------------------------

    def __handle_channel_property_actual_value_updated_event(self, event: RegisterActualValueEvent) -> None:
        channel_property = self.__channels_properties_repository.get_by_id(property_id=event.updated_record.id)

        if channel_property is None:
            self.__logger.warning(
                "Channel property couldn't be found in database",
                extra={
                    "device": {"id": str(event.updated_record.device_id)},
                    "channel": {
                        "id": str(event.updated_record.channel_id)
                        if event.updated_record.channel_id is not None
                        else None
                    },
                    "property": {"id": str(event.updated_record.id)},
                },
            )
            return

        if isinstance(channel_property, ChannelDynamicPropertyEntity):
            try:
                property_state = self.__channels_properties_states_repository.get_by_id(property_id=channel_property.id)

            except NotImplementedError:
                self.__logger.warning("States repository is not configured. State could not be fetched")

                return

            actual_value = (
                event.updated_record.actual_value
                if isinstance(event.updated_record.actual_value, (str, int, float, bool))
                or event.updated_record.actual_value is None
                else str(event.updated_record.actual_value)
            )
            expected_value = (
                event.updated_record.expected_value
                if isinstance(event.updated_record.expected_value, (str, int, float, bool))
                or event.updated_record.expected_value is None
                else str(event.updated_record.expected_value)
            )

            state_data: Dict[str, Union[str, int, float, bool, datetime, ButtonPayload, SwitchPayload, None]] = {
                "actual_value": event.updated_record.actual_value,
                "expected_value": event.updated_record.expected_value,
                "pending": actual_value != expected_value and expected_value is not None,
                "valid": event.updated_record.actual_value_valid,
            }

            if property_state is None:
                try:
                    property_state = self.__channels_properties_states_manager.create(
                        channel_property=channel_property,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Creating new channel property state",
                    extra={
                        "device": {
                            "id": str(channel_property.channel.device.id),
                        },
                        "channel": {
                            "id": str(channel_property.channel.id),
                        },
                        "property": {
                            "id": str(channel_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

            else:
                try:
                    property_state = self.__channels_properties_states_manager.update(
                        channel_property=channel_property,
                        state=property_state,
                        data=state_data,
                    )

                except NotImplementedError:
                    self.__logger.warning("States manager is not configured. State could not be saved")

                    return

                self.__logger.debug(
                    "Updating existing channel property state",
                    extra={
                        "device": {
                            "id": str(channel_property.channel.device.id),
                        },
                        "channel": {
                            "id": str(channel_property.channel.id),
                        },
                        "property": {
                            "id": str(channel_property.id),
                        },
                        "state": {
                            "id": str(property_state.id),
                            "actual_value": property_state.actual_value,
                            "expected_value": property_state.expected_value,
                            "pending": property_state.pending,
                        },
                    },
                )

        elif isinstance(channel_property, ChannelStaticPropertyEntity):
            actual_value_normalized = str(channel_property.value) if channel_property.value is not None else None
            updated_value_normalized = (
                str(event.updated_record.actual_value) if event.updated_record.actual_value is not None else None
            )

            if actual_value_normalized != updated_value_normalized:
                self.__channels_properties_manager.update(
                    data={
                        "value": event.updated_record.actual_value,
                    },
                    channel_property=channel_property,
                )

                self.__logger.debug(
                    "Updating existing device property",
                    extra={
                        "device": {
                            "id": str(channel_property.device.id),
                        },
                        "property": {
                            "id": str(channel_property.id),
                        },
                    },
                )
