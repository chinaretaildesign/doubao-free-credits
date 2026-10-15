# Refresh PATH in current PowerShell session and verify Git
$machine = [System.Environment]::GetEnvironmentVariable("PATH", "Machine")
$user = [System.Environment]::GetEnvironmentVariable("PATH", "User")
$env:PATH = $machine + ";" + $user

Write-Host ""
Write-Host "=== Git version ==="
git --version
Write-Host ""
Write-Host "=== Global config ==="
git config --global user.name
git config --global user.email
git config --global http.sslBackend
Write-Host ""
Write-Host "=== Push status ==="
Set-Location "D:\WorkBuddy\tmp\doubao-skill-publish"
git status -sb
git push
Write-Host ""
Write-Host "Done. Git Bash is also available from Start Menu." -ForegroundColor Green