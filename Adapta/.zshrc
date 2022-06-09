#aliases
alias ll="ls -A"
alias logg="git log --decorate --all --graph --oneline"
alias gs="git status"
alias gf="git fetch"
alias gc="git checkout"

# case insensitive autocomplete
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

# use starship prompt
eval "$(starship init zsh)"
