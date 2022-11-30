import pathlib
import cattrs
from omegaconf import OmegaConf
from config.config import Config


def parse_config(path_to_config: str | pathlib.Path) -> Config:
    dictionary_config = OmegaConf.to_container(OmegaConf.merge(
        OmegaConf.load(path_to_config),
        OmegaConf.structured(Config)
    ), resolve=True)
    return cattrs.structure(dictionary_config, Config)