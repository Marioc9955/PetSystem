<#
.SYNOPSIS
Creates repository issues from a JSON array of { title, body } and adds them to a GitHub Project.
.EXAMPLE
.\importTickets.ps1 -WhatIf
.EXAMPLE
.\importTickets.ps1
.NOTES
Requires GitHub CLI authenticated with repository access and project write access:
  gh auth login
  gh auth refresh -s project
Each run creates new issues. After a partial failure, remove successful tickets
from the input before retrying to avoid duplicates.
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$JsonPath,
    [ValidatePattern('^[^/\s]+/[^/\s]+$')]
    [string]$Repository = 'Marioc9955/PetSystem',
    [ValidateNotNullOrEmpty()]
    [string]$ProjectOwner = 'Marioc9955',
    [ValidateRange(1, 2147483647)]
    [int]$ProjectNumber = 6
)

$ErrorActionPreference = 'Stop'
if (-not $JsonPath) {
    $JsonPath = Join-Path $PSScriptRoot 'tickets.json'
}
$json = Get-Content -LiteralPath $JsonPath -Raw -Encoding UTF8
if (-not $json.TrimStart().StartsWith('[')) {
    throw 'Expected a JSON array of objects with title and body fields.'
}
# Direct assignment avoids a nested array from ConvertFrom-Json in Windows PowerShell 5.1.
$tickets = ConvertFrom-Json -InputObject $json
foreach ($ticket in $tickets) {
    if ($null -eq $ticket -or $ticket.title -isnot [string] -or
        [string]::IsNullOrWhiteSpace($ticket.title) -or $ticket.body -isnot [string]) {
        throw 'Every ticket must have a non-empty string title and a string body.'
    }
}

if (-not $WhatIfPreference -and $tickets.Count -gt 0) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        throw 'Install GitHub CLI (gh) and authenticate before importing.'
    }
    & gh project view $ProjectNumber --owner $ProjectOwner --format json | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw 'Cannot access the project. Check the owner, project number, and gh authentication.'
    }
}

foreach ($ticket in $tickets) {
    if (-not $PSCmdlet.ShouldProcess(
        "$Repository -> $ProjectOwner project $ProjectNumber",
        "Create issue '$($ticket.title)' and add it to the project"
    )) { continue }

    $bodyFile = [System.IO.Path]::GetTempFileName()
    try {
        [System.IO.File]::WriteAllText($bodyFile, $ticket.body, [System.Text.UTF8Encoding]::new($false))
        $issueUrl = & gh issue create --repo $Repository --title $ticket.title --body-file $bodyFile
        if ($LASTEXITCODE -ne 0) {
            throw "Issue creation failed for '$($ticket.title)'. Check GitHub before retrying."
        }
        $issueUrl = ($issueUrl -join "`n").Trim()
        Write-Host "Created: $issueUrl"
        & gh project item-add $ProjectNumber --owner $ProjectOwner --url $issueUrl | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw "Issue exists at $issueUrl but project linking failed. Add that URL using gh project item-add; do not recreate the issue."
        }
        Write-Host "Added to project $ProjectNumber."
    }
    finally {
        Remove-Item -LiteralPath $bodyFile -Force
    }
}
