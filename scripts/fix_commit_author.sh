#!/bin/bash
# Copyright (c) 2018-2021 Terry Greeniaus.
# All rights reserved.

# Helper script to iterate through all "edit" commits in
# an interactive rebase and update the commit author.
make clean
while true; do
    git -c user.name="Terry Greeniaus" -c user.email=terrygreeniaus@gmail.com commit --amend --reset-author --no-edit
    git rebase --continue || break
done
