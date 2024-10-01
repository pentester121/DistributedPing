Installation on windows : 
1. download and install python3 latest version ( tested with 3.12.6 )
2. ```bash
   pip install requests ping3 python-socketio websocket-client eventlet #Or you can use pipx or pip3 or ....
3. edit the code and wite down your state ( esfahan , tehran , khorasan , etc.. )  and ISP ( hamhrah aval , Irancell , Rightel , Shatel , etc... ) and save the file .  
4. ```bash
   python client-win.py #run the program and leave it 


Installation on linux ( only tested on ubuntu and debian ) 
```bash
apt update && apt upgrade -y
apt install python3 python3-pip
pip install requests ping3 python-socketio websocket-client eventlet
