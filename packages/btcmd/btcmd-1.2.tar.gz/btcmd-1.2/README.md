# Bookmarked Terminal Commands - btcmd
## About
If you need to type extensive commands on a daily basis, whether to connect to a server or to clean up unused container images, this tool is for you. You can mark your favorite commands and call them from a simple shortcut, all in the comfort of an installation via pip.

## Requirements 
- Python

## Installation
- Open your terminal and type `pip install btcmd`
- After installing run: `btcmd -h` for more details. It's very easy to use.

## How to use
#### To list all saved commands, type in terminal:
- `btcmd -l` 
#### To save a command with an nickname, type in terminal:
- `btcmd -s 'COMMAND_YOU_WANT_TO_SAVE' -n COMMAND_NICKNAME`
#### To rename a command's nickname, type in terminal:
- `btcmd -n 'COMMAND_YOU_WANT_TO_RENAME'`
#### To delete a saved command, type in terminal:
- `btcmd -d COMMAND_NICKNAME` 
#### To run the command by the nickname, type in terminal:
- `btcmd -r COMMAND_NICKNAME` or simply `btcmd COMMAND_NICKNAME`
#### To see help details, type in terminal:
- `btcmd -h`