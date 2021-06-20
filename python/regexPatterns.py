### DRIVER
newRaceTest = r'Copyright 202[0-9] Equibase Company LLC. All Rights Reserved.'

cancelledRace = r'Cancelled - '
quarterHorseRace = r'(- Quarter Horse|Arabian|Mixed)'
generalInfoCutoff = r'Last Raced Pgm'
horseInfoCutoff = r'Fractional Times:|Final Time:'
timesInfoCutoff = r'Run-Up: '
betInfoCutoff = r'Past Performance Running Line Preview'
endInfoCutoff = r'Trainers: '


### GENINFOFNS
distanceSurfaceLinePattern = r'Track Record:'
weatherConditionsLinePattern = r'Weather: [A-Za-z]+ Track:'
startNotesLinePattern = r'Off at: [0-9:]+ Start:'
segmentsLinePattern = r'Last Raced Pgm'

genInfoLine1TrackPattern = r' *([^-]+) - ([^-]+) - (.*)'
genInfoLine1LethbridgePattern = r' *([^-]+-[^-]+) - ([^-]+) - ([^-]+)'
genInfoLine1DatePattern = r'([A-Za-z]*) (\d?\d), (\d\d\d\d)'
genInfoLine1RaceNumPattern = r'\d?\d'

genInfoLine2BreedPattern = r'- (.*)$'

distanceSurfaceFullSearchPattern = r'([- A-Za-z]+)(?=(Current )?Track)'
distanceSurfaceSpecSearchPattern = r' (.*) (?=On The)On The ([A-Z][-a-z ]*) '

weatherConditionsSearchPattern = r'Weather: ([A-Z][a-z]*) Track: ([A-Z][a-z]*)'

startNotesSearchPattern = r'Off at: (\d?\d:\d\d) Start: ([A-Z0-9][a-z0-9 ]*)'

segmentsSearchPattern = r'PP ([A-Za-z0-9/]+) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?Fin'


### HORSEINFOFNS
horseInfoBottomLineCheckPattern = r'^ (\d?\d[A-Z][a-z]{2}\d\d|---)'

horseInfoTopLineSearchPattern = r'^ ([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*) ?([0-9/A-Za-z]*)'

horseInfoBottomLineSearchPattern = r'^ (\d?\d[A-Z][a-z]{2}\d\d [A-Z]{2,3}|---) (\d?\d[ABCX]?) ([^0-9]+) (\d?\d?\d)[»½¶]* ([ABCLM]+|[ABCLM]+ [23abcfghijklnopqrsvWwxyz]+|- -|[23abcfghijklnopqrsvWwxyz]+) ([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ?([-0-9]*) ([0-9]+\.\d\d)?\*? ?(.*)$'
horseInfoDateSearchPattern = r'(\d?\d)([A-Z][a-z]{2})(\d\d) ([A-Z]{2,3})'
horseJockeySearchPattern = r"(.*) ?\(([-A-Za-z,. ']+)\)"


### TIMESINFOFNS
fractionalTimesLinePattern = r'Fractional Times:|Final Time:'
runupLinePattern = r'Run-Up:'

fractionalTimesSearchPattern = r'(Fractional Times: ([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*) ?([0-9.:]*))? Final Time: ([0-9.:]*)'
runupSearchPattern = r'Run-Up: ([0-9.]*)'


#### BETINFOFNS
WPSLinePattern = r'Total WPS Pool'
betsLinePattern = r'Pgm Horse Win'
advancedBetsLinePattern = r'(Exacta|Trifecta|Superfecta|Daily Double)'
buyinPattern = r'(\$\d\.\d\d)'

WPSSearchPattern = r'Total WPS Pool: \$([0-9,]*)'

betLabelPattern = r'Pgm Horse Win (Place)? ?(Show)?'
firstPlaceWSearchPattern = r'\d?\d[ABC]? .+ (\d?\d?\d\.\d\d)()()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'
firstPlaceWPSearchPattern = r'\d?\d[ABC]? .+ (\d?\d?\d\.\d\d) (\d?\d\.\d\d)()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'
firstPlaceWPSSearchPattern = r'\d?\d[ABC]? .+ (\d?\d?\d\.\d\d) (\d?\d\.\d\d) (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'

secondPlaceWSearchPattern = r'\d?\d[ABC]? .+()()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'
secondPlaceWPSearchPattern = r'\d?\d[ABC]? .+ (\d?\d\.\d\d)()( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'
secondPlaceWPSSearchPattern = r'\d?\d[ABC]? .+ (\d?\d\.\d\d) (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\) )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'

thirdPlaceWPSearchPattern = r'\d?\d[ABC]? .+()( (?=\$\d\.\d\d)([0-9.$ A-Za-z,]* [0-9-/]* (\([0-9A-Za-z ]+\)? )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'
thirdPlaceWPSSearchPattern = r'\d?\d[ABC]? .+ (\d?\d\.\d\d)( ([0-9.$ A-Za-z,]* [AL0-9-/]* (\([0-9A-Za-z ]+\)? )?[0-9,.]+ [0-9,.]*)( [0-9,.]*)?)?$'

additionalBetLineSearchPattern = r'([0-9.$ A-Za-z,]*) ([0-9-/ABC]*) (\([0-9A-Za-z ]+\) )?([0-9,.]+\.\d\d) ([0-9,.]*)( [0-9,.]*)?$'


### RUNLINEINFOFNS
pointOfCallLinePattern = r'^ Pgm Horse Name (Start|[0-9/]+)'
firstCallStartRLSearchPattern = r'^ (\d?\d[ABC]?) [^0-9]+ \d?\d[ABC]?( ---)+$'
firstCallNonStartRLSearchPattern = r'^ (\d?\d[ABC]?) [^0-9]+ \d?\d[ABC]?( ---)+$'

rlTopLineSearchPattern = r'([-0-9/A-Za-z]+) ?([-0-9/A-Za-z]*) ?([-0-9/A-Za-z]*) ?([-0-9/A-Za-z]*) ?([-0-9/A-Za-z]*) ?([-0-9/A-Za-z]*)$'

rlBottomLineSearchPattern = r'^ (\d?\d[ABCX]?) [^0-9]+ ([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*) ?([0-9-]*)$'


### ENDITEMSFNS
trainerLinePattern = r'^ Trainers:'
ownerLinePattern = r'^ Owners:'
footnoteLinePattern = r'^ Footnotes$'

trainerFullSearchPattern = r'( \d?\d - [^;]+;)+'
trainerShortSearchPattern = r'(\d?\d) - (.+)$'

ownerFullSearchPattern = r'( \d?\d - ?[^;]+;)+'
ownerShortSearchPattern = r'^ (\d?\d) - ?(.+)$'