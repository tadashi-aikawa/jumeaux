#!/usr/bin/env bats

JUMEAUX="pipenv run python jumeaux/executor.py"

setup() {
  rm -rf requests config.yml responses report.json
}

@test "Usage" {
  $JUMEAUX -h
}


#--------------------------
# jumeaux init
#--------------------------

@test "Init with no args" {
  run $JUMEAUX init
  [ "$status" -eq 1 ]
  [[ ! -a config.yml ]]
  [[ ! -a requests ]]
}

@test "Init with invalid args" {
  run $JUMEAUX init hogehoge
  [ "$status" -eq 1 ]
  [[ ! -a config.yml ]]
  [[ ! -a requests ]]
}

@test "Init rest" {
  $JUMEAUX init rest
  [[ -a config.yml ]]
  [[ -a requests ]]
}

@test "Init minimum" {
  $JUMEAUX init minimum
  [[ -a config.yml ]]
  [[ -a requests ]]
}

@test "Init json" {
  $JUMEAUX init json
  [[ -a config.yml ]]
  [[ -a requests ]]
}

@test "Init ignore_properties" {
  $JUMEAUX init ignore_properties
  [[ -a config.yml ]]
  [[ -a requests ]]
}


#--------------------------
# jumeaux run
#--------------------------

@test "Run" {
  $JUMEAUX init rest
  $JUMEAUX run requests
  [[ -a responses ]]
}

@test "Run with log level options" {
  $JUMEAUX init rest
  $JUMEAUX run requests -v
  $JUMEAUX run requests -vv
  $JUMEAUX run requests -vvv
  [[ -a responses ]]
}


#--------------------------
# jumeaux retry
#--------------------------

@test "Retry" {
  $JUMEAUX init rest
  $JUMEAUX run requests > report.json
  [[ -a responses ]]
  [[ -a report.json ]]
  rm -rf requests config.yml responses

  $JUMEAUX retry report.json
  [[ -a responses ]]
  [[ -a report.json ]]
}

