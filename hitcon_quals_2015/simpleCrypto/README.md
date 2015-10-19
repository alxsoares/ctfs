#Simple Crypto solution

## Intro
SimpleCrypto was the easiest (least amount of point) crypto problem of the HITCON CTF Quals 2015. 

It comes as a simple ruby/sinatra web application that asks you to login, creates a session cookie and then check if there's a flag "admin:true" in your cookie. There's no login per se, just a session cookie oracle. 

## Principles of the attack
The cryptography being used for the sessions cookie is a flavor of AES used a CFB mode. Looking at the size of the IV (initialization vector) we are dealing with a 128 bits version of AES (ie a block is 16 bytes). As a super quick refresher, the AES cipher primitive works on block of data, here 16 bytes at the time, the *mode* (here CFB) is basically telling how you how to expand that behaviour to a stream of data longer than 16 bytes. Looking at wikipedia ([CFB mode](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Feedback_.28CFB.29)) one can see how CFB works : you cipher the IV, xor the first 16 bytes of plain text with the ciphered xor; it gives you the first 16 bytes of ciphertext and also what's going to get feed in the ciphering primitive for the next 16 bytes block, and so on. 
The flaw in this implementation is somewhat obvious: there's no verification of the integrity of the session cookie (no signature, HMAC, etc.) and basically the CFB mode generates a stream of pseudo-random bytes that are being xored to the plaintext. However, if you know the plain text being ciphered, a simple xor can modify it to whatever you want; the modification you made will propagate to the next block (as the cipher text is used to generate the next 16 pseudo-random bytes) but that's pretty much it. 

## The attack
### Running the code
Something that usually really useful is being able to run the code on your machine so you can debug information and perform a dynamic analysis, as opposed as trying to guess what the code you have is doing.For instance you want to know what the JSON blob looks like before being ciphered (so you can mess with it and make sure your modification results in what you think they will). 
Disclaimer: I have no idea what ruby and sinatra do, how people use it, and so on. 

1.  Install ruby (find the windows installer, the apt-get that works, etc.) 
2.  Install sinatra (use "gem" to install sinatra, the command is `gem install sinatra` 
3.  Try to run it (and fail). Apparently sinatra/cookies doesn't get installed :(
4.  Google it and find out you need to gem install `sinatra-contrib` (go figure) 
5.  Run it. Now it fails because files are missing.
6.  Create a fake key and a fake flag, potentially change their path in the .rb file to match your configuration. 
7.  Runs it. It works! But returns immediately :(
8.  More google: the architecture of the code is a bit more fancier than a simple hello world (using modular Sinatra apparently), and therefore this SinatraApp patterns requires a bit more massaging to run successfully.  So you need a `config.ru` file that you run with the `rackup` command (sure.... see commited files for the details) 
9.  `rackup config.ru`
10.  Success! 
11.  Now you can add some debugging code for more information about what's going on under the hood (like print json) 

### Yeah at last the attack!
Looking at the verification code, we need a valid JSON blob that contains a username, and ideally admin:true. The fields 'password' and 'db' don't matter. 
We settle with a target session cookie looking like :
`{"username":"aaa", "admin": true}` 
The reason: up to the last 'a' of the username, we fit everything in a 16 byte block that will remain untouched, the remaining data fits in a second 16 bytes block, and then, nothing more! (so no cascading effect because we tampered with the second AES block).
So the process: 

1. Go to the website, register the username : `aaaV,VadminV:trueAB` and any password you fancy. Note: I replaced the '"' by 'V' so that they don't get escaped by the JSON parser, 'A' will be a '}' and 'B' will be a ' '. The last two are probably useless and could have been "} " directly but helped me visualise the process and make sure some special character doesn't get escaped without me realising it.  
2. Grab the cookie you get (I'm using the chrome extension "Edit This Cookie"). 
3. Find the XOR "difference" between `{"username":"aaaV,VadminV:trueAB", ......`  and `{"username":"aaa","admin":true} `, xor that difference to the cookie you have (because `A xor B xor C` is the same as `A xor C xor B`) and truncate the remaining part of the cookie (the one beyond those first 32 bytes (and the 16 bytes of IV that are at the beginning of the cookie)).
4. Replace the old cookie with the new one.
5. Get the flag !

## Conclusion
You probably want to add a signature to your session cookie so that any shenanigans would be detected and probably goggle what is the best practice in those conditions rather than coming up with your own exotic session cookie. 