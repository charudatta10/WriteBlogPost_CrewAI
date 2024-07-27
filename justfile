#    <one line to give the program's name and a brief idea of what it does.>  
#    Copyright © 2024 Charudatta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#    email contact: 152109007c@gmailcom

set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]

default:
    just --list --unsorted

init:
    #!pwsh
    git init
    New-Item -ItemType "file" -Path ".gitattribute", "main.py", "requirement.yaml"
    New-Item -ItemType "directory" -Path "archives", "docs", "src", "test"
    New-Item -ItemType "file" -Path .\* -Name "__init__.py" -ErrorAction SilentlyContinue
    gig gen python > .gitignore 
    u

config:
    dynaconf init -f json 

doc:
    #!pwsh
    conda activate blog
    p -m mkdocs new .
    
readme:
    python C:/Users/chaitrali/Documents/GitHub/readme-generator

commit message="init":
    #!pwsh
    git add .
    git commit -m {{message}}

exe file_name:
    #!pwsh
    pyintsaller src/{{file_name}} -onefile

#alias b := build
#build: 
#   echo "hi"; echo "bye"

#########-ADD-Custom-Tasks-Here-##################





        

