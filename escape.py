import escaperoom.engine
run_game = True
print("Welcome to the escape room game")
print(r"""
         ,     .
        /(     )\               A
   .--.( `.___.' ).--.         /_\
   `._ `%_&%#%$_ ' _.'     /| <___> |\
      `|(@\*%%/@)|'       / (  |L|  ) \
       |  |%%#|  |       J d8bo|=|od8b L
        \ \$#%/ /        | 8888|=|8888 |
        |\|%%#|/|        J Y8P"|=|"Y8P F
        | (.".)%|         \ (  |L|  ) /
    ___.'  `-'  `.___      \|  |L|  |/
  .'#*#`-       -'$#*`.       / )|
 /#%^#%*_ *%^%_  #  %$%\    .J (__)
 #&  . %%%#% ###%*.   *%\.-'&# (__)
 %*  J %.%#_|_#$.\J* \ %'#%*^  (__)
 *#% J %$%%#|#$#$ J\%   *   .--|(_)
 |%  J\ `%%#|#%%' / `.   _.'   |L|
 |#$%||` %%%$### '|   `-'      |L|
 (#%%||` #$#$%%% '|            |L|
 | ##||  $%%.%$%  |            |L|
 |$%^||   $%#$%   |  VK/cf     |L|
 |&^ ||  #%#$%#%  |            |L|
 |#$*|| #$%$$#%%$ |\           |L|
 ||||||  %%(@)$#  |\\          |L|
 `|||||  #$$|%#%  | L|         |L|
      |  #$%|$%%  | ||l        |L|
      |  ##$H$%%  | |\\        |L|
      |  #%%H%##  | |\\|       |L|
      |  ##% $%#  | Y|||       |L|
      J $$#* *%#% L  |E/
      (__ $F J$ __)  F/
      J#%$ | |%%#%L
      |$$%#& & %%#|
      J##$ J % %%$F
       %$# * * %#&
       %#$ | |%#$%
       *#$%| | #$*
      /$#' ) ( `%%\
     /#$# /   \ %$%\
    ooooO'     `Ooooo
    
    *Source: https://www.asciiart.eu/mythology/monsters
    """)

print("Escape before the the cybersecurity minotaur captures you")
print("Type 'quit' to quit")
print("Type help for assistance")
engine = escaperoom.engine.Engine()

while run_game:
    next_step = input("What would you like to do?")
    run_game = engine.command(next_step)