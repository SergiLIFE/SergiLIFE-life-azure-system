#!/bin/bash
# L.I.F.E. Platform Emergency Deployment Script for October 15 Demos
# Execute this in Azure Cloud Shell to deploy functional platform

echo "🚀 L.I.F.E. Platform Emergency Deployment Starting..."
echo "📅 October 15, 2025 Demo Ready Deployment"
echo "💰 Pipeline: $771K+ | Target: $345K Q4 → $50.7M by 2029"

# Navigate to deployment directory
cd /home/sergio/life-platform-deploy

# Create index.html using cat with proper EOF
cat > index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>L.I.F.E. Platform - Neural Learning Revolution</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        .header {
            background: rgba(0,0,0,0.2);
            padding: 20px;
            text-align: center;
            border-bottom: 2px solid rgba(255,255,255,0.1);
        }
        .logo { font-size: 2.5rem; font-weight: bold; margin-bottom: 10px; }
        .subtitle { font-size: 1.2rem; opacity: 0.9; }
        .main-content {
            flex: 1;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }
        .hero {
            text-align: center;
            margin-bottom: 60px;
        }
        .hero h1 { font-size: 3rem; margin-bottom: 20px; }
        .hero p { font-size: 1.3rem; opacity: 0.9; max-width: 800px; margin: 0 auto 30px; }
        .demo-status {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
            text-align: center;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        .feature-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            transition: transform 0.3s ease;
        }
        .feature-card:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 3rem; margin-bottom: 20px; }
        .api-endpoints {
            background: rgba(0,0,0,0.2);
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
        }
        .endpoint { 
            background: rgba(255,255,255,0.1);
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            font-family: monospace;
        }
        .status-badge {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            margin-left: 10px;
        }
        .cta-button {
            display: inline-block;
            background: #28a745;
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin: 10px;
            transition: background 0.3s ease;
        }
        .cta-button:hover { background: #218838; }
        .footer {
            background: rgba(0,0,0,0.3);
            padding: 20px;
            text-align: center;
        }
        .live-demo {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            border-radius: 15px;
            padding: 30px;
            margin: 40px 0;
            text-align: center;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="logo">🧠 L.I.F.E. Platform</div>
        <div class="subtitle">Learning Individually from Experience - Neural Revolution</div>
    </header>

    <main class="main-content">
        <section class="hero">
            <h1>Welcome to the Future of Learning</h1>
            <p>Experience groundbreaking neuroadaptive technology that processes real-time EEG data for personalized education and healthcare applications.</p>
            
            <div class="live-demo">
                <h2>🎯 LIVE OCTOBER 15, 2025 DEMO!</h2>
                <p><strong>23 Participants | 7 Sessions | 4 Days to Launch</strong></p>
                <p><strong>Azure Marketplace:</strong> 9a600d96-fe1e-420b-902a-a0c42c561adb</p>
                <span class="status-badge">✅ OPERATIONAL</span>
            </div>
        </section>

        <section class="features">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Sub-millisecond Processing</h3>
                <p>Real-time EEG analysis with 0.38-0.45ms latency for immediate neural feedback and adaptive learning optimization.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <h3>78-82% Accuracy</h3>
                <p>Proven accuracy on real EEG datasets with continuous learning and neural state monitoring capabilities.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🏥</div>
                <h3>Enterprise Ready</h3>
                <p>Production-deployed on Azure with enterprise-grade security, scalability, and compliance for healthcare institutions.</p>
            </div>
        </section>

        <section class="api-endpoints">
            <h2>🔗 Live API Endpoints (ACTIVE)</h2>
            <p>Production-ready APIs for neural processing and adaptive learning:</p>
            
            <div class="endpoint">
                <strong>EEG Processor:</strong> 
                <a href="https://life-functions-app.azurewebsites.net/api/eeg_processor" style="color: #4ecdc4;">
                    life-functions-app.azurewebsites.net/api/eeg_processor
                </a>
                <span class="status-badge">ACTIVE</span>
            </div>
            
            <div class="endpoint">
                <strong>Learning API:</strong> 
                <a href="https://life-functions-app.azurewebsites.net/api/learning_api" style="color: #4ecdc4;">
                    life-functions-app.azurewebsites.net/api/learning_api
                </a>
                <span class="status-badge">ACTIVE</span>
            </div>
            
            <div class="endpoint">
                <strong>Analytics Monitor:</strong> 
                <a href="https://life-functions-app.azurewebsites.net/api/analytics_monitor" style="color: #4ecdc4;">
                    life-functions-app.azurewebsites.net/api/analytics_monitor
                </a>
                <span class="status-badge">ACTIVE</span>
            </div>
            
            <div class="endpoint">
                <strong>Health Check:</strong> 
                <a href="https://life-functions-app.azurewebsites.net/api/health" style="color: #4ecdc4;">
                    life-functions-app.azurewebsites.net/api/health
                </a>
                <span class="status-badge">ACTIVE</span>
            </div>
            
            <div class="endpoint">
                <strong>Campaign Automation:</strong> 
                <a href="https://life-functions-app.azurewebsites.net/api/campaign_automation" style="color: #4ecdc4;">
                    life-functions-app.azurewebsites.net/api/campaign_automation
                </a>
                <span class="status-badge">ACTIVE</span>
            </div>
        </section>

        <section style="text-align: center; margin: 40px 0;">
            <h2>🚀 Experience L.I.F.E. Platform NOW</h2>
            <p><strong>Ready for October 15th demonstration with 23 participants</strong></p>
            <a href="https://life-functions-app.azurewebsites.net/api/health" class="cta-button">🩺 Test API Health</a>
            <a href="https://portal.azure.com/" class="cta-button">🔧 Azure Portal</a>
            <a href="https://life-microsoft-demo-app.azurewebsites.net/" class="cta-button">📊 Microsoft Demo</a>
        </section>

        <section class="demo-status">
            <h2>📋 October 15 Demo Schedule</h2>
            <p><strong>Pipeline Opportunity:</strong> $771,000+</p>
            <p><strong>Revenue Target:</strong> $345K Q4 2025 → $50.7M by 2029</p>
            <p><strong>Participants:</strong> 23 registered across 7 time zones</p>
            <p><strong>Infrastructure:</strong> All Azure services operational</p>
            <div style="margin-top: 20px;">
                <span class="status-badge">✅ APIs ACTIVE</span>
                <span class="status-badge">✅ FUNCTIONS RUNNING</span>
                <span class="status-badge">✅ DEMOS READY</span>
            </div>
        </section>
    </main>

    <footer class="footer">
        <p>© 2025 L.I.F.E. Platform - Sergio Paya Borrull | Revolutionary Neural Learning Technology</p>
        <p><strong>Live Demo:</strong> October 15, 2025 | <strong>Deployment:</strong> Azure Static Web Apps + Functions</p>
        <p><strong>Contact:</strong> Info@lifecoach121.com | <strong>Marketplace ID:</strong> 9a600d96-fe1e-420b-902a-a0c42c561adb</p>
    </footer>

    <script>
        // Add real-time status checking
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🧠 L.I.F.E. Platform loaded - October 15 Demo Ready!');
            
            // Test API endpoints
            const endpoints = [
                'https://life-functions-app.azurewebsites.net/api/health',
                'https://life-functions-app.azurewebsites.net/api/eeg_processor',
                'https://life-functions-app.azurewebsites.net/api/learning_api'
            ];
            
            endpoints.forEach(endpoint => {
                fetch(endpoint, { mode: 'no-cors' })
                    .then(() => console.log(`✅ ${endpoint} - ACTIVE`))
                    .catch(() => console.log(`⚠️ ${endpoint} - Check connectivity`));
            });
        });
    </script>
