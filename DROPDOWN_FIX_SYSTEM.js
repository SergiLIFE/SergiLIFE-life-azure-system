/*
🎯 L.I.F.E. Platform - Interactive Dropdown Menu Fix
======================================================

Fixes dropdown menus to be fully interactive and clickable
Ensures menu items can be clicked to activate functions
Copyright 2025 - Sergio Paya Borrull
*/

class AdvancedDropdownSystem {
    constructor() {
        this.dropdowns = new Map();
        this.activeDropdown = null;
        this.init();
    }

    init() {
        console.log('✅ Initializing Advanced Dropdown System...');
        this.scanForDropdowns();
        this.attachGlobalListeners();
        this.createDropdownStyles();
    }

    // Create comprehensive dropdown styles
    createDropdownStyles() {
        if (document.getElementById('dropdown-system-styles')) return;

        const styles = `
            <style id="dropdown-system-styles">
                /* Dropdown Container */
                .life-dropdown-container {
                    position: relative;
                    display: inline-block;
                }

                /* Dropdown Toggle Button */
                .life-dropdown-toggle {
                    background: linear-gradient(135deg, #0066cc 0%, #004499 100%);
                    color: white;
                    padding: 12px 20px;
                    font-size: 1em;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    transition: all 0.3s ease;
                    box-shadow: 0 2px 8px rgba(0, 102, 204, 0.3);
                    user-select: none;
                }

                .life-dropdown-toggle:hover {
                    background: linear-gradient(135deg, #0080ff 0%, #0055dd 100%);
                    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.5);
                    transform: translateY(-2px);
                }

                .life-dropdown-toggle:active {
                    transform: translateY(0);
                }

                .life-dropdown-toggle.active {
                    background: linear-gradient(135deg, #004499 0%, #002266 100%);
                    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
                }

                /* Dropdown Arrow Indicator */
                .life-dropdown-arrow {
                    display: inline-block;
                    transition: transform 0.3s ease;
                    font-size: 0.8em;
                }

                .life-dropdown-toggle.active .life-dropdown-arrow {
                    transform: rotate(180deg);
                }

                /* Dropdown Menu */
                .life-dropdown-menu {
                    position: absolute;
                    top: 100%;
                    left: 0;
                    background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
                    border: 2px solid #0066cc;
                    border-radius: 8px;
                    min-width: 250px;
                    margin-top: 8px;
                    box-shadow: 0 8px 24px rgba(0, 102, 204, 0.3), 0 12px 32px rgba(0, 0, 0, 0.4);
                    z-index: 10000;
                    opacity: 0;
                    visibility: hidden;
                    transform: translateY(-10px) scaleY(0.95);
                    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
                    max-height: 400px;
                    overflow-y: auto;
                    backdrop-filter: blur(10px);
                }

                .life-dropdown-menu.active {
                    opacity: 1;
                    visibility: visible;
                    transform: translateY(0) scaleY(1);
                }

                /* Dropdown Menu Items */
                .life-dropdown-item {
                    padding: 14px 18px;
                    color: #ffffff;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    transition: all 0.2s ease;
                    border-left: 3px solid transparent;
                    font-size: 0.95em;
                    font-weight: 500;
                }

                .life-dropdown-item:first-child {
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }

                .life-dropdown-item:last-child {
                    border-bottom-left-radius: 6px;
                    border-bottom-right-radius: 6px;
                }

                .life-dropdown-item:hover {
                    background: rgba(0, 102, 204, 0.2);
                    border-left-color: #ffd700;
                    padding-left: 22px;
                    color: #ffd700;
                    box-shadow: inset 0 0 10px rgba(0, 102, 204, 0.1);
                }

                .life-dropdown-item:active {
                    background: rgba(0, 102, 204, 0.35);
                    transform: scale(0.98);
                }

                .life-dropdown-item.selected {
                    background: rgba(0, 102, 204, 0.25);
                    border-left-color: #ffd700;
                    color: #ffd700;
                }

                .life-dropdown-item:disabled {
                    opacity: 0.5;
                    cursor: not-allowed;
                    background: transparent;
                }

                .life-dropdown-item:disabled:hover {
                    background: transparent;
                    border-left-color: transparent;
                    color: #ffffff;
                }

                /* Dropdown Item Icon */
                .life-dropdown-item-icon {
                    font-size: 1.2em;
                    min-width: 20px;
                }

                /* Dropdown Item Text */
                .life-dropdown-item-text {
                    flex: 1;
                }

                /* Dropdown Item Description */
                .life-dropdown-item-desc {
                    font-size: 0.85em;
                    color: #888;
                    margin-top: 3px;
                    display: block;
                }

                /* Dropdown Header */
                .life-dropdown-header {
                    padding: 12px 18px;
                    border-bottom: 1px solid rgba(0, 102, 204, 0.3);
                    font-weight: bold;
                    color: #0066cc;
                    background: rgba(0, 102, 204, 0.05);
                }

                /* Dropdown Divider */
                .life-dropdown-divider {
                    height: 1px;
                    background: rgba(0, 102, 204, 0.2);
                    margin: 8px 0;
                }

                /* Scrollbar Styling */
                .life-dropdown-menu::-webkit-scrollbar {
                    width: 6px;
                }

                .life-dropdown-menu::-webkit-scrollbar-track {
                    background: rgba(0, 102, 204, 0.1);
                    border-radius: 3px;
                }

                .life-dropdown-menu::-webkit-scrollbar-thumb {
                    background: rgba(0, 102, 204, 0.4);
                    border-radius: 3px;
                }

                .life-dropdown-menu::-webkit-scrollbar-thumb:hover {
                    background: rgba(0, 102, 204, 0.6);
                }

                /* Dropdown Right Aligned */
                .life-dropdown-container.right .life-dropdown-menu {
                    left: auto;
                    right: 0;
                }

                /* Keyboard Focus State */
                .life-dropdown-item:focus-visible {
                    outline: 2px solid #ffd700;
                    outline-offset: -2px;
                }

                /* Mobile Responsive */
                @media (max-width: 768px) {
                    .life-dropdown-menu {
                        min-width: 200px;
                        max-height: 300px;
                    }

                    .life-dropdown-item {
                        padding: 12px 14px;
                        font-size: 0.9em;
                    }
                }

                /* Loading State */
                .life-dropdown-loading {
                    padding: 20px;
                    text-align: center;
                    color: #888;
                }

                .life-dropdown-loading::after {
                    content: '...';
                    animation: dots 1.5s steps(4, end) infinite;
                }

                @keyframes dots {
                    0%, 20% { content: '.'; }
                    40% { content: '..'; }
                    60%, 100% { content: '...'; }
                }

                /* Empty State */
                .life-dropdown-empty {
                    padding: 20px;
                    text-align: center;
                    color: #888;
                    font-style: italic;
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', styles);
        console.log('✅ Dropdown styles injected');
    }

    // Scan for existing dropdowns and enhance them
    scanForDropdowns() {
        // Find all select elements
        document.querySelectorAll('select').forEach(select => {
            if (!select.closest('.life-dropdown-container')) {
                this.convertSelectToDropdown(select);
            }
        });

        // Find all elements with data-dropdown attribute
        document.querySelectorAll('[data-dropdown]').forEach(element => {
            this.enhanceDropdown(element);
        });
    }

    // Convert HTML select to custom dropdown
    convertSelectToDropdown(selectElement) {
        const options = Array.from(selectElement.options);
        const selectedIndex = selectElement.selectedIndex;

        // Create dropdown container
        const container = document.createElement('div');
        container.className = 'life-dropdown-container';

        // Create toggle button
        const toggle = document.createElement('button');
        toggle.className = 'life-dropdown-toggle';
        toggle.innerHTML = `
            <span>${options[selectedIndex]?.text || 'Select...'}</span>
            <span class="life-dropdown-arrow">▼</span>
        `;

        // Create dropdown menu
        const menu = document.createElement('div');
        menu.className = 'life-dropdown-menu';

        // Add header if provided
        const header = selectElement.dataset.header;
        if (header) {
            const headerEl = document.createElement('div');
            headerEl.className = 'life-dropdown-header';
            headerEl.textContent = header;
            menu.appendChild(headerEl);
        }

        // Add options as menu items
        options.forEach((option, index) => {
            const item = document.createElement('div');
            item.className = 'life-dropdown-item';
            if (index === selectedIndex) item.classList.add('selected');
            item.innerHTML = `
                <span class="life-dropdown-item-text">${option.text}</span>
            `;

            item.addEventListener('click', (e) => {
                e.stopPropagation();
                selectElement.selectedIndex = index;
                selectElement.dispatchEvent(new Event('change', { bubbles: true }));

                toggle.querySelector('span').textContent = option.text;
                menu.querySelectorAll('.life-dropdown-item').forEach(el => {
                    el.classList.remove('selected');
                });
                item.classList.add('selected');

                toggle.classList.remove('active');
                menu.classList.remove('active');

                console.log(`✅ Selected: ${option.text}`);
            });

            menu.appendChild(item);
        });

        // Toggle button event
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isActive = menu.classList.contains('active');

            if (this.activeDropdown && this.activeDropdown !== menu) {
                this.activeDropdown.classList.remove('active');
                this.activeDropdown.previousElementSibling?.classList.remove('active');
            }

            menu.classList.toggle('active');
            toggle.classList.toggle('active');
            this.activeDropdown = isActive ? null : menu;

            console.log(`📊 Dropdown toggled: ${isActive ? 'closed' : 'opened'}`);
        });

        container.appendChild(toggle);
        container.appendChild(menu);

        selectElement.style.display = 'none';
        selectElement.parentNode.insertBefore(container, selectElement);

        console.log(`✅ Converted select to interactive dropdown: ${options[selectedIndex]?.text}`);
    }

    // Enhance existing dropdown elements
    enhanceDropdown(element) {
        const items = element.querySelectorAll('[data-dropdown-item]');

        items.forEach(item => {
            item.classList.add('life-dropdown-item');

            item.addEventListener('click', (e) => {
                e.stopPropagation();
                this.handleDropdownItemClick(item, element);
            });

            item.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.handleDropdownItemClick(item, element);
                }
            });
        });
    }

    // Handle dropdown item click
    handleDropdownItemClick(item, container) {
        const action = item.dataset.action;
        const target = item.dataset.target;

        console.log(`🎯 Dropdown item clicked: ${item.textContent.trim()}`);

        // Remove active state from siblings
        item.parentElement.querySelectorAll('.life-dropdown-item.selected').forEach(el => {
            el.classList.remove('selected');
        });

        item.classList.add('selected');

        // Execute action
        if (action && typeof window[action] === 'function') {
            console.log(`➡️ Executing action: ${action}`);
            window[action](target);
        } else if (target) {
            console.log(`➡️ Navigating to: ${target}`);
            window.location.href = target;
        }

        // Close dropdown
        const menu = item.closest('.life-dropdown-menu');
        if (menu) {
            menu.classList.remove('active');
            const toggle = menu.previousElementSibling;
            if (toggle) toggle.classList.remove('active');
        }
    }

    // Attach global event listeners
    attachGlobalListeners() {
        // Close dropdowns when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.life-dropdown-container')) {
                document.querySelectorAll('.life-dropdown-menu.active').forEach(menu => {
                    menu.classList.remove('active');
                    const toggle = menu.previousElementSibling;
                    if (toggle) toggle.classList.remove('active');
                });
                this.activeDropdown = null;
            }
        });

        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.life-dropdown-menu.active').forEach(menu => {
                    menu.classList.remove('active');
                    const toggle = menu.previousElementSibling;
                    if (toggle) toggle.classList.remove('active');
                });
                this.activeDropdown = null;
            }
        });

        console.log('✅ Global dropdown listeners attached');
    }

    // Create a new dropdown programmatically
    createDropdown(containerId, items, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) {
            console.error(`❌ Container not found: ${containerId}`);
            return;
        }

        const dropdownContainer = document.createElement('div');
        dropdownContainer.className = 'life-dropdown-container';
        if (options.align === 'right') {
            dropdownContainer.classList.add('right');
        }

        // Create toggle
        const toggle = document.createElement('button');
        toggle.className = 'life-dropdown-toggle';
        toggle.innerHTML = `
            <span>${options.label || 'Select Option'}</span>
            <span class="life-dropdown-arrow">▼</span>
        `;

        // Create menu
        const menu = document.createElement('div');
        menu.className = 'life-dropdown-menu';

        // Add header if provided
        if (options.header) {
            const header = document.createElement('div');
            header.className = 'life-dropdown-header';
            header.textContent = options.header;
            menu.appendChild(header);
        }

        // Add items
        items.forEach((item, index) => {
            const itemEl = document.createElement('div');
            itemEl.className = 'life-dropdown-item';
            itemEl.innerHTML = `
                <span class="life-dropdown-item-icon">${item.icon || '•'}</span>
                <div>
                    <span class="life-dropdown-item-text">${item.label}</span>
                    ${item.description ? `<span class="life-dropdown-item-desc">${item.description}</span>` : ''}
                </div>
            `;

            itemEl.addEventListener('click', (e) => {
                e.stopPropagation();

                // Remove selected state
                menu.querySelectorAll('.life-dropdown-item.selected').forEach(el => {
                    el.classList.remove('selected');
                });

                itemEl.classList.add('selected');

                // Execute callback
                if (item.onClick) {
                    console.log(`➡️ Executing callback for: ${item.label}`);
                    item.onClick(item);
                }

                // Close dropdown
                menu.classList.remove('active');
                toggle.classList.remove('active');

                console.log(`✅ Clicked dropdown item: ${item.label}`);
            });

            menu.appendChild(itemEl);
        });

        // Toggle click handler
        toggle.addEventListener('click', (e) => {
            e.stopPropagation();
            const isActive = menu.classList.contains('active');

            if (this.activeDropdown && this.activeDropdown !== menu) {
                this.activeDropdown.classList.remove('active');
                this.activeDropdown.previousElementSibling?.classList.remove('active');
            }

            menu.classList.toggle('active');
            toggle.classList.toggle('active');
            this.activeDropdown = isActive ? null : menu;
        });

        dropdownContainer.appendChild(toggle);
        dropdownContainer.appendChild(menu);

        container.innerHTML = '';
        container.appendChild(dropdownContainer);

        console.log(`✅ Created new dropdown with ${items.length} items`);
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.lifeDropdownSystem = new AdvancedDropdownSystem();
    });
} else {
    window.lifeDropdownSystem = new AdvancedDropdownSystem();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdvancedDropdownSystem;
}
