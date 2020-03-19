function! ggt#VimOutCallback(chan, msg)
    echo a:msg
endfunction

" This function taken from the lh-vim repository
function! ggt#GetVisualSelection()
    try
        let a_save = @a
        normal! gv"ay
        return @a
    finally
        let @a = a_save
    endtry
endfunction

"Only support python3,please install python3,
function! ggt#GetAvailablePythonCmd()
    for cmd in ['python3'] 
        if executable(cmd)
            return cmd
        endif
    endfor
    return ""
endfunction
