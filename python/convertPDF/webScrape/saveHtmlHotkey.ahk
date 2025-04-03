^j::
i:=51
Loop, 8 {
    Send, ^s
    Sleep, 3000
    Send, equibase%i%
    Send, {Enter}
    Sleep, 3000
    Send, ^w
    Sleep, 3000
    i++
}
Return

Escape::
ExitApp
Return