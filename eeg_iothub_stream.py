"""
EEG IoT Hub Streaming for L.I.F.E Platform

Uses azure-iot-device when available; otherwise provides a stub that logs
messages. Connection string is read from environment variable AZURE_IOTHUB_DEVICE_CONNECTION_STRING
or can be provided directly to create_device_client.

ASCII-safe logging only.
"""

import asyncio
import json
import logging
import os
from typing import Any, AsyncIterator, Dict, Optional

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

try:  # Prefer async client
    from azure.iot.device.aio import (
        IoTHubDeviceClient as _RealIoTHubDeviceClient,  # type: ignore
    )
except Exception:  # pragma: no cover
    _RealIoTHubDeviceClient = None  # type: ignore


class _StubDeviceClient:
    async def connect(self) -> None:
        logger.info("[IoT] Stub client connected")

    async def send_message(self, message: str) -> None:
        logger.info("[EEG->IoT] %s", message[:200])

    async def shutdown(self) -> None:
        logger.info("[IoT] Stub client shutdown")


class IoTHubDeviceClientFactory:
    @staticmethod
    def create_from_connection_string(connection_string: str):
        if _RealIoTHubDeviceClient is not None:
            return _RealIoTHubDeviceClient.create_from_connection_string(connection_string)  # type: ignore[no-any-return]
        return _StubDeviceClient()


def create_device_client(connection_string: Optional[str] = None):
    cs = connection_string or os.getenv("AZURE_IOTHUB_DEVICE_CONNECTION_STRING")
    if not cs:
        logger.warning(
            "[WARN] No IoT Hub device connection string found. Using stub client."
        )
        return _StubDeviceClient()
    if _RealIoTHubDeviceClient is None:
        logger.warning("[WARN] azure-iot-device not installed. Using stub client.")
        return _StubDeviceClient()
    return IoTHubDeviceClientFactory.create_from_connection_string(cs)


async def stream_eeg_to_platform(
    read_from_headset: AsyncIterator[Dict[str, Any]],
    device_client: Optional[Any] = None,
    interval_seconds: float = 0.0039,
) -> None:
    """
    Stream EEG samples to IoT Hub. 256 Hz sampling ~ every 3.9 ms.
    read_from_headset: async iterator yielding dict samples (JSON-serializable)
    """
    client = device_client or create_device_client()

    await client.connect()
    try:
        async for sample in read_from_headset:
            await client.send_message(json.dumps(sample))
            await asyncio.sleep(interval_seconds)
    finally:
        await client.shutdown()
