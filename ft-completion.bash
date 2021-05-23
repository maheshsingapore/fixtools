#!/usr/bin/env bash


_ft() {

if [ "${#COMP_WORDS[@]}" != "2" ]; then
    return
fi

declare -r OPERS="tabulate compare extract simulate serve"
local operation=${COMP_WORDS[1]}
COMPREPLY=($( compgen -W "$OPERS" "$operation"))

}

complete -F _ft ft
