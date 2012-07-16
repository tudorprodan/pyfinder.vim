if exists("g:loaded_pyfinder")
    finish
endif
let g:loaded_pyfinder = 1

if !has("python")
    " Python bindings must be enabled in
    " order to use this script.
    " We fail graciously.
    finish
endif

let s:current_script_dir = expand("<sfile>:p:h")

exec "pyfile ".s:current_script_dir."/"."pyfinder.py"
python << EOF
PySourceFinder.plugin_loaded()
EOF

function s:FindModule()
    let found_file = ""
python << EOF
import vim

# prefix variables with "pyfinder_" in order not to pollute the py namespace
pyfinder_current_line = vim.current.line
pyfinder_current_file = vim.eval("expand(\"%:p\")") or None

pyfinder_file_name = PySourceFinder.search(pyfinder_current_line, pyfinder_current_file)

vim.command("let found_file = \"{}\"".format(pyfinder_file_name))
EOF
    return found_file
endfunction

function s:EditFoundModule()
    let file = s:FindModule()

    if filereadable(file)
        exec "e " . file
    endif
endfunction

command -nargs=0 PySourceFind call s:EditFoundModule()

nnoremap <leader>gs :PySourceFind<CR>
