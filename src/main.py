from collections import defaultdict
from datetime import datetime

class CustomerData:
    def __init__(self):
        self.events = defaultdict(list)
    
    def ingest_event(self, event_type, customer_id, event_time, **kwargs):
        self.events[customer_id].append((event_time, event_type, kwargs.get('total_amount', 0)))

    def calculate_lifetime_value(self, customer_id):
        events = self.events[customer_id]
        total_expenditure = sum(amount for _, event_type, amount in events if event_type == 'ORDER')
        visit_frequency = sum(1 for _, event_type, _ in events if event_type == 'SITE_VISIT')
        return 52 * (total_expenditure / visit_frequency) if visit_frequency else 0

    def top_x_simple_ltv_customers(self, x):
        ltv_customers = [(self.calculate_lifetime_value(customer_id), customer_id) for customer_id in self.events]
        return sorted(ltv_customers, reverse=True)[:x]

# Example usage
if __name__ == "__main__":
    events = [
        ("CUSTOMER", "customer1", datetime(2021, 1, 1), {"last_name": "ch", "adr_city": "Dallas ", "adr_state": "TX"}),
        ("SITE_VISIT", "customer1", datetime(2023, 1, 5), {"tags": ["tag1", "tag2"]}),
        ("ORDER", "customer1", datetime(2024, 1, 10), {"total_amount": 100})
    ]
    
    customer_data = CustomerData()
    for event_type, customer_id, event_time, kwargs in events:
        customer_data.ingest_event(event_type, customer_id, event_time, **kwargs)
    
    top_customers = customer_data.top_x_simple_ltv_customers(1)
    print("Top Customers with the highest Simple Lifetime Value:")
    for ltv, customer_id in top_customers:
        print(f"Customer ID: {customer_id}, Simple Lifetime Value: {ltv}")
