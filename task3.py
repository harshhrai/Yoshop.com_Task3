import pandas as pd

# Load the dataset
file_path = r"C:\Users\ADMIN\OneDrive - Amity University\Documents\Yoshop.com\YoshopsAutomation_Task3\Dataset\orders_2020_2021_DataSet_Updated.csv"
orders_df = pd.read_csv(file_path)

# Preprocessing relevant columns
orders_df['Billing Street Address'] = orders_df['Billing Street Address'].fillna("Unknown")
orders_df['Shipping Street Address'] = orders_df['Shipping Street Address'].fillna("Unknown")
orders_df['LineItem Qty'] = orders_df['LineItem Qty'].replace('[₹,]', '', regex=True).astype(float)
orders_df['Total'] = orders_df['Total'].replace('[₹,]', '', regex=True).astype(float)

# Condition 1: Shipping address differs from the billing address
diff_address_orders = orders_df[orders_df['Billing Street Address'] != orders_df['Shipping Street Address']]

# Condition 2: Multiple orders of the same item
multiple_item_orders = orders_df[orders_df.duplicated(subset=['Order #', 'LineItem Name'], keep=False)]

# Condition 3: Unusually large orders (e.g., top 5% of order quantities)
large_orders_threshold = orders_df['LineItem Qty'].quantile(0.95)
unusually_large_orders = orders_df[orders_df['LineItem Qty'] > large_orders_threshold]

# Condition 4: Multiple orders to the same address with different payment methods
multiple_payment_methods = orders_df.groupby(['Shipping Street Address']).filter(lambda x: x['Payment Method'].nunique() > 1)

# Condition 5: Unexpected international orders (assuming India as local)
international_orders = orders_df[orders_df['Shipping Country'] != 'India']

# Exporting results to CSV
eda_results = {
    "Shipping Differs from Billing": diff_address_orders,
    "Multiple Orders of Same Item": multiple_item_orders,
    "Unusually Large Orders": unusually_large_orders,
    "Multiple Payment Methods at Same Address": multiple_payment_methods,
    "Unexpected International Orders": international_orders
}

for key, df in eda_results.items():
    file_name = f"{key.replace(' ', '_')}.csv"
    df.to_csv(file_name, index=False)

from fpdf import FPDF

# Create PDF report
pdf = FPDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# Title
pdf.set_font("Arial", "B", 16)
pdf.cell(200, 10, txt="Fake Buyer Identification System - EDA Report", ln=True, align="C")

# Adding content to the PDF
pdf.set_font("Arial", size=12)
pdf.ln(10)

conditions = [
    "1. Shipping address differs from the billing address",
    "2. Multiple orders of the same item",
    "3. Unusually large orders",
    "4. Multiple orders to the same address with different payment methods",
    "5. Unexpected international orders"
]

for i, condition in enumerate(conditions, 1):
    pdf.cell(200, 10, txt=condition, ln=True)
    pdf.ln(2)

pdf.output("Fake_Buyer_Identification_EDA_Report.pdf")
