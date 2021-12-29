echo ">> FETCHING UPSTREAM..."
git clone https://github.com/AsmSafone/MusicPlayer /MusicPlayer
echo ">> INSTALLING REQUIREMENTS..."
cd /MusicPlayer
pip3 install -U -r requirements.txt
echo ">> STARTING MUSIC PLAYER USERBOT..."
clear
echo "
  __  __           _        _____  _                       
 |  \/  |         (_)      |  __ \| |                      
 | \  / |_   _ ___ _  ___  | |__) | | __ _ _   _  ___ _ __ 
 | |\/| | | | / __| |/ __| |  ___/| |/ _` | | | |/ _ \ '__|
 | |  | | |_| \__ \ | (__  | |    | | (_| | |_| |  __/ |   
 |_|  |_|\__,_|___/_|\___| |_|    |_|\__,_|\__, |\___|_|   
                                            __/ |          
                                           |___/           
YOUR MUSIC PLAYER USERBOT IS SUCCESSFULLY DEPLOYED & RUNNING
"
python3 main.py
