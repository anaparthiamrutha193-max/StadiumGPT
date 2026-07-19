"""Thread-safe in-memory adapter for live stadium sensor feeds.
Replace `ingest_crowd` with a Kafka/MQTT/webhook adapter in production without changing API routes.
"""
from __future__ import annotations
from datetime import UTC, datetime
from threading import Lock
from typing import Any

_DEFAULT_READINGS: dict[str, dict[str, Any]] = {
    "Gate A": {"count": 655, "capacity": 900, "flow_per_minute": 31.0},
    "Gate B": {"count": 328, "capacity": 900, "flow_per_minute": 14.0},
    "Gate C": {"count": 471, "capacity": 850, "flow_per_minute": 19.0},
    "Gate D": {"count": 218, "capacity": 700, "flow_per_minute": 10.0},
}

class LiveOperationsStore:
    def __init__(self) -> None:
        self._lock = Lock()
        now = datetime.now(UTC)
        self._readings = {zone: {**reading, "updated_at": now, "source": "mock_live_feed"} for zone, reading in _DEFAULT_READINGS.items()}

    def ingest_crowd(self, zone: str, count: int, capacity: int, flow_per_minute: float, source: str, observed_at: datetime | None) -> dict[str, Any]:
        record = {"count": count, "capacity": capacity, "flow_per_minute": flow_per_minute, "source": source, "updated_at": observed_at or datetime.now(UTC)}
        with self._lock:
            self._readings[zone] = record
        return self.crowd(zone)

    def crowd(self, zone: str) -> dict[str, Any]:
        with self._lock:
            reading = self._readings.get(zone)
            if reading is None:
                reading = {"count": 0, "capacity": 1, "flow_per_minute": 0.0, "source": "no_live_feed", "updated_at": datetime.now(UTC)}
            result = dict(reading)
            all_readings = {name: dict(value) for name, value in self._readings.items()}
        percentage = round(min(100, result["count"] / max(1, result["capacity"]) * 100))
        projected = round(min(100, (result["count"] + result["flow_per_minute"] * 15) / max(1, result["capacity"]) * 100))
        density = "High" if percentage >= 75 else "Moderate" if percentage >= 45 else "Low"
        alternatives = [name for name, value in sorted(all_readings.items(), key=lambda item: item[1]["count"] / max(1, item[1]["capacity"])) if name != zone][:2]
        return {"zone": zone, "density": density, "percentage": percentage, "predicted_percentage_15m": projected, "flow_per_minute": result["flow_per_minute"], "source": result["source"], "updated_at": result["updated_at"], "alternate_gates": alternatives}

    def context(self) -> str:
        snapshots = [self.crowd(zone) for zone in self.zones()]
        gates = "; ".join(f"{row['zone']}: {row['percentage']}% occupancy, {row['flow_per_minute']}/min, projected {row['predicted_percentage_15m']}%" for row in snapshots)
        return (f"Crowd telemetry ({gates}). Security: no verified high-priority alerts. Medical: no active incidents in the control feed. "
                "Volunteers: 18 available, 6 positioned at gates. Transport: shuttle wait 8 min, parking north lot 62% full. "
                "Weather: 29C, partly cloudy, 15% rain probability. Data source: development mock live feed; confirm through venue control.")

    def zones(self) -> list[str]:
        with self._lock:
            return list(self._readings.keys())

live_operations = LiveOperationsStore()