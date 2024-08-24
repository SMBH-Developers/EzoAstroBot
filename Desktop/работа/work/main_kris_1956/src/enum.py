from enum import Enum


class Status(Enum):
    ALIVE = 'alive'
    BLACK_LIST = 'black_list'
    ID_INVALID = 'id_invalid'
    PAYED = 'payed'
    EXPECT = 'expect'
    TOO_MANY_FLOOD = 'too_many_flood'
    MANUAL_PROCESSING = 'manual_processing'
    TEENAGER = 'teenager'

    PEER_FLOOD = 'peer_flood'
