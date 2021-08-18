#
#  Reads ZIMPOL3 Binary Data (Z3BD) file and returnd tha data as numpy array
# 
#  Parameters
#
#    fname      : Dile name  
#    header     : Directory with header entries
#    get_header : If True only the header is read and returnd instad of the array 
# 

import numpy, re


def z3readbd(fname, header={}, get_header=False):
    #

    SOH = '\001'
    STX = '\002'
    ETX = '\003'

    bSOH = b'\001'
    bSTX = b'\002'
    bETX = b'\003'

    NADT = {'f32': numpy.float32, 'f64': numpy.float64,
            's8': numpy.int8, 's16': numpy.int16,
            's32': numpy.int32, 's64': numpy.int64,
            'u8': numpy.uint8, 'u16': numpy.uint16,
            'u32': numpy.uint32, 'u64': numpy.uint64}

    fid = open(fname, mode="rb")

    bh = fid.read(1)

    if bh != bSOH:
        print("Error: z3readbd: Wrong file format!")
        fid.close()
        return

    # read header
    s = str(bh, 'iso-8859-1')
    # read until STX
    while not STX in s:
        br = fid.read(1)
        assert len(br) == 1, 'STX not found'
        s += str(br, 'iso-8859-1')
        #
    # scan header
    m = re.match('\001(?P<ts>[usf][123468]+)(?P<dl>\[.*\])(?P<al>[^\002]*)\002', s)
    assert m != None, 'invalid header'
    ts = m.group('ts')  # type size
    dl = eval(m.group('dl'))  # dimension list
    al = m.group('al')  # attribute list  ### is str

    ### print('z3fread ts=',ts,'dl=',dl,'al=',al,'m.span()=',m.span()) ####
    #

    # create  header directory
    s = al;
    i, n = 0, len(s)
    while i < n:
        m = re.match(
            '^ (?P<nam>[a-zA-Z][a-zA-Z0-9_]*)=(?P<val>({[^{}]*({[^{}]*})*[^{}]*})|("[^"]*")|([-+]?[0-9]+(\.[0-9]+)?)([eE][-+]?[0-9]+)?)',
            s[i:n])
        if not m: print('fread_bd al i,n,s=', i, n, s); break  #####
        nam = m.group('nam')
        val = m.group('val')
        i += m.span()[1]
        if ((val[0] == '{') or (val[0] == '"')):
            v = val[1:-1]
        else:
            v = eval(val)
        #
        header.update({nam: v})

    if get_header:
        fid.close()
        return header

    # determine size of array data string
    es = int(ts[1:])
    ds = es // 8
    for le in dl: ds *= le
    #
    # read binary data as string    
    bd = fid.read(ds)
    if not len(bd) == ds:
        print('fread_bd len(bd),ds=', len(bd), ds)  ####

    #
    # create ndarray
    shape = tuple(dl)
    nadt = NADT[ts]
    ### print('z3fread shape,nadt=',shape,nadt) ####
    ard = numpy.ndarray(shape, dtype=nadt, buffer=bd, order='C')
    #
    # swap bytes to convert big endian to little endian
    # creating a copy of type Array
    ar = ard.byteswap().view()
    #
    #
    assert len(ar) == len(ard), 'duplicating and byteswapping of array failed'
    #
    betx = fid.read(1)
    assert betx == bETX, 'ETX missing or misplaced; etx=' + str(ord(etx))
    fid.close()
    #
    return ar
#