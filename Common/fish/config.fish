# ~/.config/fish/config.fish

starship init fish | source

#aliases
alias ls="eza"
alias ll="eza --all --long --group-directories-first --icons"
alias lt="eza --all --long --group-directories-first --icons --tree"
alias logg="git log --decorate --all --graph --oneline"
alias gs="git status"
alias gf="git fetch"
alias gc="git checkout"
