A simple python libary to send messages via whatsapp Will be updated multiple times in the future Written in Python 3

Functions:

Replace number with the phone number in the format of countrycode+number (Do not use any symbols) Replace message with your message does not matter if spaces as it is replaced with %20 which whatsapp regards as a extension to the message so you can add messages with spaces no problem

pythonwhatsapp.webdmclose(number, message) Opens whatsapp using webbrowser to send a message using the public whatsapp web api (Which includes having the option of sending messages to specific numbers via changes in the url) then presses enter using pyautogui as the api only places the text but does not press send. Then it closes the tab with using the hotkey with pyautogui ctrl w.

pythonwhatsapp.webdmopen(number,message) Opens whatsapp using webbrowser to send a message using the public whatsapp web api (Which includes having the option of sending messages to specific numbers via changes in the url) then presses enter using pyautogui as the api only places the text but does not press send.

phonedm(number, message) Opens whatsapp using the api to send messages on phone. (Have not figured out how to auto send yet)

phonegroup() Not built yet as i am yet to figure out.

webgroupclose(invite, message) Opens whatsapp using webbrowser to send a message using the public whatsapp web api (It includes the option to open a group but not place any placeholder text). Due to the limiations of the api, I had to use pyautogui function of typing the message then pressing enter. Then it cloeses the group with pyautogui hotkey ctrl,w.

webgroupopen(invite, message) Opens whatsapp using webbrowser to send a message using the public whatsapp web api (It includes the option to open a group but not place any placeholder text). Due to the limiations of the api, I had to use pyautogui function of typing the message then pressing enter.

Will add more features if they are suggested.