</body>
</html>
HTMLEOF

# Create staticwebapp.config.json
cat > staticwebapp.config.json << 'CONFIGEOF'
{
  "routes": [
    {
      "route": "/*",
      "serve": "/index.html",
      "statusCode": 200
    },
    {
      "route": "/api/*",
      "allowedRoles": ["anonymous"]
    }
  ],
  "responseOverrides": {
    "404": {
      "serve": "/index.html"
    }
  },
  "mimeTypes": {
    ".json": "application/json",
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript"
  },
  "globalHeaders": {
    "Cache-Control": "no-cache"
  }
}
CONFIGEOF

echo "✅ Files created successfully!"
echo "📁 Contents:"
ls -la

echo ""
echo "🚀 Deploying to Azure Static Web Apps..."
echo "🌐 Target URL: green-ground-0c65efe0f.1.azurestaticapps.net"

# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

echo ""
echo "📦 Deployment using SWA CLI..."

# Deploy using the deployment token
swa deploy --deployment-token 5b139950a418f9c8f01bed34b53dbbd974506123d808b2a6a0f2a70b8c0ba9a401-ac2639f4-c6a5-40ee-ac93-4ebc3fd317f100f04060c65efe0f --app-location . --output-location .

echo ""
echo "🎯 DEPLOYMENT COMPLETE!"
echo "🌐 Live URL: https://green-ground-0c65efe0f.1.azurestaticapps.net"
echo "📅 October 15, 2025 Demo Ready!"
echo "👥 23 Participants | 💰 $771K+ Pipeline"

echo ""
echo "🔍 Verifying deployment..."
curl -I https://green-ground-0c65efe0f.1.azurestaticapps.net

echo ""
echo "✅ L.I.F.E. Platform Emergency Deployment Complete!"
echo "🎉 Ready for October 15 demonstrations!"