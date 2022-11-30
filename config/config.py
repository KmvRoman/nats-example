from attrs import define
from omegaconf import MISSING
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent


@define
class NatsSettings:
    user: str = MISSING
    password: str = MISSING
    ip_address: str = MISSING
    nats_port: str = MISSING


@define
class Config:
    nats: NatsSettings = NatsSettings()