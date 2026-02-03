# Egyptian Van Sales System (VSS)

**Egyptian Van Sales System (VSS)** is a specialized Odoo 19 module designed to automate Direct Store Delivery (DSD) operations. It provides a complete solution for companies managing mobile distribution fleets, specifically tailored for the requirements of the Egyptian market.

---

## Key Features

### 1. Route Management & Filtering

- **Dynamic Route Logic:** Salesmen are restricted to viewing only the customers assigned to their specific route for the current day.
- **Scheduling:** Flexible management of geographical regions and daily delivery schedules.

### 2. Van Stock Control

- **Mobile Warehouses:** Each salesman is linked to a specific "Van Location" (Internal Location).
- **Inventory Validation:** Real-time stock checks to prevent any sales transaction if the items are not physically available in the van.

### 3. Automated Transaction Workflow

- **One-Click Confirm:** Custom logic that automates the entire backend process:
  - Validates and completes the Delivery Order (Stock Picking).
  - Generates and posts the Invoice.
  - Registers the Payment (Cash/Check/Credit) to the appropriate journal.

### 4. Localized Thermal Printing

- **80mm Receipt:** Optimized QWeb report designed for thermal mobile printers.
- **Bilingual Support:** Full RTL (Right-to-Left) layout with Arabic (Amount to Text) for total amounts.

---

## Technical Highlights

- **Odoo Version:** 19.0 (Latest)
- **Tech Stack:** Python, XML, QWeb, PostgreSQL.
- **Dependencies:** `sale_management`, `stock`, `account`, `hr`.
- **Security Layer:** \* **RBAC:** Role-Based Access Control using Groups.
  - **Record Rules:** Multi-level data isolation to ensure salesmen only access their authorized data.
  - **Context Execution:** Leveraging `sudo()` for secure cross-module payment registration.

---

## Security Roles

- **Salesman Group:** Limited access to assigned routes and personal sales performance.
- **Manager Group:** Comprehensive oversight of all routes, inventory levels, and team transactions.

---

## Installation

1. **Add to Path:** Copy the `van_sales` folder to your Odoo custom addons directory.
2. **Configuration:** Ensure the `depends` modules are available in your Odoo environment.
3. **Install:** \* Update the Apps list in Odoo.
   - Search for "Egyptian Van Sales System" and click **Install**.
