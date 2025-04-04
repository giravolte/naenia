# The contents of this file are subject to the BitTorrent Open Source License
# Version 1.1 (the License).  You may not copy or use this file, in either
# source code or executable form, except in compliance with the License.  You
# may obtain a copy of the License at http://www.bittorrent.com/license/.
#
# Software distributed under the License is distributed on an AS IS basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied.  See the License
# for the specific language governing rights and limitations under the
# License.

# Written by Petru Paler
# Updated by Mattia (@giravolte)

DICT_DELIM = b"d"
INT_DELIM  = b"i"
LIST_DELIM = b"l"
BYTE_SEP   = b":"
END_DELIM  = b"e"

class BError(Exception):
    """
    Base class for errors.

    Used for exceptions raised during the
    encoding or decoding of bencoded data.
    """
    pass

def decode_int(x, i):
    i += 1
    end = x.index(END_DELIM, i)
    n = int(x[i:end])
    if x[i:i+2] == b"-0":
        raise ValueError
    elif x[i:i+1] == b"0" and end != i+1:
        raise ValueError
    return (n, end+1)

def decode_str(x, i):
    sep = x.index(BYTE_SEP, i)
    n = int(x[i:sep])
    if x[i:i+1] == b"0" and sep != i+1:
        raise ValueError
    sep += 1
    return (x[sep:sep+n], sep+n)

def decode_list(x, i):
    l = []; i += 1
    while x[i:i+1] != END_DELIM:
        v, i = _decode[x[i:i+1]](x, i)
        l.append(v)
    return (l, i+1)

def decode_dict(x, i):
    d = {}; i += 1; last_k = None
    while x[i:i+1] != END_DELIM:
        k, i = decode_str(x, i)
        if last_k is not None and k <= last_k:
            raise ValueError
        last_k = k
        d[k], i = _decode[x[i:i+1]](x, i)
    return (d, i+1)

_decode = {}
_decode[INT_DELIM]  = decode_int
_decode[LIST_DELIM] = decode_list
_decode[DICT_DELIM] = decode_dict
_decode[b"0"]       = decode_str
_decode[b"1"]       = decode_str
_decode[b"2"]       = decode_str
_decode[b"3"]       = decode_str
_decode[b"4"]       = decode_str
_decode[b"5"]       = decode_str
_decode[b"6"]       = decode_str
_decode[b"7"]       = decode_str
_decode[b"8"]       = decode_str
_decode[b"9"]       = decode_str

def bdecode(x: bytes) -> int | dict | list | bytes:
    """Decodes a bencoded byte string into its corresponding Python object."""
    try:
        obj, l = _decode[x[0:1]](x, 0)
    except (LookupError, TypeError, ValueError):
        raise BError("Invalid bencoded string.")
    if l != len(x):
        raise BError("Invalid bencoded string.")
    return obj

class Bencached:
    __slots__ = ["bencoded"]

    def __init__(self, s):
        self.bencoded = s

def encode_bencached(x, e):
    e.append(x.bencoded)

def encode_int(x, e):
    e.extend((INT_DELIM, str(x).encode("utf-8"), END_DELIM))

def encode_bool(x, e):
    encode_int(1 if x else 0, e)

def encode_bytes(x, e):
    e.extend((str(len(x)).encode("utf-8"), BYTE_SEP, x))

def encode_string(x, e):
    encode_bytes(x.encode("utf-8"), e)

def encode_list(x, e):
    e.append(LIST_DELIM)
    for i in x:
        _encode[type(i)](i, e)
    e.append(END_DELIM)

def encode_dict(x, e):
    e.append(DICT_DELIM)
    for k, v in sorted(x.items()):
        try:
            k = k.encode("utf-8")
        except AttributeError:
            pass
        e.extend((str(len(k)).encode("utf-8"), BYTE_SEP, k))
        _encode[type(v)](v, e)
    e.append(END_DELIM)

_encode = {}
_encode[Bencached] = encode_bencached
_encode[int]       = encode_int
_encode[bool]      = encode_bool
_encode[bytes]     = encode_bytes
_encode[str]       = encode_string
_encode[list]      = encode_list
_encode[dict]      = encode_dict

def bencode(x: int | bool | bytes | str | list | dict | Bencached) -> bytes:
    """Encodes a Python object into its corresponding bencode format."""
    e = []
    _encode[type(x)](x, e)
    return b"".join(e)

__all__ = [
    "bdecode",
    "bencode",
    "Bencached"
]