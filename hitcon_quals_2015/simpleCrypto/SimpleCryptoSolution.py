import urllib
from cryptoUtils import *

username_entered= "{\"username\":\"aaaV,VadminV:trueAB"
userame_desired= "{\"username\":\"aaa\",\"admin\":true} "


print username_entered #aaaV,VadminV:trueAB

delta_user =  fixedXORRaw(username_entered, userame_desired)

cookie = "%7B%A5%7D%17%DBN%C7%D1%5B%F2%17%09C4%ED%1E%89%DAp%92%00%DD%A8%13%85l%D9%1A%F6%2F%FA%9A%E9%16%EB%F4%CE%3E%A1D%EA%01b%A0%29%0D%3C%C9%A3A%CE%FF%E2%A3%07p%D2%97%CD%D0%A2%D9%3C%3C%A0%92%E8KM%B7X%05%DDR%BCj%08%1B%D6%19%E0%C3%0BwI%D2%8B"
cookie_decode = urllib.unquote(cookie)
iv= cookie_decode[0:16]
json = cookie_decode[16:]

new_cookie  = iv + fixedXORRaw(delta_user, json[0:len(delta_user)])
print urllib.quote(new_cookie)