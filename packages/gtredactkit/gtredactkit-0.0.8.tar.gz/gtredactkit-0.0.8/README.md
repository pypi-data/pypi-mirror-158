# gtredactkit 🔐📝

>This repository is an alternative of [PyRedactKit](https://github.com/brootware/PyRedactKit) an open source sensitive data redaction tool with support for redacting name.
<p align="center">
  <img src="./images/asciiRedact.png" alt="Python Redactor Kit!"/>
<br />
<i>A fork of PyRedactKit to redact and unredact sensitive information like ip addresses, emails and domains.</i>
<code>pip install --upgrade gtredactkit && redactor</code>
</p>

<p align="center">
   <!-- <img alt="PyPI - Downloads" src="https://pepy.tech/badge/gtredactkit/month"> -->
   <!-- <img alt="PyPI - Downloads" src="https://pepy.tech/badge/gtredactkit"> -->
   <!-- <a href="https://twitter.com/brootware"><img src="https://img.shields.io/twitter/follow/brootware?style=social" alt="Twitter Follow"></a> -->
   <!-- <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/gtredactkit"> <img alt="PyPI" src="https://img.shields.io/pypi/v/gtredactkit"> -->
   <!-- <a href="https://sonarcloud.io/summary/new_code?id=brootware_gtredactkit"><img src="https://sonarcloud.io/api/project_badges/measure?project=brootware_gtredactkit&metric=alert_status" alt="reliability rating"></a> -->
   <!-- <img alt="GitHub Workflow Status" src="https://img.shields.io/github/workflow/status/brootware/gtredactkit/CI?label=CI"> -->
</p>

## Features

Redacts and Unredacts the following from your text files. 📄 ✍️

- sg nric 🆔
- credit cards 🏧
- dns 🌐
- emails ✉️
- ipv4 📟
- ipv6 📟
- base64 🅱️

## Pre-requisites

- [Python3](https://www.python.org/downloads/) installed
- [pip](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) installed

## How to use

Demo:
![demo](./images/pyredact.gif)

Clone the repo

```bash
git clone https://github.com/brootware/gtredactkit.git && cd gtredactkit
```

Redact from terminal

```bash
python gtredactkit.py 'this is my ip:127.0.0.1. my email is broot@outlook.com. secret link is github.com'
```

Redact a single file

```bash
python gtredactkit.py -f test.txt 
```

Unredact the file

```bash
python gtredactkit.py -f redacted_test.txt -u .hashshadow_test.txt.json 
```

Redact using custom regex pattern

```bash
python gtredactkit.py -f file -c custom.json
```

```bash
$ python gtredactkit.py ip_test.txt 

  ________ __    __________           .___              __     ____  __.__  __   
 /  _____//  |_  \______   \ ____   __| _/____    _____/  |_  |    |/ _|__|/  |_ 
/   \  __\   __\  |       _// __ \ / __ |\__  \ _/ ___\   __\ |      < |  \   __\
\    \_\  \  |    |    |   \  ___// /_/ | / __ \\  \___|  |   |    |  \|  ||  |  
 \______  /__|    |____|_  /\___  >____ |(____  /\___  >__|   |____|__ \__||__|  
        \/               \/     \/     \/     \/     \/               \/                                                                                   
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
                    |P|o|w|e|r|e|d| |b|y| |B|r|o|o|t|w|a|r|e|
                    +-+-+-+-+-+-+-+ +-+-+ +-+-+-+-+-+-+-+-+-+
            
    https://github.com/brootware
    https://brootware.github.io                                                                             
    
[ + ] Processing starts now. This may take some time depending on the file size. Monitor the redacted file size to monitor progress
[ + ] No option supplied, will be redacting all the sensitive data supported
[ + ] Redacted 10064 targets...
[ + ] Redacted results saved to ./redacted_ip_test.txt
```

Sample Result:

```txt
John, please get that article on b8bd54d3-34ee-4f31-8b2b-0d729929e8aa to me by 5:00PM on Jan 9th 2012. 4:00 would be ideal, actually. If you have any questions, You can reach me at(519)-236-2723 or get in touch with my associate at 7b3c7641-4b09-4e00-8e02-0e68e47b0ded.
All rights reserved. Printed in the United States of America. No part of this book may be used or reproduced in any manner whatsoever without written permission except in the case of brief quotations embodied in critical articles and reviews. For information address HarperCollins Publishers, 10 East 53rd Street, New York, NY 10022. His name is David. I met him and John last week. Gowtham Teja Kanneganti is a good student. I was born on Oct 4, 1995. My Indian mobile number is +91-7761975545. After coming to USA I got a new number +1-405-413-5255. I live on 1003 E Brooks St, Norman, Ok, 73071. I met  a child, who is playing with josh.
this is my IP: 49f62b69-98c1-4f7b-87d1-8f7f6723f44e
My router is : e83747e7-521f-4f44-982f-0de1b2be4d19
1d6716c8-1f1b-4e90-a62e-a0be14417e78
0a5671c0-5de9-4198-a731-aff33e22a653
ce336df7-e58e-4297-9644-c8199f5e38cf
020fc1b6-6035-474b-8f6d-7c0890e94e6b
c0f238ef-cc94-48e7-9c98-e8883d9dd947
63d76480-e7d4-4ebf-9101-04b9e70ddd8d
c33d0c2a-8d87-48c7-b846-20f938a8f902
My email is c1f04434-c7e9-4d9a-a0a9-7a0651a046cd
a36aab91-9c25-4221-a7a4-a0ff01c8d752
this is my IP: 0c15d46a-67e7-4906-9dd4-ee520ab91b47
My router is: ca00a810-4ff8-4880-8983-9b6dbbeb06f8
12830911-20a9-45f8-ae04-9a4f807ee3b8
6b042458-83a2-4ce9-b029-c62e83180719
e1e8c2f3-5a9f-49ff-bc3e-cefe0f842274
611ccb57-ea69-41b6-946d-1284a1a345d0
492b72d2-cf23-477f-a02e-78bb04ad13ab
Base64 data
dd4e5123-c87a-4ff0-ba40-f7f601270484
d660b76c-c2ce-4401-90a6-35277a2def23
bbde787d-f515-4fcb-a583-e4d3d8185ca3
10c5d831-2728-45d0-8810-c0e6bb40a4c9
a5bac8dd-bd89-4bc8-94a9-b510beb88d6a
Singapore NRIC
c9a85803-e706-4322-99a0-e1c76705c4e8
05759c8a-a2e7-46d8-8739-bb6c97fb8117
0b29e289-a3af-4cbc-92d6-d044601a2458
be05fce6-7464-43cb-9164-914f8e63ff5c
b857a0c2-b108-44d5-b3ea-f0bc05e36dee
5eccbebc-f2a9-4420-a436-66f08a6f63c5
Card_Number,Card_Family,Credit_Limit,Cust_ID
b35843a8-6483-44ec-884c-868dd3296d34,Premium,530000,CC67088
d392cc27-d20b-4876-ae64-4196c5b05dd3,Gold,18000,CC12076
acb4d6d7-1c7c-42d1-a02c-6b229e2a9e4a,Premium,596000,CC97173
b92d943a-73d8-4318-955d-2e364836f641,Gold,27000,CC55858
e0b66cbd-6174-4491-b938-408a47d38fb9,Platinum,142000,CC90518
6b73619c-bcbf-4509-a064-1fb110f5dd45,Gold,50000,CC49168
24f31233-cba6-4f6a-a2d6-0ce49952b2cb,Premium,781000,CC66746
```

To redact multiple files from a directory and place it in a new directory

```bash
python gtredactkit.py dir_test -d redacted_dir
```

## Optional Help Menu as below

```bash
usage: redactor [-h] [-f FILE [FILE ...]] [-u UNREDACT] [-d DIROUT] [-c CUSTOMFILE] [-r] [-e EXTENSION] [text ...]

Supply a sentence or paragraph to redact sensitive data from it. Or read in a file or set of files with -f to redact

positional arguments:
  text                  Redact sensitive data of a sentence from command prompt. (default: None)

optional arguments:
  -h, --help            show this help message and exit
  -f FILE [FILE ...], --file FILE [FILE ...]
                        Path of a file or a directory of files. (default: None)
  -u UNREDACT, --unredact UNREDACT
                        Option to unredact masked data. Usage: redactor -f [redacted_file] -u [.hashshadow.json] (default: None)
  -d DIROUT, --dirout DIROUT
                        Output directory of the file. Usage: redactor -f [file/filestoredact] -d [redacted_dir] (default: None)
  -c CUSTOMFILE, --customfile CUSTOMFILE
                        User defined custom regex pattern for redaction. Usage: redactor -f [file/filestoredact] -c [customfile.json] (default: None)
  -r, --recursive       Search through subfolders (default: True)
  -e EXTENSION, --extension EXTENSION
                        File extension to filter by. (default: )
```
