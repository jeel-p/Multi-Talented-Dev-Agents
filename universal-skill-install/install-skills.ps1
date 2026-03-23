#Requires -Version 5.1
<#
.SYNOPSIS
  Wrapper for install_skills.py (universal SKILL.md installer).

.EXAMPLE
  .\install-skills.ps1

.EXAMPLE
  .\install-skills.ps1 -Source .\my-skills -Tools all -Scope global

.EXAMPLE
  .\install-skills.ps1 -ListTools
#>
param(
  [string] $Source,
  [string] $Tools = "all",
  [ValidateSet("global", "project")]
  [string] $Scope = "global",
  [string] $ProjectRoot = (Get-Location).Path,
  [switch] $DryRun,
  [switch] $Force,
  [switch] $Link,
  [switch] $ListTools
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = Join-Path $here "install_skills.py"

if (-not (Test-Path $py)) {
  Write-Error "Missing $py"
}

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
  $python = Get-Command python3 -ErrorAction SilentlyContinue
}
if (-not $python) {
  Write-Error "Python 3 is required. Install from https://www.python.org/downloads/ and ensure python is on PATH."
}

$args = @($py)
if ($ListTools) {
  $args += "--list-tools"
} else {
  if ($Source) {
    $args += @("--source", $Source)
  }
  $args += @("--tools", $Tools, "--scope", $Scope, "--project-root", $ProjectRoot)
  if ($DryRun) { $args += "--dry-run" }
  if ($Force) { $args += "--force" }
  if ($Link) { $args += "--link" }
}

& $python.Source $args
exit $LASTEXITCODE
