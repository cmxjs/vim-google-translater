# vim google translater

vim google translater 可以帮你在 vim 中翻译单词或语句

## Install
### Plug安装:
``` vim
Plug 'cmxjs/vim-translater'
source %
PlugInstall
```
### 普通安装:
把所有文件拷贝到 `~/.vim/` 目录下，就可以用了。

### 添加 `~/.vimrc` 文件：
```vim
vnoremap <silent> <C-e> :<C-u>Ggv<CR>
nnoremap <silent> <C-e> :<C-u>Ggc<CR>
noremap <leader>fj :<C-u>Gge<CR>
```

### 如何使用

在普通模式下，按 `ctrl+e`， 会翻译当前光标下的单词；

在 `visual` 模式下选中单词或语句，按 `ctrl+e`，会翻译选择的单词或语句；

点引导键再点f，j，可以在命令行输入要翻译的单词或语句；

译文将会在编辑器底部的命令栏显示。

### Reference project
[vim-youdao-translater](https://github.com/ianva/vim-youdao-translater)
