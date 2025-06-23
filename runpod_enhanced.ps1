# Enhanced RunPod WhisperX Caller Script
# Supports all new configurable parameters

param(
    [Parameter(Mandatory=$false)]
    [string]$PayloadFile = "payloads/basic_transcription.json",
    
    [Parameter(Mandatory=$false)]
    [switch]$Sync = $false,
    
    [Parameter(Mandatory=$false)]
    [string]$ApiKey = $env:RUNPOD_API_KEY,
    
    [Parameter(Mandatory=$false)]
    [string]$EndpointId = $env:ENDPOINT_ID
)

# Configuration
if (-not $ApiKey) {
    $ApiKey = $env:RUNPOD_API_KEY
    if (-not $ApiKey) {
        Write-Host "❌ RUNPOD_API_KEY not found. Set it in environment or pass -ApiKey parameter" -ForegroundColor Red
        exit 1
    }
}

if (-not $EndpointId) {
    $EndpointId = $env:ENDPOINT_ID
    if (-not $EndpointId) {
        Write-Host "❌ ENDPOINT_ID not found. Set it in environment or pass -EndpointId parameter" -ForegroundColor Red
        exit 1
    }
}

Write-Host "🚀 Enhanced WhisperX RunPod Caller" -ForegroundColor Green
Write-Host "================================================"
Write-Host "📋 Payload File: $PayloadFile"
Write-Host "⚙️  Mode: $(if ($Sync) { 'Synchronous' } else { 'Asynchronous' })"
Write-Host "🔑 Endpoint: $EndpointId"
Write-Host ""

# Check if payload file exists
if (-not (Test-Path $PayloadFile)) {
    Write-Host "❌ Payload file not found: $PayloadFile" -ForegroundColor Red
    Write-Host ""
    Write-Host "Available payload examples:"
    Get-ChildItem -Path "payloads/*.json" | ForEach-Object {
        Write-Host "  • $($_.Name)" -ForegroundColor Yellow
    }
    exit 1
}

# Load and display payload
$payload = Get-Content -Raw $PayloadFile
Write-Host "📝 Request Payload:" -ForegroundColor Cyan
Write-Host $payload
Write-Host ""

# Set up headers
$headers = @{
    Authorization = "Bearer $ApiKey"
    "Content-Type" = "application/json"
}

if ($Sync) {
    # Synchronous request
    Write-Host "🔄 Making synchronous request..." -ForegroundColor Yellow
    $uri = "https://api.runpod.ai/v2/$EndpointId/runsync"
    
    try {
        $response = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $payload
        
        if ($response.error) {
            Write-Host "❌ Error: $($response.error)" -ForegroundColor Red
        } else {
            Write-Host "✅ Success!" -ForegroundColor Green
            Write-Host ""
            Write-Host "📊 Results:" -ForegroundColor Cyan
            
            # Display key information
            if ($response.output.segments) {
                Write-Host "  • Segments found: $($response.output.segments.Count)"
                Write-Host "  • Language detected: $($response.output.language)"
                
                if ($response.output.config_used) {
                    Write-Host "  • Model used: $($response.output.config_used.model)"
                    Write-Host "  • Batch size: $($response.output.config_used.batch_size)"
                    Write-Host "  • Diarization: $($response.output.config_used.diarize)"
                }
                
                Write-Host ""
                Write-Host "📝 First few segments:" -ForegroundColor Cyan
                $response.output.segments | Select-Object -First 3 | ForEach-Object {
                    $speaker = if ($_.speaker) { $_.speaker } else { "N/A" }
                    Write-Host "  [$([math]::Round($_.start, 2))s - $([math]::Round($_.end, 2))s] $speaker`: $($_.text.Trim())"
                }
            }
            
            # Save full response
            $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
            $outputFile = "response_$timestamp.json"
            $response | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding UTF8
            Write-Host ""
            Write-Host "💾 Full response saved to: $outputFile" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "❌ Request failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}
else {
    # Asynchronous request (your original method)
    Write-Host "🔄 Making asynchronous request..." -ForegroundColor Yellow
    $uri = "https://api.runpod.ai/v2/$EndpointId/run"
    
    try {
        $jobResponse = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -Body $payload
        $jobId = $jobResponse.id
        
        Write-Host "🟢 Queued job ID: $jobId" -ForegroundColor Green
        Write-Host ""
        
        # Poll for completion
        do {
            $job = Invoke-RestMethod -Uri "https://api.runpod.ai/v2/$EndpointId/status/$jobId" -Headers $headers
            $timestamp = Get-Date -Format "HH:mm:ss"
            Write-Host "$timestamp Status: $($job.status)" -ForegroundColor Yellow
            
            if ($job.status -ne "COMPLETED") {
                Start-Sleep 5
            }
        } until ($job.status -eq "COMPLETED")
        
        Write-Host ""
        Write-Host "✅ Job completed!" -ForegroundColor Green
        
        # Display results
        if ($job.output.error) {
            Write-Host "❌ Error: $($job.output.error)" -ForegroundColor Red
        } else {
            Write-Host "📊 Results:" -ForegroundColor Cyan
            
            if ($job.output.segments) {
                Write-Host "  • Segments found: $($job.output.segments.Count)"
                Write-Host "  • Language detected: $($job.output.language)"
                
                if ($job.output.config_used) {
                    Write-Host "  • Model used: $($job.output.config_used.model)"
                    Write-Host "  • Batch size: $($job.output.config_used.batch_size)"
                    Write-Host "  • Diarization: $($job.output.config_used.diarization)"
                }
                
                Write-Host ""
                Write-Host "📝 First few segments:" -ForegroundColor Cyan
                $job.output.segments | Select-Object -First 3 | ForEach-Object {
                    $speaker = if ($_.speaker) { $_.speaker } else { "N/A" }
                    Write-Host "  [$([math]::Round($_.start, 2))s - $([math]::Round($_.end, 2))s] $speaker`: $($_.text.Trim())"
                }
            }
            
            # Save full response
            $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
            $outputFile = "response_$timestamp.json"
            $job.output | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputFile -Encoding UTF8
            Write-Host ""
            Write-Host "💾 Full response saved to: $outputFile" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "❌ Request failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Done!" -ForegroundColor Green 