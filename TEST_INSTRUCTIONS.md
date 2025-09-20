# Test Instructions for Reviewers

**Overview:**  
This submission includes the L.I.F.E. Platform solution for Azure Marketplace, with all required documentation, validation evidence, and deployment scripts. The platform is designed for easy deployment and validation in a standard Azure environment.

## 1. Deployment & Access
- No special license keys or paid accounts are required for testing.
- All scripts and configuration files are included in the repository.
- The solution can be deployed using the provided Azure CLI and PowerShell scripts (`setup-azure-oidc.ps1`, `azure.yaml`, `azd up`).

## 2. Test Accounts & Credentials
- **OIDC Authentication:**  
  Use your Microsoft/Azure test tenant credentials. No hardcoded secrets or passwords are required; authentication is handled via Azure OIDC and your test tenant.
- No additional test accounts or credentials are needed.

## 3. Validation & Evidence
- **Run the validation suite:**
  - Activate the Python environment and install dependencies (`pip install -r requirements.txt`).
  - Run the main validation script:  
    `python autonomous_optimizer.py`
  - All logs and evidence will be generated in the `logs/` and `results/` directories.
- **Review the README and MARKETPLACE_SUMMARY.md** for methodology, metrics, and validation claims.

## 4. Critical Notes
- No external dependencies beyond those in `requirements.txt`.
- No paid services or third-party licenses required for testing.
- All evidence and logs are Unicode-safe and human-readable.
- If you encounter any issues, please refer to the README for troubleshooting or contact the developer listed in the documentation.
