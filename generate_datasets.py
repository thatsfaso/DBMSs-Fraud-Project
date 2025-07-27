import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Configurazione di base
n_customers = 1000
n_terminals = 200
days = 365

# Cartella di output
output_dir = "datasets"
os.makedirs(output_dir, exist_ok=True)

# 1. Generazione Profili Clienti (customer_profiles.csv)
def generate_customers(n_customers, output_file):
    customer_profiles = pd.DataFrame({
        "customer_id": [f"C{str(i).zfill(5)}" for i in range(n_customers)],
        "location": np.random.choice(["US", "EU", "Asia"], n_customers),
        "spending_frequency": np.random.poisson(5, n_customers),  # Media 5 trans/mese
        "spending_amount": np.random.lognormal(3, 0.5, n_customers)  # Media ~€50
    })
    customer_profiles.to_csv(f"{output_dir}/{output_file}", index=False)

# 2. Generazione Profili Terminali (terminals.csv)
def generate_terminals(n_terminals, output_file):
    terminal_profiles = pd.DataFrame({
        "terminal_id": [f"T{str(i).zfill(5)}" for i in range(n_terminals)],
        "location": np.random.choice(["US", "EU", "Asia"], n_terminals)
    })
    terminal_profiles.to_csv(f"{output_dir}/{output_file}", index=False)

# 3. Generazione Transazioni (transactions.csv)
def generate_transactions(customers_file, terminals_file, days, n_transactions, output_file):
    # Carica clienti e terminali
    customers = pd.read_csv(f"{output_dir}/{customers_file}")
    terminals = pd.read_csv(f"{output_dir}/{terminals_file}")

    transactions = []
    start_date = datetime.now() - timedelta(days=days)

    for _ in range(n_transactions):
        customer = customers.sample(1).iloc[0]
        terminal = terminals.sample(1).iloc[0]

        # Data casuale nell'ultimo anno
        transaction_date = start_date + timedelta(days=np.random.randint(0, days))

        transactions.append({
            "transaction_id": f"TX{len(transactions):08d}",
            "customer_id": customer["customer_id"],
            "terminal_id": terminal["terminal_id"],
            "amount": np.random.lognormal(3, 0.5),  # Media ~€50
            "date": transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "is_fraud": (np.random.random() < 0.01)  # 1% chance di frode
        })

    transactions_df = pd.DataFrame(transactions)
    transactions_df.to_csv(f"{output_dir}/{output_file}", index=False)

# Genera i 3 Dataset
if __name__ == "__main__":
    # Dataset Small (~50MB)
    generate_customers(n_customers, "customers_small.csv")
    generate_terminals(n_terminals, "terminals_small.csv")
    generate_transactions("customers_small.csv", "terminals_small.csv", days, 250_000, "transactions_small.csv")

    # Dataset Medium (~100MB)
    generate_customers(n_customers, "customers_medium.csv")
    generate_terminals(n_terminals, "terminals_medium.csv")
    generate_transactions("customers_medium.csv", "terminals_medium.csv", days, 500_000, "transactions_medium.csv")

    # Dataset Large (~200MB)
    generate_customers(n_customers, "customers_large.csv")
    generate_terminals(n_terminals, "terminals_large.csv")
    generate_transactions("customers_large.csv", "terminals_large.csv", days, 1_000_000, "transactions_large.csv")

    print("Dataset generati con successo!")