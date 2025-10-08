# L.I.F.E Platform - AI Agent Instructions

## Project Overview
This is the **L.I.F.E (Neuroadaptive Learning System) Platform** - an Azure-native system combining neuroadaptive learning with cloud-scale AI processing. The platform integrates Azure Logic Apps, Azure Functions, and Python-based visual generation tools for marketplace deployment.

## Architecture & Components

### Core Technology Stack
- **Azure Logic Apps Standard Runtime** - Primary orchestration layer
- **Azure Functions** (.NET 6.0/8.0) - Serverless compute for AI processing  
- **Python Scripts** - Visual asset generation and standalone utilities
- **Azure Marketplace Integration** - Deployment target with specific asset requirements

### Key Dependencies & Setup
The project requires specific Azure toolchain versions:
- Node.js v18.20.8 for Logic Apps runtime
- Azure Functions Core Tools v4.2.2
- .NET SDK 6.0 and 8.0 (dual-channel support)
- Python with Pillow for visual generation

Dependencies are auto-installed to `~/.azurelogicapps/dependencies/` during development setup.

## Development Patterns

### Visual Asset Generation
- **Pattern**: Standalone Python scripts that generate Azure Marketplace assets
- **Location**: `generate_visuals_standalone.py` creates logos (280x280, 216x216) and screenshots (1280x720)
- **Convention**: All assets saved to `marketplace_assets/` directory with specific naming:
  - `LIFE_Platform_Logo_280x280.png`
  - `LIFE_Platform_Logo_216x216.png` 
  - `LIFE_Platform_Screenshot_1280x720.png`

### Error Handling Strategy
- **Graceful degradation**: Scripts check dependencies first, provide clear installation instructions
- **Font fallbacks**: Uses Arial with default font fallback for cross-platform compatibility
- **User-friendly exits**: Always pause with "Press Enter to exit" for debugging

### Azure Integration Points
- **Logic Apps**: Uses standard runtime with local dependency management
- **Functions**: Multi-framework support (.NET 6.0/8.0) for different service tiers
- **Marketplace**: Assets must meet specific size/format requirements for Partner Center upload

## Critical Workflows

### Local Development Setup
1. Azure toolchain auto-downloads on first run to `~/.azurelogicapps/dependencies/`
2. Python dependencies checked at runtime with installation guidance
3. Visual assets generated locally before marketplace upload

### Asset Generation Process
```bash
# Double-click to run (no terminal required)
python generate_visuals_standalone.py
```
- Creates marketplace-ready assets with Azure branding (#0078D4 blue)
- Optimizes file sizes for Partner Center requirements
- Provides next-step guidance for marketplace upload

## Project-Specific Conventions

### Naming & Branding
- **Platform Name**: "L.I.F.E Platform" (always with periods)
- **Tagline**: "Neuroadaptive Learning System" 
- **Colors**: Azure blue (#0078D4, #005A9E) with white text
- **Domain**: References lifecoach-121.com for contact

### File Organization
- Standalone utilities use descriptive suffixes (`_standalone.py`)
- Output directories match Azure service names (`marketplace_assets/`)
- Error messages provide specific, actionable solutions

### Performance Metrics (Marketing)
When referencing system capabilities, use established metrics:
- 95.8% accuracy, 0.42ms latency, 880x faster than competitors
- 99.9% uptime SLA, Enterprise security & compliance

## Integration Notes
- Platform designed for Azure Marketplace distribution
- Supports both Azure Logic Apps Standard and Functions deployment models
- Visual assets must align with Azure Partner Center specifications
- Dependencies managed locally to avoid deployment conflicts