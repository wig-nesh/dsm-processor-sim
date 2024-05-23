from encoder import *

def Srg(MPSeqData):
    if MPSeqData in [encode_IRtoMPS(0x10),encode_IRtoMPS(0x20),encode_IRtoMPS(0x30),encode_IRtoMPS(0x40),encode_IRtoMPS(0x50),encode_IRtoMPS(0x60)]: return 0
    if MPSeqData in [encode_IRtoMPS(0x11),encode_IRtoMPS(0x21),encode_IRtoMPS(0x31),encode_IRtoMPS(0x41),encode_IRtoMPS(0x51),encode_IRtoMPS(0x61)]: return 1
    if MPSeqData in [encode_IRtoMPS(0x12),encode_IRtoMPS(0x22),encode_IRtoMPS(0x32),encode_IRtoMPS(0x42),encode_IRtoMPS(0x52),encode_IRtoMPS(0x62)]: return 2
    if MPSeqData in [encode_IRtoMPS(0x13),encode_IRtoMPS(0x23),encode_IRtoMPS(0x33),encode_IRtoMPS(0x43),encode_IRtoMPS(0x53),encode_IRtoMPS(0x63)]: return 3
    if MPSeqData in [encode_IRtoMPS(0x14),encode_IRtoMPS(0x24),encode_IRtoMPS(0x34),encode_IRtoMPS(0x44),encode_IRtoMPS(0x54),encode_IRtoMPS(0x64)]: return 4
    if MPSeqData in [encode_IRtoMPS(0x15),encode_IRtoMPS(0x25),encode_IRtoMPS(0x35),encode_IRtoMPS(0x45),encode_IRtoMPS(0x55),encode_IRtoMPS(0x65)]: return 5
    if MPSeqData in [encode_IRtoMPS(0x16),encode_IRtoMPS(0x26),encode_IRtoMPS(0x36),encode_IRtoMPS(0x46),encode_IRtoMPS(0x56),encode_IRtoMPS(0x66)]: return 6
    if MPSeqData in [encode_IRtoMPS(0x17),encode_IRtoMPS(0x27),encode_IRtoMPS(0x37),encode_IRtoMPS(0x47),encode_IRtoMPS(0x57),encode_IRtoMPS(0x67)]: return 7
    if MPSeqData in [encode_IRtoMPS(0x18),encode_IRtoMPS(0x28),encode_IRtoMPS(0x38),encode_IRtoMPS(0x48),encode_IRtoMPS(0x58),encode_IRtoMPS(0x68)]: return 8
    if MPSeqData in [encode_IRtoMPS(0x19),encode_IRtoMPS(0x29),encode_IRtoMPS(0x39),encode_IRtoMPS(0x49),encode_IRtoMPS(0x59),encode_IRtoMPS(0x69)]: return 9
    if MPSeqData in [encode_IRtoMPS(0x1a),encode_IRtoMPS(0x2a),encode_IRtoMPS(0x3a),encode_IRtoMPS(0x4a),encode_IRtoMPS(0x5a),encode_IRtoMPS(0x6a)]: return 10
    if MPSeqData in [encode_IRtoMPS(0x1b),encode_IRtoMPS(0x2b),encode_IRtoMPS(0x3b),encode_IRtoMPS(0x4b),encode_IRtoMPS(0x5b),encode_IRtoMPS(0x6b)]: return 11
    if MPSeqData in [encode_IRtoMPS(0x1c),encode_IRtoMPS(0x2c),encode_IRtoMPS(0x3c),encode_IRtoMPS(0x4c),encode_IRtoMPS(0x5c),encode_IRtoMPS(0x6c)]: return 12
    if MPSeqData in [encode_IRtoMPS(0x1d),encode_IRtoMPS(0x2d),encode_IRtoMPS(0x3d),encode_IRtoMPS(0x4d),encode_IRtoMPS(0x5d),encode_IRtoMPS(0x6d)]: return 13
    if MPSeqData in [encode_IRtoMPS(0x1e),encode_IRtoMPS(0x2e),encode_IRtoMPS(0x3e),encode_IRtoMPS(0x4e),encode_IRtoMPS(0x5e),encode_IRtoMPS(0x6e)]: return 14
    if MPSeqData in [encode_IRtoMPS(0x1f),encode_IRtoMPS(0x2f),encode_IRtoMPS(0x3f),encode_IRtoMPS(0x4f),encode_IRtoMPS(0x5f),encode_IRtoMPS(0x6f)]: return 15
    if MPSeqData==encode_IRtoMPS(0x70): return 0
    if MPSeqData==encode_IRtoMPS(0x71): return 1
    if MPSeqData==encode_IRtoMPS(0x72): return 2
    if MPSeqData==encode_IRtoMPS(0x73): return 3
    if MPSeqData==encode_IRtoMPS(0x74): return 4
    if MPSeqData==encode_IRtoMPS(0x75): return 5
    if MPSeqData==encode_IRtoMPS(0x76): return 6
    if MPSeqData==encode_IRtoMPS(0x77): return 7
    if MPSeqData==encode_IRtoMPS(0x78): return 8
    if MPSeqData==encode_IRtoMPS(0x79): return 9
    if MPSeqData==encode_IRtoMPS(0x7a): return 10
    if MPSeqData==encode_IRtoMPS(0x7b): return 11
    if MPSeqData==encode_IRtoMPS(0x7c): return 12
    if MPSeqData==encode_IRtoMPS(0x7d): return 13
    if MPSeqData==encode_IRtoMPS(0x7e): return 14
    if MPSeqData==encode_IRtoMPS(0x7f): return 15
    if MPSeqData==encode_IRtoMPS(0x80): return 0
    if MPSeqData==encode_IRtoMPS(0x81): return 1
    if MPSeqData==encode_IRtoMPS(0x82): return 2
    if MPSeqData==encode_IRtoMPS(0x83): return 3
    if MPSeqData==encode_IRtoMPS(0x84): return 4
    if MPSeqData==encode_IRtoMPS(0x85): return 5
    if MPSeqData==encode_IRtoMPS(0x86): return 6
    if MPSeqData==encode_IRtoMPS(0x87): return 7
    if MPSeqData==encode_IRtoMPS(0x88): return 8
    if MPSeqData==encode_IRtoMPS(0x89): return 9
    if MPSeqData==encode_IRtoMPS(0x8a): return 10
    if MPSeqData==encode_IRtoMPS(0x8b): return 11
    if MPSeqData==encode_IRtoMPS(0x8c): return 12
    if MPSeqData==encode_IRtoMPS(0x8d): return 13
    if MPSeqData==encode_IRtoMPS(0x8e): return 14
    if MPSeqData==encode_IRtoMPS(0x8f): return 15
    if MPSeqData==encode_IRtoMPS(0x90)+1: return 0
    if MPSeqData==encode_IRtoMPS(0x91)+1: return 1
    if MPSeqData==encode_IRtoMPS(0x92)+1: return 2
    if MPSeqData==encode_IRtoMPS(0x93)+1: return 3
    if MPSeqData==encode_IRtoMPS(0x94)+1: return 4
    if MPSeqData==encode_IRtoMPS(0x95)+1: return 5
    if MPSeqData==encode_IRtoMPS(0x96)+1: return 6
    if MPSeqData==encode_IRtoMPS(0x97)+1: return 7
    if MPSeqData==encode_IRtoMPS(0x98)+1: return 8
    if MPSeqData==encode_IRtoMPS(0x99)+1: return 9
    if MPSeqData==encode_IRtoMPS(0x9a)+1: return 10
    if MPSeqData==encode_IRtoMPS(0x9b)+1: return 11
    if MPSeqData==encode_IRtoMPS(0x9c)+1: return 12
    if MPSeqData==encode_IRtoMPS(0x9d)+1: return 13
    if MPSeqData==encode_IRtoMPS(0x9e)+1: return 14
    if MPSeqData==encode_IRtoMPS(0x9f)+1: return 15
    if MPSeqData==encode_IRtoMPS(0xa0)+1: return 0
    if MPSeqData==encode_IRtoMPS(0xa1)+1: return 1
    if MPSeqData==encode_IRtoMPS(0xa2)+1: return 2
    if MPSeqData==encode_IRtoMPS(0xa3)+1: return 3
    if MPSeqData==encode_IRtoMPS(0xa4)+1: return 4
    if MPSeqData==encode_IRtoMPS(0xa5)+1: return 5
    if MPSeqData==encode_IRtoMPS(0xa6)+1: return 6
    if MPSeqData==encode_IRtoMPS(0xa7)+1: return 7
    if MPSeqData==encode_IRtoMPS(0xa8)+1: return 8
    if MPSeqData==encode_IRtoMPS(0xa9)+1: return 9
    if MPSeqData==encode_IRtoMPS(0xaa)+1: return 10
    if MPSeqData==encode_IRtoMPS(0xab)+1: return 11
    if MPSeqData==encode_IRtoMPS(0xac)+1: return 12
    if MPSeqData==encode_IRtoMPS(0xad)+1: return 13
    if MPSeqData==encode_IRtoMPS(0xae)+1: return 14
    if MPSeqData==encode_IRtoMPS(0xaf)+1: return 15
    if MPSeqData==encode_IRtoMPS(0xb0)+1: return 0
    if MPSeqData==encode_IRtoMPS(0xb1)+1: return 1
    if MPSeqData==encode_IRtoMPS(0xb2)+1: return 2
    if MPSeqData==encode_IRtoMPS(0xb3)+1: return 3
    if MPSeqData==encode_IRtoMPS(0xb4)+1: return 4
    if MPSeqData==encode_IRtoMPS(0xb5)+1: return 5
    if MPSeqData==encode_IRtoMPS(0xb6)+1: return 6
    if MPSeqData==encode_IRtoMPS(0xb7)+1: return 7
    if MPSeqData==encode_IRtoMPS(0xb8)+1: return 8
    if MPSeqData==encode_IRtoMPS(0xb9)+1: return 9
    if MPSeqData==encode_IRtoMPS(0xba)+1: return 10
    if MPSeqData==encode_IRtoMPS(0xbb)+1: return 11
    if MPSeqData==encode_IRtoMPS(0xbc)+1: return 12
    if MPSeqData==encode_IRtoMPS(0xbd)+1: return 13
    if MPSeqData==encode_IRtoMPS(0xbe)+1: return 14
    if MPSeqData==encode_IRtoMPS(0xbf)+1: return 15