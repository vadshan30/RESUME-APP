# TERMINUS AI - OpenAI API Setup Script

Write-Host "🤖 TERMINUS AI - OpenAI API Configuration" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check for both config.json and Environment Variable
$envKey = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
$hasEnvKey = -not [string]::IsNullOrWhiteSpace($envKey)

if (-not (Test-Path "config.json")) {
    @{
        openai_api_key = ""
        openai_model   = "gpt-4o-mini"
        use_openai     = $false
    } | ConvertTo-Json | Set-Content "config.json"
}

# Read current config
$config = Get-Content "config.json" | ConvertFrom-Json

Write-Host "📋 Current Configuration:" -ForegroundColor Yellow
if ($hasEnvKey) {
    $maskedKey = $envKey.Substring(0, [Math]::Min(7, $envKey.Length)) + "..." 
    Write-Host "  API Key (Env Var): $maskedKey" -ForegroundColor Green
}
elseif ($config.openai_api_key) {
    # Warn about insecure storage
    $maskedKey = $config.openai_api_key.Substring(0, [Math]::Min(7, $config.openai_api_key.Length)) + "..." 
    Write-Host "  API Key (Config Check): $maskedKey (INSECURE: Stored in plain text)" -ForegroundColor Yellow
}
else {
    Write-Host "  API Key: Not set" -ForegroundColor Red
}

Write-Host "  OpenAI Enabled: $($config.use_openai)" -ForegroundColor White
Write-Host "  Model: $($config.openai_model)" -ForegroundColor White
Write-Host ""

# Ask user what to do
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "  1. Set OpenAI API Key (Securely via Env Var)" -ForegroundColor White
Write-Host "  2. Enable/Disable OpenAI" -ForegroundColor White
Write-Host "  3. Change Model" -ForegroundColor White
Write-Host "  4. View Instructions" -ForegroundColor White
Write-Host "  5. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📝 Enter your OpenAI API Key:" -ForegroundColor Cyan
        Write-Host "   (Get it from: https://platform.openai.com/api-keys)" -ForegroundColor Yellow
        $apiKey = Read-Host "API Key"
        
        if ($apiKey) {
            # Set User-level Environment Variable
            [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", $apiKey, "User")
            
            # Also set in current session so it works immediately
            $env:OPENAI_API_KEY = $apiKey

            # Clear from config.json if present
            $config.openai_api_key = ""
            $config | ConvertTo-Json | Set-Content "config.json"
            
            Write-Host "✅ API Key saved securely!" -ForegroundColor Green
            Write-Host "   (Stored in User Environment Variables)" -ForegroundColor Gray
            
            # Ask if they want to enable it
            $enable = Read-Host "Enable OpenAI now? (y/n)"
            if ($enable -eq "y") {
                $config.use_openai = $true
                $config | ConvertTo-Json | Set-Content "config.json"
                Write-Host "✅ OpenAI enabled!" -ForegroundColor Green
            }
        }
    }
    
    "2" {
        if ($config.use_openai) {
            $config.use_openai = $false
            Write-Host "✅ OpenAI disabled. Using regex parser." -ForegroundColor Yellow
        }
        else {
            # Check if key exists anywhere
            $currentEnvKey = [System.Environment]::GetEnvironmentVariable("OPENAI_API_KEY", "User")
            if (-not $config.openai_api_key -and -not $currentEnvKey) {
                Write-Host "❌ Please set API key first (option 1)" -ForegroundColor Red
            }
            else {
                $config.use_openai = $true
                Write-Host "✅ OpenAI enabled!" -ForegroundColor Green
            }
        }
        $config | ConvertTo-Json | Set-Content "config.json"
    }
    
    "3" {
        Write-Host ""
        Write-Host "Available models:" -ForegroundColor Cyan
        Write-Host "  1. gpt-4o-mini (Fast, Cheap)" -ForegroundColor White
        Write-Host "  2. gpt-4o (Best Quality)" -ForegroundColor White
        Write-Host "  3. gpt-3.5-turbo (Legacy)" -ForegroundColor White
        $modelChoice = Read-Host "Choose model (1-3)"
        
        switch ($modelChoice) {
            "1" { $config.openai_model = "gpt-4o-mini" }
            "2" { $config.openai_model = "gpt-4o" }
            "3" { $config.openai_model = "gpt-3.5-turbo" }
        }
        $config | ConvertTo-Json | Set-Content "config.json"
        Write-Host "✅ Model set to: $($config.openai_model)" -ForegroundColor Green
    }
    
    "4" {
        Write-Host ""
        Write-Host "📚 How to get OpenAI API Key:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "1. Go to: https://platform.openai.com/api-keys" -ForegroundColor White
        Write-Host "2. Sign up or log in (ensure billing is active)" -ForegroundColor White
        Write-Host "3. Click 'Create new secret key'" -ForegroundColor White
        Write-Host "4. Run this script again and paste it" -ForegroundColor White
        Write-Host ""
    }
    
    "5" {
        Write-Host "👋 Goodbye!" -ForegroundColor Cyan
        exit
    }
}

Write-Host ""
Write-Host "🚀 Run: .\terminus assistant" -ForegroundColor Green
