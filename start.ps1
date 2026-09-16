[CmdletBinding()]
param(
    [ValidateNotNullOrEmpty()]
    [string]$Database = 'pet_clinic_dev',

    [switch]$Version
)

$ErrorActionPreference = 'Stop'

$pythonPath = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$odooPath = Join-Path $PSScriptRoot 'odoo-19.0\odoo-bin'
$configPath = Join-Path $PSScriptRoot '.local\odoo.conf'

foreach ($requiredPath in @($pythonPath, $odooPath, $configPath)) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) {
        throw "Required file is missing: $requiredPath. Complete the local Odoo setup before starting PetSystem."
    }
}

$odooArguments = @($odooPath, '-c', $configPath, '-d', $Database)
if ($Version) {
    $odooArguments += '--version'
}
else {
    $httpPort = '8069'
    foreach ($line in Get-Content -LiteralPath $configPath) {
        if ($line -match '^\s*http_port\s*=\s*(\d+)\s*$') {
            $httpPort = $Matches[1]
            break
        }
    }

    Start-Process "http://localhost:$httpPort"
}

Push-Location -LiteralPath $PSScriptRoot
try {
    & $pythonPath @odooArguments
    $odooExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}

exit $odooExitCode
