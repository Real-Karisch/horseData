^j::
i:=1
Loop, 20 {
    Send, ^s
    Sleep, 2000
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