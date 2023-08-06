__version__ = '0.1.0'

from dataclasses import dataclass, field
from math import ceil
from anyascii import anyascii

basic_table = ("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?"
       "¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ`¿abcdefghijklmnopqrstuvwxyzäöñüà")
extended_table = ("````````````````````^```````````````````{}`````\\````````````[~]`"
       "|````````````````````````````````````€``````````````````````````")

@dataclass
class SmsMessage:
    body: str
    twilio: bool = False
    encoded_text: str = field(init=False)
    encoded_bytes: bytearray = field(init=False)
    length: int = field(init=False)
    segments: int = field(init=False)
    def __post_init__(self):
        self.encoded_text = SmsMessage.message_encode(self.body).decode()
        self.encoded_bytes = bytes(SmsMessage.message_encode(self.body))
        self.length = len(self.encoded_bytes)
        self.segments = ceil(self.length/(153 if self.twilio and self.length>160 else 160))
    
    def __repr__(self):
        return self.encoded_text
    
    """Encode a unicode string to a bytearray of SMS characters"""
    def message_encode(plaintext: str) -> bytearray:
        literatedtext = anyascii(plaintext)
        charbytes = bytearray()
        for character in literatedtext:
            character_index = basic_table.find(character);
            if character_index != -1:
                charbytes.append(character_index)
                continue
            character_index = extended_table.find(character)
            if character_index != -1:
                charbytes.append(27) #escape to extended table
                charbytes.append(character_index)
        return charbytes

    """Encode python string into a GSM-7 python encoded string"""
    def encode(string: str) -> str:
        return SmsMessage.message_encode(string).decode()