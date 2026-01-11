# change mutex name
$mutexName = "Local\faceRecognitionProject" 

try {   
    $mutex = [System.Threading.Mutex]::OpenExisting($mutexName)    
    Write-Host "Success: The Mutex '$mutexName' IS running and locked." -ForegroundColor Green  
    $mutex.Dispose()
}
catch {
    Write-Host "Not Found: The Mutex '$mutexName' is NOT active." -ForegroundColor Red
}