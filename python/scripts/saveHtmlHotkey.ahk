^j::
i:=1
Loop, 30 {
    Send, ^s
    Sleep, 3000
    Send, equibase%i%
    Send, {Enter}
    Sleep, 3000
    Send, ^w
    Sleep, 4000
    i++
}
Return

Escape::
ExitApp
Return