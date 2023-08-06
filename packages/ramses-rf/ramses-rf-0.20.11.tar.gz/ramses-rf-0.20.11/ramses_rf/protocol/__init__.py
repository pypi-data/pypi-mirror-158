#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""RAMSES RF - a RAMSES-II protocol decoder & analyser."""

# noqa: F401, pylint: disable=unused-import

from logging import Logger

from .address import Address, is_valid_dev_id
from .command import CODE_API_MAP, Command, FaultLog, Priority
from .const import (
    SZ_DEVICE_ROLE,
    SZ_DOMAIN_ID,
    SZ_ZONE_CLASS,
    SZ_ZONE_IDX,
    SZ_ZONE_MASK,
    SZ_ZONE_TYPE,
    __dev_mode__,
)
from .exceptions import (
    CorruptStateError,
    ExpiredCallbackError,
    InvalidAddrSetError,
    InvalidPacketError,
)
from .logger import set_logger_timesource, set_pkt_logging
from .message import Message
from .packet import _PKT_LOGGER, Packet
from .protocol import create_msg_stack
from .ramses import CODES_BY_DEV_SLUG, CODES_SCHEMA
from .schema import PACKET_LOG, PACKET_LOG_SCHEMA, SERIAL_CONFIG_SCHEMA, SERIAL_PORT
from .transport import SZ_POLLER_TASK, create_pkt_stack

# skipcq: PY-W2000
from .const import (  # noqa: F401, isort: skip, pylint: disable=unused-import
    I_,
    RP,
    RQ,
    W_,
    F9,
    FA,
    FC,
    FF,
    DEV_ROLE,
    DEV_ROLE_MAP,
    DEV_TYPE,
    DEV_TYPE_MAP,
    ZON_ROLE,
    ZON_ROLE_MAP,
)

# skipcq: PY-W2000
from .const import (  # noqa: F401, isort: skip, pylint: disable=unused-import
    _0001,
    _0002,
    _0004,
    _0005,
    _0006,
    _0008,
    _0009,
    _000A,
    _000C,
    _000E,
    _0016,
    _0100,
    _0150,
    _01D0,
    _01E9,
    _0404,
    _0418,
    _042F,
    _0B04,
    _1030,
    _1060,
    _1081,
    _1090,
    _1098,
    _10A0,
    _10B0,
    _10D0,
    _10E0,
    _10E1,
    _10E2,
    _1100,
    _11F0,
    _1260,
    _1280,
    _1290,
    _1298,
    _12A0,
    _12B0,
    _12C0,
    _12C8,
    _12F0,
    _1300,
    _1470,
    _1F09,
    _1F41,
    _1F70,
    _1FC9,
    _1FCA,
    _1FD0,
    _1FD4,
    _2210,
    _2249,
    _22C9,
    _22D0,
    _22D9,
    _22E0,
    _22E5,
    _22E9,
    _22F1,
    _22F2,
    _22F3,
    _22F4,
    _22F7,
    _22F8,
    _22B0,
    _2309,
    _2349,
    _2389,
    _2400,
    _2401,
    _2410,
    _2411,
    _2420,
    _2D49,
    _2E04,
    _2E10,
    _30C9,
    _3110,
    _3120,
    _313E,
    _313F,
    _3150,
    _31D9,
    _31DA,
    _31E0,
    _3200,
    _3210,
    _3220,
    _3221,
    _3222,
    _3223,
    _3B00,
    _3EF0,
    _3EF1,
    _4401,
    _PUZZ,
)


def set_pkt_logging_config(**config) -> Logger:
    set_pkt_logging(_PKT_LOGGER, **config)
    return _PKT_LOGGER
