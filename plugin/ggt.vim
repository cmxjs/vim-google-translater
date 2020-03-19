let s:translator_file = expand('<sfile>:p:h') . "/../google.py"
if exists('v:true')
    let s:translator = {'stdout_buffered': v:true, 'stderr_buffered': v:true}
else
    let s:translator = {'stdout_buffered': 1, 'stderr_buffered': 1}
endif

function! s:translator.on_stdout(jobid, data, event)
    if !empty(a:data[0]) | echomsg join(a:data) | endif
endfunction
let s:translator.on_stderr = function(s:translator.on_stdout)

function! s:translator.start(lines)
    let python_cmd = ggt#GetAvailablePythonCmd()
    if empty(python_cmd)
        echoerr "[GoogleTranslator] [Error]: Python package neeeds to be installed!"
        return -1
    endif

    let cmd = printf("%s %s %s", python_cmd, s:translator_file, a:lines)
    if exists('*jobstart')
        return jobstart(cmd, self)
    elseif exists('*job_start') && ! has("gui_macvim")
        return job_start(cmd, {'out_cb': "ggt#VimOutCallback"})
    else
        echo system(cmd)
    endif
endfunction

function! s:GoogleVisualTranslate()
    call s:translator.start(ggt#GetVisualSelection())
endfunction

function! s:GoogleCursorTranslate()
    call s:translator.start(expand("<cword>"))
endfunction

function! s:GoogleEnterTranslate()
    let word = input("Please enter the word: ")
    redraw!
    call s:translator.start(word)
endfunction

command! Ggv call <SID>GoogleVisualTranslate()
command! Ggc call <SID>GoogleCursorTranslate()
command! Gge call <SID>GoogleEnterTranslate()
