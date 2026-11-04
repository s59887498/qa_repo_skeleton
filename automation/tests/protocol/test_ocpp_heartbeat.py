"""Minimal OCPP-J Heartbeat envelope example, not a full OCPP simulator/certification."""

import asyncio
from datetime import datetime, timezone
import json
from uuid import uuid4

import pytest


@pytest.mark.protocol
@pytest.mark.case("PROTO-001", "Heartbeat 請求回應關聯", steps=["連本機 WebSocket", "送 Heartbeat", "核對 response ID"], expected="同一 ID 的 CALLRESULT 並含 UTC 時間")
def test_heartbeat_correlation():
    from websockets.asyncio.client import connect
    from websockets.asyncio.server import serve

    async def scenario():
        async def handler(socket):
            kind, request_id, action, payload = json.loads(await socket.recv())
            assert (kind, action, payload) == (2, "Heartbeat", {})
            await socket.send(json.dumps([3, request_id, {
                "currentTime": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            }]))

        async with serve(handler, "127.0.0.1", 0, subprotocols=["ocpp1.6"]) as server:
            port = server.sockets[0].getsockname()[1]
            async with connect(f"ws://127.0.0.1:{port}/DEMO-001", subprotocols=["ocpp1.6"]) as socket:
                request_id = str(uuid4())
                await socket.send(json.dumps([2, request_id, "Heartbeat", {}]))
                response = json.loads(await asyncio.wait_for(socket.recv(), timeout=3))
                assert response[:2] == [3, request_id]
                assert datetime.fromisoformat(response[2]["currentTime"].replace("Z", "+00:00")).tzinfo

    asyncio.run(asyncio.wait_for(scenario(), timeout=10))
