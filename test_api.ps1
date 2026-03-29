Start-Sleep -Seconds 6
Write-Output '--- Test: Signup ---'
try {
  $body = @{username='testadmin'; email='testadmin@example.com'; password='pass1234'} | ConvertTo-Json
  $res = Invoke-RestMethod -Uri http://127.0.0.1:5000/api/register -Method Post -ContentType 'application/json' -Body $body
  Write-Output ("Signup response: " + ($res | ConvertTo-Json -Compress))
} catch {
  Write-Output ("Signup failed: " + $_.Exception.Message)
}
Write-Output '--- Test: Login ---'
try {
  $body = @{email='testadmin@example.com'; password='pass1234'} | ConvertTo-Json
  $login = Invoke-RestMethod -Uri http://127.0.0.1:5000/api/login -Method Post -ContentType 'application/json' -Body $body
  Write-Output ("Login response: " + ($login | ConvertTo-Json -Compress))
  $token = $login.token
} catch {
  Write-Output ("Login failed: " + $_.Exception.Message)
  exit 1
}
Write-Output '--- Test: Register domain (first) ---'
$headers = @{ Authorization = "Bearer $token" }
try {
  $body = @{interval=6} | ConvertTo-Json
  $reg = Invoke-RestMethod -Uri http://127.0.0.1:5000/api/register/example.com -Method Post -Headers $headers -ContentType 'application/json' -Body $body
  Write-Output ("Register response: " + ($reg | ConvertTo-Json -Compress))
} catch {
  Write-Output ("Register failed (first): " + $_.Exception.Message)
}
Write-Output '--- Test: Register domain (second) ---'
try {
  $body = @{interval=6} | ConvertTo-Json
  $reg2 = Invoke-RestMethod -Uri http://127.0.0.1:5000/api/register/example.com -Method Post -Headers $headers -ContentType 'application/json' -Body $body
  Write-Output ("Second register response (unexpected): " + ($reg2 | ConvertTo-Json -Compress))
} catch {
  Write-Output ("Second register failed as expected. Error: " + $_.Exception.Message)
}
