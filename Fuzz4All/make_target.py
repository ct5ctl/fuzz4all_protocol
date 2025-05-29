from typing import Any, Dict, List, Optional, Tuple, Union

from Fuzz4All.target.C.C import CTarget
from Fuzz4All.target.CPP.CPP import CPPTarget
from Fuzz4All.target.GO.GO import GOTarget
from Fuzz4All.target.JAVA.JAVA import JAVATarget
from Fuzz4All.target.QISKIT.QISKIT import QiskitTarget
from Fuzz4All.target.SMT.SMT import SMTTarget
from Fuzz4All.target.target import Target


from Fuzz4All.target.FTP.FTP import FTPTarget
from Fuzz4All.target.HTTP.HTTP import HTTPTarget
from Fuzz4All.target.DICOM.DICOM import DICOMTarget
from Fuzz4All.target.QUIC.QUIC import QUICTarget
from Fuzz4All.target.RTSP.RTSP import RTSPTarget

from Fuzz4All.target.DTLS.TinyDTLS import TinyDTLSTarget
from Fuzz4All.target.SMTP.Exim import EximTarget
from Fuzz4All.target.SIP.Kamailio import KamailioTarget
from Fuzz4All.target.QUIC.NGTCP2 import NGTCP2Target


def make_target(kwargs: Dict[str, Any]) -> Target:
    """Make a target from the given command line arguments."""
    language = kwargs["language"]
    if language == "cpp":  # G++
        return CPPTarget(**kwargs)
    elif language == "c":  # GCC
        return CTarget(**kwargs)
    elif language == "qiskit":  # Qiskit
        return QiskitTarget(**kwargs)
    elif language == "smt2":  # SMT solvers
        return SMTTarget(**kwargs)
    elif language == "go":  # GO
        return GOTarget(**kwargs)
    elif language == "java":  # Java
        return JAVATarget(**kwargs)
    elif language == "ftp":
        return FTPTarget(**kwargs)
    elif language == "http":
        return HTTPTarget(**kwargs)
    elif language == "dicom":
        return DICOMTarget(**kwargs)
    elif language == "quic":
        return QUICTarget(**kwargs)
    elif language == "ngtcp2":
        return NGTCP2Target(**kwargs)
    elif language == "dtls":
        return TinyDTLSTarget(**kwargs)
    elif language == "smtp":
        return EximTarget(**kwargs)
    elif language == "sip":
        return KamailioTarget(**kwargs)
    elif language == "rtsp":
        return RTSPTarget(**kwargs)
    else:
        raise ValueError(f"Invalid target {language}")


def make_target_with_config(config_dict: Dict[str, Any]) -> Target:
    """Create a target from a configuration dictionary."""

    llm = config_dict["llm"]
    fuzzing = config_dict["fuzzing"]
    target = config_dict["target"]

    target_compat_dict = {
        # simple mapping
        "language": target["language"],
        "folder": fuzzing["output_folder"],
        "bs": llm.get("batch_size", 1),
        "temperature": llm.get("temperature", 1.0),
        "device": llm.get("device", "cuda"),
        "model_name": llm.get("model_name", "bigcode/starcoder"),
        "max_length": llm.get("max_length", 1024),
        "use_hw": fuzzing.get("use_hand_written_prompt", False),
        "no_input_prompt": fuzzing.get("no_input_prompt", False),
        "prompt_strategy": fuzzing.get("prompt_strategy", 0),
        "level": fuzzing.get("log_level", 0),
        # compatibility conversion
        # signalling the target to use the config file
        "template": "fuzzing_with_config_file",
        "config_dict": config_dict,
        "target_name": fuzzing.get("target_name", "target"),
    }

    # print the target config
    print("=== Target Config ===")
    for k, v in target_compat_dict.items():
        print(f"{k}: {v}")
    print("====================")

    if target["language"] == "cpp":
        return CPPTarget(**target_compat_dict)
    elif target["language"] == "c":
        return CTarget(**target_compat_dict)
    elif target["language"] == "qiskit":
        return QiskitTarget(**target_compat_dict)
    elif target["language"] == "smt2":
        return SMTTarget(**target_compat_dict)
    elif target["language"] == "go":
        return GOTarget(**target_compat_dict)
    elif target["language"] == "java":
        return JAVATarget(**target_compat_dict)
    elif target["language"] == "ftp":
        return FTPTarget(**target_compat_dict)
    elif target["language"] == "http":
        return HTTPTarget(**target_compat_dict)
    elif target["language"] == "dicom":
        return DICOMTarget(**target_compat_dict)
    elif target["language"] == "quic":
        return QUICTarget(**target_compat_dict)
    elif target["language"] == "rtsp":
        return RTSPTarget(**target_compat_dict)
    elif target["language"] == "smtp":
        return EximTarget(**target_compat_dict)
    elif target["language"] == "sip":
        return KamailioTarget(**target_compat_dict)
    elif target["language"] == "dtls":
        return TinyDTLSTarget(**target_compat_dict)
    elif target["language"] == "ngtcp2":
        return NGTCP2Target(**target_compat_dict)
    else:
        raise ValueError(f"Invalid target {target['language']}")
