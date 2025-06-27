; version using macro insetead of triggers
M98 P"0:/macros/printStart.g"
G21
G90
G1 Z50
G1 X50 Y50
M98 P"0:/macros/tempReadout.g"
M98 P"0:/macros/square.g"
M98 P"0:/macros/nextLayer.g"
G1 Z100
G1 X50 Y50
M98 P"0:/macros/tempReadout.g"
M98 P"0:/macros/square.g"
M98 P"0:/macros/nextLayer.g"
G4 S1
M98 P"0:/macros/printComplete.g"
G28
M2
