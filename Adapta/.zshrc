#aliases
alias ll="ls -A"
alias logg="git log --decorate --all --graph --oneline"
alias gs="git status"

# case insensitive autocomplete
autoload -Uz compinit && compinit
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Za-z}'

# use starship prompt
eval "$(starship init zsh)"
