// Enhanced JavaScript with animations and better UX
class ZRADemo {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupQuickActions();
        console.log('🚀 ZRA SDK Demo Initialized');
    }

    setupEventListeners() {
        // Taxpayer Verification
        document.getElementById('verifyForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.verifyTaxpayer();
        });

        // Tax Calculation
        document.getElementById('taxForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.calculateTax();
        });

        // Compliance Check
        document.getElementById('complianceForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.checkCompliance();
        });

        // Compliance Report
        document.getElementById('complianceReportForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.generateComplianceReport();
        });
    }

    setupQuickActions() {
        // Auto-fill TPINs for quick testing
        document.querySelectorAll('.action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tpin = e.currentTarget.getAttribute('onclick').match(/'(\d+)'/)[1];
                this.fillAllTPINs(tpin);
            });
        });
    }

    fillAllTPINs(tpin) {
        document.getElementById('tpin').value = tpin;
        document.getElementById('complianceTpin').value = tpin;
        document.getElementById('reportTpin').value = tpin;
        
        // Auto-submit verification
        setTimeout(() => this.verifyTaxpayer(), 300);
    }

    async verifyTaxpayer() {
        const tpin = document.getElementById('tpin').value;
        const resultDiv = document.getElementById('verifyResult');
        
        if (!this.validateTPIN(tpin)) {
            this.showError(resultDiv, 'Please enter a valid 9-digit TPIN');
            return;
        }

        this.showLoading(resultDiv, '🔍 Verifying taxpayer information...');

        try {
            const response = await fetch('/api/verify', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tpin })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showTaxpayerResult(data.data);
            } else {
                this.showError(resultDiv, data.error);
            }
        } catch (error) {
            this.showError(resultDiv, `Network error: ${error.message}`);
        }
    }

    async calculateTax() {
        const income = document.getElementById('income').value;
        const taxType = document.getElementById('taxType').value;
        const resultDiv = document.getElementById('taxResult');
        
        if (!income || income <= 0) {
            this.showError(resultDiv, 'Please enter a valid income amount');
            return;
        }

        this.showLoading(resultDiv, '💰 Calculating tax amount...');

        try {
            const response = await fetch('/api/calculate-tax', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    income: parseFloat(income), 
                    tax_type: taxType 
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showTaxResult(data.data, taxType);
            } else {
                this.showError(resultDiv, data.error);
            }
        } catch (error) {
            this.showError(resultDiv, `Network error: ${error.message}`);
        }
    }

    async checkCompliance() {
        const tpin = document.getElementById('complianceTpin').value;
        const resultDiv = document.getElementById('complianceResult');
        
        if (!this.validateTPIN(tpin)) {
            this.showError(resultDiv, 'Please enter a valid 9-digit TPIN');
            return;
        }

        this.showLoading(resultDiv, '🔍 Checking compliance status...');

        try {
            const response = await fetch('/api/compliance', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tpin })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showComplianceResult(data.compliance_data);
            } else {
                this.showError(resultDiv, data.error);
            }
        } catch (error) {
            this.showError(resultDiv, `Network error: ${error.message}`);
        }
    }

    async generateComplianceReport() {
        const tpin = document.getElementById('reportTpin').value;
        const resultDiv = document.getElementById('complianceReportResult');
        
        if (!this.validateTPIN(tpin)) {
            this.showError(resultDiv, 'Please enter a valid 9-digit TPIN');
            return;
        }

        this.showLoading(resultDiv, '📊 Generating comprehensive compliance report...');

        try {
            const response = await fetch('/api/compliance-report', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tpin })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.showComplianceReport(data.compliance_report);
            } else {
                this.showError(resultDiv, data.error);
            }
        } catch (error) {
            this.showError(resultDiv, `Network error: ${error.message}`);
        }
    }

    // UI Helper Methods
    showLoading(container, message) {
        container.innerHTML = `
            <div class="result info">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="loading"></div>
                    <span>${message}</span>
                </div>
            </div>
        `;
    }

    showError(container, message) {
        container.innerHTML = `
            <div class="result error">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>${message}</span>
                </div>
            </div>
        `;
    }

    showTaxpayerResult(taxpayer) {
        const resultDiv = document.getElementById('verifyResult');
        resultDiv.innerHTML = `
            <div class="result success">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <i class="fas fa-check-circle" style="color: #28a745; font-size: 1.5rem;"></i>
                    <h4 style="margin: 0;">Taxpayer Verified Successfully</h4>
                </div>
                <div class="taxpayer-details">
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-user"></i> Name:</span>
                        <span class="detail-value">${taxpayer.name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-building"></i> Business:</span>
                        <span class="detail-value">${taxpayer.business_name}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-envelope"></i> Email:</span>
                        <span class="detail-value">${taxpayer.email}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-phone"></i> Phone:</span>
                        <span class="detail-value">${taxpayer.phone}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-map-marker-alt"></i> Tax Center:</span>
                        <span class="detail-value">${taxpayer.tax_center}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label"><i class="fas fa-calendar"></i> Registration:</span>
                        <span class="detail-value">${taxpayer.registration_date}</span>
                    </div>
                </div>
            </div>
        `;
    }

    showTaxResult(calculation, taxType) {
        const resultDiv = document.getElementById('taxResult');
        const taxName = taxType === 'income' ? 'Income Tax' : 'VAT';
        
        resultDiv.innerHTML = `
            <div class="result info">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <i class="fas fa-calculator" style="color: #17a2b8; font-size: 1.5rem;"></i>
                    <h4 style="margin: 0;">${taxName} Calculation</h4>
                </div>
                <div class="calculation-details">
                    <div class="detail-row">
                        <span class="detail-label">Gross Income:</span>
                        <span class="detail-value">ZMW ${calculation.gross_income.toLocaleString()}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Tax Amount:</span>
                        <span class="detail-value" style="color: #dc3545; font-weight: bold;">
                            ZMW ${calculation.tax_amount.toLocaleString()}
                        </span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Effective Tax Rate:</span>
                        <span class="detail-value" style="color: #28a745; font-weight: bold;">
                            ${calculation.effective_tax_rate}%
                        </span>
                    </div>
                </div>
            </div>
        `;
    }

    showComplianceResult(compliance) {
        const resultDiv = document.getElementById('complianceResult');
        const statusClass = this.getComplianceStatusClass(compliance.compliance_status);
        const riskClass = `risk-${compliance.risk_level.toLowerCase()}`;
        
        let issuesHTML = '';
        if (compliance.compliance_issues && compliance.compliance_issues.length > 0) {
            issuesHTML = `
                <div class="compliance-issues">
                    <h5><i class="fas fa-exclamation-triangle"></i> Compliance Issues:</h5>
                    <ul>
                        ${compliance.compliance_issues.map(issue => `<li>${issue}</li>`).join('')}
                    </ul>
                </div>
            `;
        } else {
            issuesHTML = '<p style="color: #28a745;"><i class="fas fa-check-circle"></i> No compliance issues found</p>';
        }

        resultDiv.innerHTML = `
            <div class="result ${statusClass}">
                <div class="compliance-header">
                    <div class="compliance-status">
                        <span class="status-badge ${this.getComplianceBadgeClass(compliance.compliance_status)}">
                            ${compliance.compliance_status}
                        </span>
                        <span class="compliance-score">${compliance.compliance_score}/100</span>
                    </div>
                    <div class="risk-level ${riskClass}">
                        <i class="fas fa-flag"></i> ${compliance.risk_level} Risk
                    </div>
                </div>
                
                <div class="compliance-details">
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Outstanding Returns</span>
                            <span class="detail-value">${compliance.outstanding_returns}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Outstanding Payments</span>
                            <span class="detail-value">ZMW ${compliance.outstanding_payments.toLocaleString()}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Penalties</span>
                            <span class="detail-value">ZMW ${compliance.penalties.toLocaleString()}</span>
                        </div>
                    </div>
                    
                    ${issuesHTML}
                </div>
            </div>
        `;
    }

    showComplianceReport(report) {
        const resultDiv = document.getElementById('complianceReportResult');
        const compliance = report.compliance_summary;
        const statusClass = this.getComplianceStatusClass(compliance.compliance_status);
        
        resultDiv.innerHTML = `
            <div class="result ${statusClass}">
                <div class="report-header">
                    <h4><i class="fas fa-file-alt"></i> Comprehensive Compliance Report</h4>
                    <small>Generated: ${report.report_generated}</small>
                </div>
                
                <div class="taxpayer-info">
                    <h5><i class="fas fa-user-tie"></i> Taxpayer Information</h5>
                    <div class="detail-grid">
                        <div class="detail-item">
                            <span class="detail-label">Name</span>
                            <span class="detail-value">${report.taxpayer_info.name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Business</span>
                            <span class="detail-value">${report.taxpayer_info.business_name}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">TPIN</span>
                            <span class="detail-value">${report.taxpayer_info.tpin}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Tax Center</span>
                            <span class="detail-value">${report.taxpayer_info.tax_center}</span>
                        </div>
                    </div>
                </div>
                
                <div class="compliance-summary">
                    <h5><i class="fas fa-chart-bar"></i> Compliance Summary</h5>
                    <div class="summary-grid">
                        <div class="summary-item">
                            <span class="summary-label">Status</span>
                            <span class="summary-value ${this.getComplianceBadgeClass(compliance.compliance_status)}">
                                ${compliance.compliance_status}
                            </span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Score</span>
                            <span class="summary-value">${compliance.compliance_score}/100</span>
                        </div>
                        <div class="summary-item">
                            <span class="summary-label">Risk Level</span>
                            <span class="summary-value risk-${compliance.risk_level.toLowerCase()}">
                                ${compliance.risk_level}
                            </span>
                        </div>
                    </div>
                </div>
                
                <div class="recommendations">
                    <h5><i class="fas fa-lightbulb"></i> Recommendations</h5>
                    <ul>
                        ${report.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    // Utility Methods
    validateTPIN(tpin) {
        return /^\d{9}$/.test(tpin);
    }

    getComplianceStatusClass(status) {
        const statusMap = {
            'Fully Compliant': 'success',
            'Mostly Compliant': 'warning', 
            'Non-Compliant': 'error',
            'Under Review': 'info'
        };
        return statusMap[status] || 'info';
    }

    getComplianceBadgeClass(status) {
        const badgeMap = {
            'Fully Compliant': 'badge-success',
            'Mostly Compliant': 'badge-warning',
            'Non-Compliant': 'badge-error',
            'Under Review': 'badge-info'
        };
        return badgeMap[status] || 'badge-info';
    }
}

// Additional CSS for enhanced components
const additionalStyles = `
    .detail-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 8px 0;
        border-bottom: 1px solid rgba(0,0,0,0.1);
    }
    
    .detail-row:last-child {
        border-bottom: none;
    }
    
    .detail-label {
        font-weight: 600;
        color: #555;
    }
    
    .detail-value {
        font-weight: 500;
    }
    
    .compliance-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .compliance-status {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .badge-success { background: #28a745; color: white; }
    .badge-warning { background: #ffc107; color: black; }
    .badge-error { background: #dc3545; color: white; }
    .badge-info { background: #17a2b8; color: white; }
    
    .risk-level {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .risk-low { background: #d4edda; color: #155724; }
    .risk-medium { background: #fff3cd; color: #856404; }
    .risk-high { background: #f8d7da; color: #721c24; }
    
    .detail-grid, .summary-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .detail-item, .summary-item {
        background: rgba(255,255,255,0.5);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
    }
    
    .compliance-issues ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .compliance-issues li {
        margin-bottom: 0.5rem;
        color: #dc3545;
    }
    
    .recommendations ul {
        margin: 0;
        padding-left: 1.5rem;
    }
    
    .recommendations li {
        margin-bottom: 0.5rem;
        color: #155724;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

// Global quick test function
function quickTest(tpin) {
    const demo = new ZRADemo();
    demo.fillAllTPINs(tpin);
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ZRADemo();
});