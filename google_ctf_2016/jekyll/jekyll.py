import webapp2
import struct
import base64
from flag import FLAG

def mixInv(a, b, c):
    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

    c ^= b >> 15
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a << 10)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >>  3
    a += b+c; a &= 0xFFFFFFFF;
    c ^= b >>  5
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a << 16)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >> 12
    a += b+c; a &= 0xFFFFFFFF;
    c ^= b >> 13
    c += a+b; c &= 0xFFFFFFFF;
    b ^=(a <<  8)&0xFFFFFFFF
    b += c+a; b &= 0xFFFFFFFF;
    a ^= c >> 13
    a += b+c; a &= 0xFFFFFFFF;




    print "Jekyl{}".format(hex(b))








    print "mix ", hex(a),hex(b),hex(c)
    return a, b, c

def mix2(a, b, c):
    a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

    a -= b+c; a &= 0xFFFFFFFF;

    a ^= c >> 13
    b -= c+a; b &= 0xFFFFFFFF;
    b ^=(a <<  8)&0xFFFFFFFF
    #print "Jekyl{}".format(hex(b))
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
    a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
    b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
    a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
    b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
    c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15

    #print "mix ", hex(a),hex(b),hex(c)
    return a, b, c

def jekyll32(data, seed):
    def mix(a, b, c):
        a &= 0xFFFFFFFF; b &= 0xFFFFFFFF; c &= 0xFFFFFFFF;

        a -= b+c; a &= 0xFFFFFFFF;

        a ^= c >> 13
        b -= c+a; b &= 0xFFFFFFFF;
        b ^=(a <<  8)&0xFFFFFFFF
        #print "Jekyl{}".format(hex(b))
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 13
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >> 12
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 16)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >>  5
        a -= b+c; a &= 0xFFFFFFFF; a ^= c >>  3
        b -= c+a; b &= 0xFFFFFFFF; b ^=(a << 10)&0xFFFFFFFF
        c -= a+b; c &= 0xFFFFFFFF; c ^= b >> 15

        print "mix ", hex(a),hex(b),hex(c)
        return a, b, c

    a = 0x9e3779b9
    b = a
    c = seed
    length = len(data)

    hexStr = ""
    for ca in data:
        hexStr+= (hex(ord(ca)))
    print hexStr

    keylen = length
    #print keylen
    while keylen >= 12:
        values = struct.unpack('<3I', data[:12])
        a += values[0]
        b += values[1]
        c += values[2]

        print "v1: %s"%hex(values[0])
        print "v2: %s"%hex(values[1])
        print "v3: %s"%hex(values[2])
    #    print 'loop'
    #    print hex(a),hex(b),hex(c)

        a, b, c = mix(a, b, c)
        keylen -= 12
        data = data[12:]

    c += length

    data += '\x00' * (12-len(data))
    values = struct.unpack('<3I', data)

    a += values[0]
    b += values[1]
    c += values[2]

    print "yo"


    a, b, c = mix(a, b, c)

    return c

def jekyll(data):
    return jekyll32(data, 0x60061e) | (jekyll32(data, 0x900913) << 32)

class AdminPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'

        cookie = self.request.cookies.get('admin')

        if cookie is not None and jekyll(base64.b64decode(cookie)) == 0x203b1b70cb122e29:
            self.response.write('Hello admin!\n'+FLAG)
        else:
            self.response.write('Who are you?')


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Hello, World!')
        self.response.set_cookie('admin', 'value', max_age=360, path='/',
                    domain='localhost:8080', secure=True)

app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/admin', AdminPage),
], debug=False)

def main():
    from paste import httpserver
    httpserver.serve(app, host='127.0.0.1', port='8080')

def swap32(i):
    return struct.unpack("<I", struct.pack(">I", i))[0]
def swapAndHex(v):
    v = swap32(v)
    v = hex(v)[2:]
    if (v[-1] == "L"): v = v[0:-1]
    return v


if __name__ == '__main__':
    main()

    v1=0x7927aad
    v2=0xb48464f
    v3=0xd2bb2554

    v1=swapAndHex(v1)
    v2=swapAndHex(v2)
    v3=swapAndHex(v3)



    strHex = v1 + v2 + v3
    print strHex
    print base64.b64encode(strHex.decode('hex'))
    print hex(jekyll(strHex.decode('hex')))
