-- TODO check what lines are actually needed
vim.cmd('autocmd!')

vim.scriptencoding = 'utf-8'
vim.opt.encoding = 'utf-8'
vim.opt.fileencoding = 'utf-8'

vim.wo.number = true

-- to see the full list of settings, :help option-list
vim.opt.title = false
vim.opt.autoindent = true
vim.opt.hlsearch = true
vim.opt.backup = false
vim.opt.showcmd = true
vim.opt.cmdheight = 1
vim.opt.laststatus = 2
vim.opt.expandtab = true -- use spaces when <Tab> is inserted
vim.opt.scrolloff = 10
vim.opt.shell = 'fish'
vim.opt.ignorecase = true
vim.opt.smarttab = true
vim.opt.breakindent = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
vim.opt.ai = true -- Auto indent
vim.opt.si = true -- Smart indent
vim.opt.wrap = true -- No wrap lines
vim.opt.backspace = 'start,eol,indent'


-- colorsheme stuff - move to another place
vim.g.catppuccin_flavour = "mocha"
require('catppuccin').setup()
vim.cmd [[colorscheme catppuccin]]
