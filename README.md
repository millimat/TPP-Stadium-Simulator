# TPP-Stadium-Simulator

I coded this two years ago on behalf of the Twitch Plays Pokemon community, for a minigame in which users could bet virtual points on randomized 3v3 matchups between teams of rental Pokemon in Pokemon Stadium 2. 

When two Pokemon were on the field, stream users could vote to select moves for the team they bet on, and the emulator running the game would randomly select a move for each team with probabilities determined by the total amount of money backing that move. It was a bit like gambling, but less random, more fun, and with higher tempers.

The simulator is super old, and I can't guarantee it still works properly, given some changes to Python syntax that have come through since 2014. There's also some crappy style going on--e.g. the simulator restarts by calling itself recursively--but I promise my Stanford education has improved my coding style. A little bit. But I had fun making it!

Below are my original release notes from when I published it on the TPP subreddit.

---

>The simulator takes the names of the Pokemon from each team and predicts the outcome of each individual matchup by determining how many turns each Pokemon will take to faint the opponent using its most powerful damaging move. Then it displays how many predicted wins each team has, giving you a rough idea of which team is more powerful and how likely it is to win the battle.
>Once this analysis is complete, the simulator allows the user to review the predicted results of any matchup by typing in the names of the two Pokemon that are fighting. If you ever saw me in the chat rationalizing move choices by spouting off damage percentages, this function is what I was using to get those numbers.
>Some things to keep in mind while using the simulator:
>-If the simulator isn't interpreting a Pokemon's name correctly, check the file pokeList.txt to make sure its spellings are consistent with yours.
>-Some matches are "flagged" if the simulator detects certain moves in either of the Pokemon's movesets. These are mostly moves whose outcomes in matches are difficult to predict over time: Explosion, Selfdestruct, Flail, Reversal, Rollout, Fury Cutter, and Super Fang. If a match is flagged, you should probably replay it before interpreting it as a victory for the marked team.
>-In determining how many turns a Pokemon will take to KO its opponent, the simulator will take into consideration how many turns each move takes to execute. However, a move is only treated as a multi-turn move if the charging turn leaves it vulnerable to enemy attack. This means Fly and Dig are counted as single-turn moves. However, if the opponent has Thunder, Earthquake, or powerful stat-boosting moves, using Fly or Dig is probably a bad idea.
>-The simulator does not account for non-damaging moves, such as stat-boosting moves, weather moves, status-inflicting moves, etc. These moves may or may not be important to your team's strategy in the actual match, so you should keep them in mind if you see them before betting.
>-There is no functionality for Future Sight, Present, or Beat Up, because these moves are somewhat more difficult to incorporate into damage calculations than other moves.
>-If a Pokemon has no damaging moves, it is assumed to lose by default. This works fine for Pokemon like Metapod, but not so well for Ditto and Wobbuffet. While Wobbuffet can be deadly if Counter, Mirror Coat, and Destiny Bond are used correctly, Ditto is generally at a significant disadvantage because of the turn needed to Transform.
