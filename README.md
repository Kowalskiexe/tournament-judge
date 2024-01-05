# Judge bot for a bot tournament

This is a bot which runs participants' bots against each other and scores them.

# The bot tournament

In this tournament participants make bots that play [iterated prisoner's dillema](https://en.wikipedia.org/wiki/Prisoner's_dilemma#The_iterated_prisoner's_dilemma) with fixed n = 10.

## Iterated prisoner's dillma rules

If one of the bots stays silent and the other testifies, testifing bot gets +0 years to its sentence and the silent bot gets +3 years to its sentence.
If both bots stay silent, they both get +1 years to their sentences each.
If both bots testify, they both get +2 years to their sentences each.

![matrix](https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Prisoners_dilemma.svg/800px-Prisoners_dilemma.svg.png)

The bots play in pairs. Every bot will play with every other bot exactly once.

The bot that gets the lowest cumulative sentence out of all the bots wins the tournament.

# Technicals

Participants provide [docker images](https://www.youtube.com/watch?v=Gjnup-PuquQ) of their bots so internally they can use any technology they want, as long as this technology supports HTTP, even Delphi.

On first round the judge bot sends HTTP POST request on port 5000 to both bots with json body:
```json
{
    "opponents_last_move": "none"
}
```
It can be simulated with commnads

On linux / macOS via
```bash
curl -X POST -H "Content-type: text/json" -d '{"opponents_last_move": "none"}' localhost:5000
```
On windows in PowerShell
```powershell
Invoke-WebRequest -Uri 'http://localhost:5000' -Method Post -Headers @{'Content-type'='text/json'} -Body '{"opponents_last_move": "none"}'
```

The participants' bots must then give HTTP response with JSON body in format:
```json
{
    "my_move": "stay silent"
}
```
or
```json
{
    "my_move": "testify"
}
```
indicating if they stay silent or testify.

The following 9 rounds are conducted similarly but judge's HTTP request is either
```json
{
    "opponents_last_move": "stay silent"
}
```
if the oppenent stayed silent in the last round.

Or
```json
{
    "opponents_last_move": "testify"
}
```
if the oppoenent testified in the last round.

After a total of 10 rounds are completed the sentences for both bots are revealed on standard output and the winning bot for this match is the one with the lower sentence.

# Example / bot template
[here](https://github.com/Kowalskiexe/tournament-bot-template)

# Running judge bot

## Requirements
* git installed on your system
* python installed on your system
* docker installed on your system

First clone this repo
```bash
git clone https://github.com/kowalskiexe/tournament-judge.git
```
Create [virtual enviroment](https://python.land/virtual-environments/virtualenv) for Python
```bash
python -m venv .tournament-judge
```
Source the virtual enviroment

On linux / macOS
```bash
source .tournament-judge/bin/activate
```
On Windows
```powershell
# in cmd.exe
.tournament-judge/Scripts/activate.bat
# in PowerSHell
.tournament-judge/Scripts/activate.ps1
```

Install depencencies
```bash
cd tournament-judge
pip install -r jduge/requirements.txt
```
Pull participants' bots
```bash
# for example
docker pull kowalskiexe/tournament-bot-template
```
Run judge bot to conduct a match between a pair of bots
```bash
# kowalskiexe/trounament-bot-template vs kowalskiexe/tournament-bot-template
# the first argument is bot A, the seocnd argument is bot B
python -m judge kowalskiexe/tournament-bot-template kowalskiexe/tournament-bot-template
```
